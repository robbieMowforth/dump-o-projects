import sounddevice as sd
from numpy import linalg as LA
import numpy as np
import winsound

duration = 100000  # seconds
print(sd.query_devices())
def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    if volume_norm>=100:
        print("LOUD")
        winsound.Beep(2500,100)
    print (int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(duration * 1000)
