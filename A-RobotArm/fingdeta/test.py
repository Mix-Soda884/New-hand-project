import numpy as np

data = [0, 1, 4, 9, 16, 7, 2, 13]
# 1次元データ例
segment1 = np.array(data)
threshold = 0
i = 0

# 勾配を計算
grad1 = np.gradient(data)
print("勾配:", grad1)

# 各要素に対して条件を適用
for grad in grad1:
    if grad > threshold:
        print("増えている")
    elif grad < threshold:
        print("減っている")
    else:
        print("不明")
    threshold = grad
    i = i + 1
print(f"データ数{i}")
