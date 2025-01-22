import os
from pylsl import StreamInlet, resolve_stream
import time
import keyboard

print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

time_thres = 1
prev_time = 0
sample, timestamp = inlet.pull_sample()

file_name0 = 'fingdata[6a].txt'
file_name1 = 'fingdata[6b].txt'
file_path0 = os.path.join(file_name0)
file_path1 = os.path.join(file_name1)
numbers0 = sample[0]
numbers1 = sample[1]

with open(file_path0, 'w') as f:
    f.write(f"{numbers0}\n")
with open(file_path1, 'w') as f:
    f.write(f"{numbers1}\n")

while True:

    sample, timestamp = inlet.pull_sample()
    numbers0 = sample[0]
    curr_time = int(round(time.time() * 100)) 
    if ((curr_time - time_thres > prev_time)):
        with open(file_path0, 'a') as f:
            f.write(f"{numbers0}\n")
    numbers1 = sample[1]
    if ((curr_time - time_thres > prev_time)):
        with open(file_path1, 'a') as f:
            f.write(f"{numbers1}\n")
    if keyboard.is_pressed("o"):
        break
