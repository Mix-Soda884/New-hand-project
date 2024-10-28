import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# データの読み込み
x = np.loadtxt("fingdata[1].txt")
y = np.loadtxt("fingdata[2].txt")

print("xのデータ:", x)
print("yのデータ:", y)

# エラーチェック：xとyのデータの長さを確認
if len(x) != len(y):
    raise ValueError("xとyのデータの長さが一致していません。同じ長さのデータを使用してください。")

# xを2次元配列に変換
X = x.reshape(-1, 1)  # 線形回帰では2次元配列が必要

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルのインスタンスを作成し、学習
model = LinearRegression()
model.fit(X_train, y_train)

# 予測と評価
y_pred = model.predict(X_test)

# 平均二乗誤差と決定係数の計算
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"平均二乗誤差 (MSE): {mse}")
print(f"決定係数 (R2スコア): {r2}")

# 結果の可視化
plt.scatter(y_test, y_pred)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.title("True vs Predicted Values")
plt.show()
