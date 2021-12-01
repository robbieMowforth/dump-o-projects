from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
#Click-able
#X:  547 Y:  781 RGB: (220,  85,  67)

#Not Click able
#X:  547 Y:  781 RGB: (240,  27,   0)


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01) #Quick Pause
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while keyboard.is_pressed('q') == False:
    if pyautogui.pixel(547,781)[0] == 220 && pyautogui.pixel(547,781)[1] == 85:
        click(547,781)
    else if pyautogui.pixel(547,781)[0] == 240 && pyautogui.pixel(547,781)[1] == 27:
        clickAmount=0
