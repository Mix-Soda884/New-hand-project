import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# === パラメータ設定 ===
window_size = 10  # スライディングウィンドウのサイズ
threshold = 0.3  # ラベル付けの閾値（適宜調整）

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

# === スライディングウィンドウ法で特徴量とラベルを作成 ===
X = []
Y = []

for i in range(len(file1) - window_size):
    # ウィンドウ内のデータを取得
    segment1 = file1[i:i + window_size]
    segment2 = file2[i:i + window_size]
    
    # 入力データを作成（2チャンネルで結合）
    X.append(np.stack([segment1, segment2], axis=-1))
    
    # ラベル付け（単純に2つのチャンネルの差分で状態を仮定）
    if np.mean(segment1) > threshold and np.mean(segment2) < -threshold:
        Y.append(1)  # 「閉じている」
    elif np.mean(segment2) > threshold and np.mean(segment1) < -threshold:
        Y.append(0)  # 「開いている」
    else:
        Y.append(2)  # 「不明」

X = np.array(X)
Y = np.array(Y)

# 不明な状態（ラベル2）は除外
mask = Y != 2
X = X[mask]
Y = Y[mask]

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
for i, (true_label, pred_label) in enumerate(zip(Y_test[:10], Y_pred_labels[:10])):
    state = "閉じている" if pred_label == 1 else "開いている"
    print(f"サンプル {i + 1}: 真のラベル = {true_label}, 予測 = {state}")
