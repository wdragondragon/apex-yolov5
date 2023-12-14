from ctypes import windll, Structure, c_ulong, byref

import km_test
import lg
import wyhkm
from apex_yolov5.socket.config import global_config

# API常量
MOUSEEVENTF_LEFTDOWN = 0x2
MOUSEEVENTF_LEFTUP = 0x4
MOUSEEVENTF_MIDDLEDOWN = 0x20
MOUSEEVENTF_MIDDLEUP = 0x40
MOUSEEVENTF_RIGHTDOWN = 0x8
MOUSEEVENTF_RIGHTUP = 0x10
MOUSEEVENTF_MOVE = 0x1

user32 = windll.user32


class PointAPI(Structure):
    # PointAPI类型,用于获取鼠标坐标
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def get_mouse_position():
    po = PointAPI()
    user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def set_mouse_position(x, y):
    if global_config.mouse_model == "kmbox":
        km_test.get().move(x, y)
    elif global_config.mouse_model == "logitech":
        lg.mouse_xy(x, y)
    elif global_config.mouse_model == "ty":
        wyhkm.get_ty().move(x, y)
    else:
        user32.mouse_event(MOUSEEVENTF_MOVE, x, y)


def left_click():
    if global_config.mouse_model == "kmbox":
        km_test.get().right(0)
        km_test.get().right(1)
    elif global_config.mouse_model == "logitech":
        lg.click_mouse_button(1)
    elif global_config.mouse_model == "ty":
        wyhkm.get_ty().left_click()
    else:
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def is_numlock_locked():
    # 使用ctypes获取键盘状态信息
    # 0x90 是Num Lock键的虚拟键码
    # 返回值是一个表示键盘状态的整数，最低位bit为1表示Num Lock被锁定
    key_state = user32.GetKeyState(0x90)

    # 判断Num Lock键的状态
    # 第16位是最低位，如果为1表示Num Lock被锁定，否则未锁定
    num_lock_state = key_state & 1

    return num_lock_state == 1
