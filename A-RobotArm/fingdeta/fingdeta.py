import pandas as pd
import numpy as np
import os

# データの読み込み (非推奨の 'delim_whitespace' の代わりに 'sep="\s+"' を使用)
df1 = pd.read_csv('fingdata[1].txt', sep='\s+', header=None)
df2 = pd.read_csv('fingdata[2].txt', sep='\s+', header=None)

# 読み込んだデータの確認（必要に応じて）
print("Data from fingdata[1].txt:\n", df1.head())
print("Data from fingdata[2].txt:\n", df2.head())

# 数値データへの変換（必要に応じてエラー処理）
df1 = df1.apply(pd.to_numeric, errors='coerce')
df2 = df2.apply(pd.to_numeric, errors='coerce')

# 欠損値を補完または削除
df1.ffill(inplace=True)  # 前方補完
df2.ffill(inplace=True)
df1.dropna(inplace=True)  # 欠損値の削除
df2.dropna(inplace=True)

# 相関の計算
correlation_matrix = df1.corrwith(df2, axis=0)

# 相関結果の出力
print("Correlation between fingdata[1] and fingdata[2]:\n", correlation_matrix)
