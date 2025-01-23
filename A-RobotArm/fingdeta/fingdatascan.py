import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import StandardScaler
import time
import keyboard
from pylsl import StreamInlet, resolve_stream

# === モデルのロード ===
def load_trained_model(model_path):
    model = load_model(model_path)
    return model

# === 筋電データのリアルタイム取得 (LSL) ===
def get_realtime_emg_data(inlet, window_size):
    """
    LSLからリアルタイムで筋電データを取得し、スライディングウィンドウ形式で返す。
    """
    emg_buffer = []  # ウィンドウサイズのデータを保持
    while len(emg_buffer) < window_size:
        sample, timestamp = inlet.pull_sample()
        emg_buffer.append(sample[:2])  # 筋電データの2チャンネルを取得
    
    return np.array(emg_buffer)

# === リアルタイム手の状態予測 ===
def predict_hand_state(model, data, scaler):
    """
    モデルを使って手の状態を予測する。
    """
    # データをスケーリング
    data_scaled = scaler.transform(data)
    
    # モデル入力形式に変換
    data_input = np.expand_dims(data_scaled, axis=0)  # (1, window_size, 2)
    
    # モデルで予測
    prediction = model.predict(data_input)
    return 1 if prediction[0] > 0.5 else 0  # 0: 開く, 1: 閉じる

# === メイン処理 ===
def main():
    # モデルのパス
    model_path = "my_model.h5"
    model = load_trained_model(model_path)
    print("モデルがロードされました。リアルタイム解析を開始します。")
    
    # LSLストリームのセットアップ
    print("LSLストリームを解決中...")
    streams = resolve_stream('type', 'EMG')  # EMGタイプのLSLストリームを解決
    inlet = StreamInlet(streams[0])
    print("LSLストリームが接続されました。")
    
    # 筋電データの読み込み (スケーラー適合用)
    try:
        file1 = np.loadtxt('fingdata[6a].txt')  # 浅指屈筋データ
        file2 = np.loadtxt('fingdata[6b].txt')  # 総指伸筋データ
    except Exception as e:
        print(f"データ読み込みエラー: {e}")
        exit()

    # データ長を短い方に合わせる
    min_length = min(len(file1), len(file2))
    file1, file2 = file1[:min_length], file2[:min_length]
    emg_data_combined = np.stack([file1, file2], axis=-1)  # (N, 2)

    # スケーラーの適合
    scaler = StandardScaler()
    scaler.fit(emg_data_combined)

    # リアルタイム処理パラメータ
    window_size = 5  # スライディングウィンドウサイズ
    file_path0 = "fingdata[1].txt"
    file_path1 = "fingdata[2].txt"
    time_thres = 100  # サンプリング間隔 (ミリ秒)
    prev_time = int(round(time.time() * 100))
    
    try:
        while True:
            # 筋電データを取得
            emg_data = get_realtime_emg_data(inlet, window_size)
            numbers0 = emg_data[:, 0]
            numbers1 = emg_data[:, 1]

            # データをファイルに保存
            curr_time = int(round(time.time() * 100))
            if curr_time - time_thres > prev_time:
                
                # ファイル書き込み
                with open(file_path0, 'a') as f:
                    f.write("\n".join(map(str, numbers0)) + "\n")
                with open(file_path1, 'a') as f:
                    f.write("\n".join(map(str, numbers1)) + "\n")
                
                # タイムスタンプ更新
                prev_time = curr_time

            # 手の状態を予測
            state = predict_hand_state(model, emg_data, scaler)
            if state == 0:
                print(f"手を開いています(state:{numbers0:4f})")
            elif state == 1:
                print(f"手を閉じています(state:{numbers1:4f})")
            
            # キーボード入力で終了
            if keyboard.is_pressed("o"):
                print("リアルタイム解析を終了します。")
                break
            
            # 適切なインターバルを設定 (例: 100ms)
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("処理が中断されました。")
    
if __name__ == "__main__":
    main()
