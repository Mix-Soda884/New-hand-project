import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# === パラメータ設定 ===
window_size = 4  # スライディングウィンドウのサイズ
threshold_multiplier = 1.0  # ラベル付けの動的閾値の倍率

# === データの読み込み ===
try:
    file1 = np.loadtxt('fingdata[1].txt')  # 尺側手根屈筋のデータ
    file2 = np.loadtxt('fingdata[2].txt')  # 短橈側手根伸筋のデータ
except Exception as e:
    print(f"データ読み込みエラー: {e}")
    exit()

# データ長を短い方に合わせる
min_length = min(len(file1), len(file2))
file1, file2 = file1[:min_length], file2[:min_length]

# データを正規化
scaler = StandardScaler()
file1 = scaler.fit_transform(file1.reshape(-1, 1)).flatten()
file2 = scaler.fit_transform(file2.reshape(-1, 1)).flatten()

# 全データの勾配を計算
grad_file1 = np.gradient(file1)
grad_file2 = np.gradient(file2)

# 勾配の差を計算
grad_diff_all = grad_file1 - grad_file2

# 動的な閾値を計算
threshold = threshold_multiplier * np.std(grad_diff_all)
print(f"動的に計算された閾値: {threshold:.2f}")
threshold = max(threshold, 0.1)  # 最小値を設定して閾値が極端に小さくならないようにする

# === スライディングウィンドウ法で特徴量とラベルを作成 ===
X = []
Y = []

for i in range(len(file1) - window_size):
    # ウィンドウ内のデータを取得
    segment1 = file1[i:i + window_size]
    segment2 = file2[i:i + window_size]

    # ウィンドウ内の勾配を計算
    grad1 = np.gradient(segment1)
    grad2 = np.gradient(segment2)

    # 勾配差の平均を計算
    # grad_diff = np.mean(grad1 - grad2)

    # 入力データを作成（2チャンネルで結合）
    X.append(np.stack([segment1, segment2], axis=-1))

    # ラベル付け（勾配差を基に状態を判定）
    if (grad1 > threshold).any():
        Y.append(1)  # 「閉じている」
    elif (grad2 < threshold).any():
        Y.append(0)  # 「開いている」
    else:
        Y.append(2)  # 「不明」

X = np.array(X)
Y = np.array(Y)

# 不明な状態（ラベル2）は除外
mask = Y != 2
if np.sum(mask) == 0:  # 有効なデータが存在しない場合
    print("データがすべて不明ラベルとして分類されました。閾値の再設定が必要です。")
    exit()
X = X[mask]
Y = Y[mask]
print(f"有効なサンプル数: {len(Y)}")

# === 訓練データとテストデータに分割 ===
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# === ニューラルネットワークモデルの構築 ===
model = Sequential([
    LSTM(64, input_shape=(window_size, 2), activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # 2値分類（開いている=0, 閉じている=1）
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# === モデルの学習 ===
history = model.fit(X_train, Y_train, epochs=20, batch_size=16, validation_split=0.1)

# === テストデータでの評価 ===
Y_pred = model.predict(X_test)
Y_pred_labels = (Y_pred > 0.5).astype(int)

accuracy = accuracy_score(Y_test, Y_pred_labels)
print(f"テストデータの精度: {accuracy:.2f}")

# === 結果の表示 ===
print("予測結果:")
for i, (true_label, pred_label) in enumerate(zip(Y_test[:20], Y_pred_labels[:20])):
    state = "閉じている" if pred_label == 1 else "開いている"
    print(f"サンプル {i + 1}: 真のラベル = {true_label}, 予測 = {state}")
