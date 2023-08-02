import pynput, win32con
# import pydirectinput
import win32api

lock_tag = '0'


def mouse_To1(des_X, des_Y, current_mouse_x=0, current_mouse_y=0):
    up = des_X - current_mouse_x
    down = des_Y - current_mouse_y
    up = int(up)
    down = int(down)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, up, down)


def set_mouse_position(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)


def lock(aims, mouse, screen_width, screen_height, shot_width, shot_height):
    min_score = -1
    min_aim = {}
    if not len(aims):
        return
    for aim in aims:
        x1 = aim["x1"]
        x2 = aim["x2"]
        y1 = aim["y1"]
        y2 = aim["y2"]
        x = x1 - x2
        y = y1 - y2
        temp = x ^ 2 + y ^ 2
        if min_score == -1 or min_score > temp:
            min_score = temp
            min_aim = aim
    x1 = min_aim["x1"]
    x2 = min_aim["x2"]
    y1 = min_aim["y1"]
    y2 = min_aim["y2"]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    mid_x = screen_width / 2
    mid_y = screen_height / 2
    targetRealX = shot_width / 2 - x
    targetRealY = screen_height / 2 - y
    print("move to {} ,{}".format(targetRealX, targetRealY))
    set_mouse_position(targetRealX, targetRealY)
