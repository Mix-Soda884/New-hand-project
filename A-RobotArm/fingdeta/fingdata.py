import numpy as np

# ファイルの読み込み
def load_emg_file(file_path):
    data = np.loadtxt(file_path)  # 改行区切りのデータを読み込み
    return data

# 勾配計算（差分）
def calculate_gradient(data):
    return np.gradient(data)

# 勾配の閾値を自動調整
def calculate_dynamic_threshold(grad1, grad2, multiplier=2.0):
    """
    勾配の標準偏差を用いて動的な閾値を計算する。
    multiplier: 標準偏差の何倍を閾値とするか
    """
    std1 = np.std(grad1)
    std2 = np.std(grad2)
    return multiplier * max(std1, std2)  # 両方の信号の中で大きい方を採用

# 状態変化の検出
def detect_state_changes(grad1, grad2, threshold):
    changes = []
    for i in range(len(grad1)):
        if abs(grad1[i]) > threshold and abs(grad2[i]) > threshold:
            if abs(grad1[i]) > abs(grad2[i]):
                changes.append(("閉じる", i))
            else:
                changes.append(("開く", i))
    return changes

# メイン処理
def main():
    # 筋電データのファイルを読み込む
    flexor_data = load_emg_file("fingdata[1].txt")  # 尺側手根屈筋
    extensor_data = load_emg_file("fingdata[2].txt")  # 短橈側手根伸筋

    # 勾配計算
    grad_flexor = calculate_gradient(flexor_data)
    grad_extensor = calculate_gradient(extensor_data)

    # 動的に閾値を計算
    threshold = calculate_dynamic_threshold(grad_flexor, grad_extensor)
    print(f"自動調整された閾値: {threshold:.2f}")

    # 状態変化を検出
    state_changes = detect_state_changes(grad_flexor, grad_extensor, threshold)

    # 結果を表示
    print("検出された状態変化:")
    for state, index in state_changes:
        print(f"時刻 {index}: 手を{state}")

if __name__ == "__main__":
    main()
