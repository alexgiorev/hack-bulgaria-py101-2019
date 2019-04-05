# you need pyautogui for this

import pyautogui

def gencoord():
    while True:
        yield pyautogui.position()

for x, y in gencoord():
    if x == y == 0:
        print('\a', end='')
