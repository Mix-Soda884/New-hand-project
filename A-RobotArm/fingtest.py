import os
from pylsl import StreamInlet, resolve_stream
import pyautogui
import time  
import keyboard

print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

time_thres = 1
prev_time = 0
pinky_thres = .7
pointer_thres = .6
n = 0

save_dir = 'fingdeta'
file_name0 = 'fingdeta[1].txt'
file_name1 = 'fingdeta[2].txt'
file_path0 = os.path.join(save_dir,file_name0)
file_path1 = os.path.join(save_dir,file_name1)

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print(f"ファイルが保存されました: {file_path0}")
print(f"ファイルが保存されました: {file_path1}")
while True:

    sample, timestamp = inlet.pull_sample()
    numbers0 = sample[0]
    curr_time = int(round(time.time() * 10)) 
    if ((curr_time - time_thres > prev_time)):
        with open(file_path0, 'a') as f:
            f.write(f"{numbers0}\n")
    numbers1 = sample[1]
    if ((curr_time - time_thres > prev_time)):
        with open(file_path1, 'a') as f:
            f.write(f"{numbers1}\n")
    if keyboard.is_pressed("o"):
        break



