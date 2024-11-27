import os
import time
import numpy as np
from sklearn.preprocessing import StandardScaler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === パラメータ設定 ===
window_size = 10  # スライディングウィンドウのサイズ
threshold_multiplier = 2.0  # 動的閾値の係数

# === スライディングウィンドウ法で状態を判別 ===
def process_emg_data(file1_path, file2_path):
    try:
        # ファイルの読み込み
        file1 = np.loadtxt(file1_path)
        file2 = np.loadtxt(file2_path)
        
        # データ長を短い方に合わせる
        min_length = min(len(file1), len(file2))
        file1, file2 = file1[:min_length], file2[:min_length]
        
        # データを正規化
        scaler = StandardScaler()
        file1 = scaler.fit_transform(file1.reshape(-1, 1)).flatten()
        file2 = scaler.fit_transform(file2.reshape(-1, 1)).flatten()
        
        # 勾配を計算
        grad1 = np.gradient(file1)
        grad2 = np.gradient(file2)
        grad_diff = grad1 - grad2

        # 動的閾値を計算
        threshold = threshold_multiplier * np.std(grad_diff)

        # スライディングウィンドウ法で状態を判別
        states = []
        for i in range(len(grad_diff) - window_size + 1):
            window = grad_diff[i:i + window_size]
            if np.mean(window) > threshold:
                states.append("閉じている")
            elif np.mean(window) < -threshold:
                states.append("開いている")
            else:
                states.append("不明")
        
        # 結果を出力
        print(f"更新されたファイルの判別結果: {states[-10:]}")  # 最新10状態を表示
    except Exception as e:
        print(f"データ処理中にエラーが発生しました: {e}")

# === ファイル監視用クラス ===
class EMGFileHandler(FileSystemEventHandler):
    def __init__(self, file1_path, file2_path):
        self.file1_path = file1_path
        self.file2_path = file2_path

    def on_modified(self, event):
        if event.src_path in [self.file1_path, self.file2_path]:
            print(f"ファイルが更新されました: {event.src_path}")
            process_emg_data(self.file1_path, self.file2_path)

# === メイン処理 ===
if __name__ == "__main__":
    # 監視するファイルのパスを指定
    file1_path = "fingdata[1].txt"  # 尺側手根屈筋のデータ
    file2_path = "fingdata[2].txt"  # 短橈側手根伸筋のデータ

    # ファイルが存在するか確認
    if not (os.path.exists(file1_path) and os.path.exists(file2_path)):
        print("監視するEMGファイルが見つかりません。ファイルを確認してください。")
        exit()

    # ファイル監視の設定
    event_handler = EMGFileHandler(file1_path, file2_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file1_path) or ".", recursive=False)

    print("監視を開始します...")
    observer.start()

    try:
        while True:
            time.sleep(1)  # プログラムを実行し続ける
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
