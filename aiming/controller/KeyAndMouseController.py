from pynput.keyboard import Controller as KeyController, Key
from pynput.mouse import Controller as MouseController, Button
from ctypes import *

KeyController = KeyController()
MouseController = MouseController()

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
    user32.mouse_event(MOUSEEVENTF_MOVE, x, y, 0, 0)
