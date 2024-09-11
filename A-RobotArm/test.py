from re import S
import Adeept
import time
import keyboard
from pylsl import StreamInlet, resolve_stream

global thread_flag
thread_flag = 1

q = 45
w = 93
e = 180
r = 90
t = 65
##起動時の初期数値

Adeept.com_init('COM5',115200,1)
Adeept.wiat_connect()

############cut-off rule#################

Adeept.three_function("'servo_attach'",0,9)
Adeept.three_function("'servo_attach'",1,6)
Adeept.three_function("'servo_attach'",2,5)
Adeept.three_function("'servo_attach'",3,3)
Adeept.three_function("'servo_attach'",4,11)

Adeept.three_function("'servo_write'",0,q)
Adeept.three_function("'servo_write'",1,w)
Adeept.three_function("'servo_write'",2,e)
Adeept.three_function("'servo_write'",3,r)
Adeept.three_function("'servo_write'",4,t)
##初期位置を呼び出す

print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

time_thres = 100
prev_time = 0
pinky_thres = .95
arm_pick = .95
"""pointer_thres = .6"""

while True:
    
    sample, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp
    curr_time = int(round(time.time() * 1000)) # get current time in milliseconds
    if ((curr_time - time_thres > prev_time)):  # if an EMG peak from channel 1 is detected and enough time has gone by since the last one, press key
        prev_time = curr_time # update time
        if(sample[0] >=  pinky_thres): 
            t = t - 5
            if (t >= 45):
                Adeept.three_function("'servo_write'",4,t)
            else:
                t = 45
        else:
            t = t + 10
            if (t <= 135):
                Adeept.three_function("'servo_write'",4,t)
            else:
                t = 135
        if(sample[1] >=  arm_pick): 
            w = w - 5
            if (w >= 0):
                Adeept.three_function("'servo_write'",1,w)
            else:
                w = 0
        if(sample[2] >= arm_pick):
            w = w + 5
            if (w <= 180):
                Adeept.three_function("'servo_write'",1,w)
            else:
                w = 180

    if keyboard.is_pressed("o"):
        break

"""
    elif ((sample[1] >=  pointer_thres) & (curr_time - time_thres > prev_time)):  # if an EMG peak from channel 2 is detected from and enough time has gone by since the last one, press key
    		prev_time = curr_time # update time 
    		pyautogui.press('p')
            
    elif ((sample[2] >=  pointer_thres) & (curr_time - time_thres > prev_time)):  # if an EMG peak from channel 3 is detected and enough time has gone by since the last one, press key
    		prev_time = curr_time # update time 
    		pyautogui.press('o')
            
    elif ((sample[3] >=  pinky_thres) & (curr_time - time_thres > prev_time)):  # if an EMG peak from channel 4 is detected and enough time has gone by since the last one, press key
    		prev_time = curr_time # update time 
    		pyautogui.press('i')
"""

"""
    if keyboard.is_pressed("a"):
        q = q + 0.25
        if (q <= 180):
            Adeept.three_function("'servo_write'",0,q)
        else:
            q = 180
    if keyboard.is_pressed("w"):
        w = w + 0.25
        if (w <= 180):
            Adeept.three_function("'servo_write'",1,w)
        else:
            w = 180
    if keyboard.is_pressed("k"):
        e = e + 0.25
        if (e <= 360):
            Adeept.three_function("'servo_write'",2,e)
        else:
            e = 360
    if keyboard.is_pressed("q"):
        r = r + 0.25
        if (r <= 180):
            Adeept.three_function("'servo_write'",3,r)
        else:
            r = 180
    if keyboard.is_pressed("x"):
        t = t + 0.50
        if (t <= 135):
            Adeept.three_function("'servo_write'",4,t)
        else:
            t = 135

    t = t - 0.25
    if (t >= 45):
        Adeept.three_function("'servo_write'",4,t)
    else:
        t = 45
    
    if keyboard.is_pressed("d"):
        q = q - 0.25
        if (q >= 0):
            Adeept.three_function("'servo_write'",0,q)
        else:
            q = 0
    if keyboard.is_pressed("s"):
        w = w - 0.25
        if (w >= 0):
            Adeept.three_function("'servo_write'",1,w)
        else:
            w = 0
    if keyboard.is_pressed("i"):
        e = e - 0.25
        if (e >= 0):
            Adeept.three_function("'servo_write'",2,e)
        else:
            e = 0
    if keyboard.is_pressed("e"):
        r = r - 0.25
        if (r >= 0):
            Adeept.three_function("'servo_write'",3,r)
        else:
            r = 0
"""