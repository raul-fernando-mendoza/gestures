from win32api import GetSystemMetrics
width = GetSystemMetrics (0)
height = GetSystemMetrics (1)
print(f"Screen resolution = {width} {height}");

import win32gui
import win32api

dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0)
for i in range(0,width):
    win32gui.SetPixel(dc, i, 0, red)  # draw red at 0,0
print("end")