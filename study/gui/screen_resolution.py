from screeninfo import get_monitors

for monitor in get_monitors():
    print(f"Width: {monitor.width}, Height: {monitor.height}")

import win32api

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
print(f"Width: {width}, Height: {height}")