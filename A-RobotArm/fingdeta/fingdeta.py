import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from scipy import stats

print(os.getcwd()) 

with open('fingdata[1].txt', 'r') as file:
    lines1 = file.readlines()
lines1 = [line.strip() for line in lines1]

with open('fingdata[2].txt', 'r') as file:
    lines2 = file.readlines()
lines2 = [line.strip() for line in lines2]


data1 = [line.split() for line in lines1]
data2= [line.split() for line in lines2]
print(data1)
print(data2)

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
print(df1)
print(df2)

try:
    df1 = pd.read_csv('fingdata[1].txt')
    df2 = pd.read_csv('fingdata[2].txt')
# dfがNoneになっている場合はエラーメッセージを表示
except FileNotFoundError:
    print("File not found")
except pd.errors.ParserError:
    print("Error parsing the file")

print(df1.isnull().sum())
print(df2.isnull().sum())

df1.ffill(inplace=True)
df2.ffill(inplace=True)
df1.dropna(inplace=True)
df2.dropna(inplace=True)
df1 = df1.apply(pd.to_numeric, errors='coerce')
df2 = df1.apply(pd.to_numeric, errors='coerce')

scaler = StandardScaler()
scaled_data1 = scaler.fit_transform(df1)
scaled_data2 = scaler.fit_transform(df2)



# ピアソン相関行列の計算
correlation_matrix1 = df1.corr(method='pearson')
correlation_matrix2 = df2.corr(method='pearson')

# 各相関ペアのp値を計算
p_values1 = pd.DataFrame(index=df1.columns, columns=df1.columns)
p_values2 = pd.DataFrame(index=df2.columns, columns=df2.columns)

for i in range(len(df1.columns)):
    for j in range(len(df1.columns)):
        if i != j:
            _, p_value = stats.pearsonr(df1.iloc[:, i], df1.iloc[:, j])
            p_values1.iloc[i, j] = p_value

for i in range(len(df2.columns)):
    for j in range(len(df2.columns)):
        if i != j:
            _, p_value = stats.pearsonr(df2.iloc[:, i], df2.iloc[:, j])
            p_values2.iloc[i, j] = p_value

# p値が有意な相関を持つペアを抽出（例として有意水準0.05）
significant_correlations = (p_value < 0.05)

from sklearn.ensemble import RandomForestRegressor

# 説明変数と目的変数を分ける（例として 'target〇' カラムを目的変数に設定）
if 'target1' in df1.columns:
    X1 = df1.drop(columns='target1')
else:
    print("Error: 'target1' column not found in df1")

y1 = df1['target1']
if 'target2' in df1.columns:
    X2 = df2.drop(columns='target2')
else:
    print("Error: 'target2' column not found in df2")
y2 = df2['target2']

model = RandomForestRegressor()
model.fit(X1, y1)
model = RandomForestRegressor()
model.fit(X2, y2)

importances = model.feature_importances_
feature_importance1 = pd.Series(importances, index=X1.columns).sort_values(ascending=False)
feature_importance2 = pd.Series(importances, index=X2.columns).sort_values(ascending=False)
print(feature_importance2)
