import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# === パラメータ設定 ===
window_size = 5  # スライディングウィンドウのサイズ
threshold_multiplier = 1.0  # ラベル付けの動的閾値の倍率

# === データの読み込み ===
try:
    file1 = np.loadtxt('fingdata[1a].txt')  # 尺側手根屈筋のデータ
    file2 = np.loadtxt('fingdata[1b].txt')  # 短橈側手根伸筋のデータ
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
segb1 = 0
segb2 = 0

# 勾配の差を計算
grad_diff_all = grad_file1 - grad_file2

# 動的閾値を計算する関数
def calculate_dynamic_threshold(predictions, strategy='mean'):
    """
    動的閾値を計算する。
    :param predictions: モデルが出力した確率値（リストまたは配列）
    :param strategy: 閾値の計算方法（'mean', 'median', 'percentile'など）
    :return: 計算された閾値
    """
    if strategy == 'mean':
        return np.mean(predictions)
    elif strategy == 'median':
        return np.median(predictions)
    elif strategy == 'percentile':
        return np.percentile(predictions, 75)  # 75%タイル値
    else:
        raise ValueError("無効なstrategy指定")

# 初期の閾値設定
dynamic_threshold = 0.5

# === スライディングウィンドウ法で特徴量とラベルを作成 ===
X = []
Y = []
segY1 = []
segY2 = []
C = len(file1) - window_size

for i in range(len(file1) - window_size):

    # ウィンドウ内のデータを取得
    segment1 = file1[i:i + window_size]
    segment2 = file2[i:i + window_size]

    # ウィンドウ内の勾配を計算
    segment11 = segment1 * segment1 #ウィンドウ内の数値を2乗
    segmean1 = np.mean(segment11) #2乗したウィンドウ内の数値を平均化
    segment22 = segment2 * segment2
    segmean2 = np.mean(segment22)
    seg1 = (segmean1 - segb1) #直前のseg1と比較
    seg2 = (segmean2 - segb2) #直前のseg2と比較
    grad = abs(seg1) - abs(seg2)

    # 入力データを作成（2チャンネルで結合）
    X.append(np.stack([segment1, segment2], axis=-1))

    # ラベル付け（勾配差を基に状態を判定）
    if (seg1 > seg2).any():
        Y.append(1)  #「閉じている」
    elif (seg1 < seg2).any():
        Y.append(0)  #「開いている」
    else:
        Y.append(2)  #「不明」
    
    segb1 = seg1
    segb2 = seg2    

X = np.array(X)
Y = np.array(Y)

# 不明な状態（ラベル2）は除外
mask = Y != 2
if np.sum(mask) == 0:  # 有効なデータが存在しない場合
    print("データがすべて不明ラベルとして分類されました。閾値の再設定が必要です。")
    exit()
X = X[mask]
Y = Y[mask]

# === 訓練データとテストデータに分割 ===
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

try:
    model = load_model('model_b.h5')  # 既存モデルをロード
except:
    # 新しいモデルを構築
    model = Sequential([
        LSTM(128, input_shape=(window_size, 2), activation='relu', return_sequences=True),
        LSTM(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 新しいOptimizerを作成してコンパイルし直す
model.compile(
    optimizer='adam',  # 必要に応じて他のオプティマイザを指定
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# === モデルの学習 ===
history = model.fit(X_train, Y_train, epochs=20, batch_size=16, validation_split=0.1)

# === モデルの保存 ===
model.save('model_b.h5')  

# === テストデータでの評価 ===
Y_pred = model.predict(X_test)
Y_pred_labels = []
Y_risalt = []
for pred in Y_pred:
    # 閾値を更新（例: 平均値を動的閾値とする）
    # dynamic_threshold = calculate_dynamic_threshold(Y_pred, strategy='mean')
    
    # 動的閾値に基づいてラベルを決定
    Y_pred_labels.append(int(pred > 0.5))
    Y_risalt.append(np.stack([pred], axis=-1))

accuracy = accuracy_score(Y_test, Y_pred_labels)
print(f"有効なサンプル数: {len(Y)}/{(C)}")
print(f"テストデータの精度: {accuracy:.2f}")

# === 結果の表示 ===
print("予測結果:")
for i, (true_label, pred_label) in enumerate(zip(Y_test[:10], Y_pred_labels[:10])):
    prob = Y_pred[i][0]  
    state = "閉じている" if pred_label == 1 else "開いている"
    print(f"サンプル {i + 1}: 真のラベル = {true_label}, 確率 = {prob:.4f}, 予測 = {state}")

plt.plot(history.history['accuracy'], label='Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim(0, 1.00)
yticks = np.arange(0, 1.01, 0.25) 
plt.yticks(yticks)
plt.legend()
plt.show()
