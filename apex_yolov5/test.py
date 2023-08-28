#
# win32api.SetCursorPos((200, 200))
import time
from ctypes import windll

import win32api
import win32con

# mouse_xy(100,100)
time0 = time.time()
for i in range(199):
    # pydirectinput.moveTo(200,200)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1)
    # mouse_xy(-3,3)
print(time.time() - time0)

user32 = windll.user32
MOUSEEVENTF_MOVE = 0x1


def mouse_to(x, y):
    intention = (x, y)
    print("开始移动，移动距离:{}".format((x, y)))
    while x != 0 or y != 0:
        (x, y) = intention
        move_up = min(1, abs(x)) * (1 if x > 0 else -1)
        move_down = min(1, abs(y)) * (1 if y > 0 else -1)
        if x == 0:
            move_up = 0
        elif y == 0:
            move_down = 0
        x -= move_up
        y -= move_down
        intention = (x, y)
        user32.mouse_event(MOUSEEVENTF_MOVE, int(move_up), int(move_down))
        time.sleep(0.001)


mouse_to(100, 100)
