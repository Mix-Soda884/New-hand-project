import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# データの読み込み
data_x = np.loadtxt("fingdata[1].txt")
data_y = np.loadtxt("fingdata[2].txt")

# データの長さチェック
if len(data_x) != len(data_y):
    raise ValueError("データファイルの長さが一致していません。")

# パラメータ設定
window_size = 30  # 適切なwindow_sizeに変更

# 入力データの整形
X = []
y = []
for i in range(len(data_x) - window_size):
    X.append(data_x[i:i + window_size])  # 過去window_size分のデータを入力に
    y.append(data_y[i + window_size])    # 対応するラベルを出力に

X = np.array(X).reshape(-1, window_size, 1)  # LSTM用に3次元に変形
y = np.array(y)

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ニューラルネットワークのモデル構築
model = Sequential()
model.add(LSTM(64, input_shape=(window_size, 1), activation='relu'))  # LSTM層
model.add(Dense(32, activation='relu'))  # 全結合層
model.add(Dense(1, activation='sigmoid'))  # 出力層（2値分類）

# モデルのコンパイル
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# モデルの学習
history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1)

# 予測した手の開閉状態を「開いている」「閉じている」として出力する
y_pred = model.predict(X_test)
y_pred_labels = np.where(y_pred > 1, "閉じている", "開いている")  

# 平均二乗誤差 (MSE) の評価
mse = mean_squared_error(y_test, y_pred)
print(f"テストデータの平均二乗誤差 (MSE): {mse}")

# 結果の表示
print("手の開閉状態予測:")
for i, state in enumerate(y_pred_labels[:20]):  # 最初の20サンプルを表示
    print(f"サンプル {i+1}: {state}")

# 手の開閉状態を時系列でプロット
plt.figure(figsize=(14, 6))
plt.plot(y_test, label='Actual', marker='o', linestyle='-', color='blue', markersize=3)
plt.plot(y_pred, label='Predicted', marker='x', linestyle='--', color='red', markersize=3)
plt.xlabel('Sample Index')
plt.ylabel('Hand State (0: Open, 1: Closed)')
plt.legend()
plt.title('Actual vs Predicted Hand State')
plt.show()