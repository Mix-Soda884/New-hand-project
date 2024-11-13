import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# データの読み込み
data_x = np.loadtxt("fingdata[1].txt")
data_y = np.loadtxt("fingdata[2].txt")

# データの長さチェック
if len(data_x) != len(data_y):
    raise ValueError("データファイルの長さが一致していません。")

# 入力データの整形
X = data_x.reshape(-1, 1)  # 2次元配列に変換
y = data_y  # 出力データとして設定

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ニューラルネットワークのモデル構築
model = Sequential([
    Dense(64, input_shape=(1,), activation='relu'),  # 隠れ層1
    Dense(32, activation='relu'),                     # 隠れ層2
    Dense(1)                                          # 出力層
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='mse')

# モデルの学習
history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.1)

# テストデータでの予測
y_pred = model.predict(X_test)

# 平均二乗誤差 (MSE) の評価
mse = mean_squared_error(y_test, y_pred)
print(f"テストデータの平均二乗誤差 (MSE): {mse}")

# 学習曲線の可視化
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.title('Training and Validation Loss over Epochs')
plt.show()
