import sounddevice as sd
from numpy import linalg as LA
import numpy as np
import winsound
import pandas as pd

duration = 7200 # seconds
NAMEEDIT = 'Session7' #CHNAGE HERE
arrayIn = []

print(sd.query_devices()) #tells us about the sound devices
def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print (int(volume_norm))
    arrayIn.append(volume_norm)
    return arrayIn
    
with sd.Stream(callback=print_sound):
    sd.sleep(duration * 1000)
    
    listIn = {NAMEEDIT:arrayIn}

    df = pd.DataFrame(listIn)
    df_csv = pd.read_csv("WithoutMeter.csv")
    df_csv[NAMEEDIT] = df.Session7 #CHANGE HERE
    df_csv.to_csv("WithoutMeter.csv", index=False, mode='w')
    
