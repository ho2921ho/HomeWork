import win32api
import win32con


pos = win32api.GetCursorPos() # 현재 마우스의 좌표

win32api.SetCursorPos(pos) # 좌표로 이동


def mouse_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


mouse_click(300, 300) # 좌표 클릭.

import wx
import time

def chapter(x,y,location,width,height):
    app = wx.App()
    time.sleep(4)
    screen = wx.ScreenDC()
    bmp = wx.Bitmap(width,height) # 캠처될 해상도
    
    mem = wx.MemoryDC(bmp)
    mem.Blit(0,0,1600,900,screen,x,y) # 마지막 두개가 중요! 캡쳐할 화면의 왼쪽 위의 모서리 좌표. 
    del mem
    
    now = time.localtime()
    time_ = "%04d-%02d-%02d-%02dh-%02dm-%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    
    saveas="{}{}".format(time_,'.bmp')
    
    bmp.SaveFile(location + '/' + saveas,wx.BITMAP_TYPE_BMP)


pos_list = [(250,250),(350,250),(450,250),(550,250),(700,250),(250,350),(350,350),(450,350)]

for pos in pos_list:
    mouse_click(*pos)
    mouse_click(*pos)
    location = 'C:/GitHub/HomeWork/Time_series/final_paper/그림/season'
    chapter(560,420,location,480,100)
    mouse_click(1560,15)
    time.sleep(2)
    
for pos in pos_list:
    mouse_click(*pos)
    mouse_click(*pos)
    location = 'C:/GitHub/HomeWork/Time_series/final_paper/그림/trend'
    chapter(560,330,location,480,100)
    mouse_click(1560,15)
    time.sleep(2)
    
for pos in pos_list:
    mouse_click(*pos)
    mouse_click(*pos)
    location = 'C:/GitHub/HomeWork/Time_series/final_paper/그림/observed'
    chapter(560,235,location,480,100)
    mouse_click(1560,15)
    time.sleep(2)
    
for pos in pos_list:
    mouse_click(*pos)
    mouse_click(*pos)
    location = 'C:/GitHub/HomeWork/Time_series/final_paper/그림/random'
    chapter(560,515,location,480,100)
    mouse_click(1560,15)
    time.sleep(2)