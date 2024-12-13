import numpy as np
import matplotlib.pyplot as plt

try:
    file1 = np.loadtxt('fingdata[b1].txt')  # 尺側手根屈筋のデータ
    file2 = np.loadtxt('fingdata[b2].txt')  # 短橈側手根伸筋のデータ
except Exception as e:
    print(f"データ読み込みエラー: {e}")
    exit()

# パラメータ
window_size = 5
gdf1 = 0
gdf2 = 0

# データ格納用
segments1, segments2, grads = [], [], []

for i in range(len(file1) - window_size):

    segment1 = file1[i:i + window_size]
    segment2 = file2[i:i + window_size]
    
    # ウィンドウ内のデータを取得
    grad1 = np.gradient(segment1)
    grad2 = np.gradient(segment2)

    # 特徴量と勾配差の保存
    segments1.append(np.mean(segment1 ** 2))
    segments2.append(np.mean(segment2 ** 2))
    grads.append(np.mean(grad1 - grad2))

# グラフを描画
plt.figure(figsize=(10, 6))

# セグメント1（file1） vs セグメント2（file2）
plt.subplot(3, 1, 1)
plt.plot(segments1, label='Segment1 (file1)', color='blue')
plt.plot(segments2, label='Segment2 (file2)', color='green')
plt.title('Segment Averages')
plt.legend()

# 勾配差
plt.subplot(3, 1, 2)
plt.plot(grads, label='Gradient Difference', color='red')
plt.title('Gradient Difference')
plt.legend()

# 元データ（file1, file2）
plt.subplot(3, 1, 3)
plt.plot(file1, label='Original file1', color='blue', alpha=0.6)
plt.plot(file2, label='Original file2', color='green', alpha=0.6)
plt.title('Original Signals')
plt.legend()

plt.tight_layout()
plt.show()
