#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import win32gui
import win32ui
import win32con
import win32api

hdesktop = win32.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

desktop_dc = win32gui.GetWindowDC(hdesktop) # Create device context
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create memory based device context
mem_dc = img_dc.CreateCompatibleDC()

# create bitmap object

screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy screen to our memory device context
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# save bitmap to file
screenshot.SaveBitmapFile(mem_dc, "screenshot.bmp")

# free our objects
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
