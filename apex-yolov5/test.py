
#
# win32api.SetCursorPos((200, 200))
import time

import win32api
import win32con

#mouse_xy(100,100)
time0 = time.time()
for i in range(199):
    #pydirectinput.moveTo(200,200)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1,1)
    #mouse_xy(-3,3)
print(time.time()-time0)



