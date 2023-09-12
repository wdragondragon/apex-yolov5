# kmbox官方交流群 190702064 by:Ghost 一蓑烟雨 小云
"""
需要修改的是15行和22行，
"""

import ctypes

import win32api

from apex_yolov5.socket.config import global_config


class KeyMouseSimulation():
    # 初始化
    # dll地址
    kmboxA = ctypes.cdll.LoadLibrary(r".\kmbox_dll_64bit.dll")
    kmboxA.KM_init.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
    kmboxA.KM_init.restype = ctypes.c_ushort
    kmboxA.KM_move.argtypes = [ctypes.c_short, ctypes.c_short]
    kmboxA.KM_move.restype = ctypes.c_int

    def __init__(self, id):
        vid = int(id[:4], 16)
        pid = int(id[4:], 16)
        # vid = hex(part1)
        # pid = hex(part2)
        # 连接kmbox_VER a
        ts = KeyMouseSimulation.kmboxA.KM_init(ctypes.c_ushort(vid), ctypes.c_ushort(pid))
        # ts = kmboxA.KM_init(ctypes.c_ushort(0X6688), ctypes.c_ushort(0x2021))
        print("初始化:{}".format(ts))

    # 调用代码
    def perss(self, vk_key: int):
        """
        \n
        键盘指定按键单击函数\n
        输入：    HID键值表\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        注意：由于点击上位机时，电脑焦点在上位机程序里。故键盘的输入\n
        无法直接看到。\n
        \n
        int KM_press(unsigned char vk_key); c++\n
        perss(vk_key); python\n
        """
        # 单击
        KeyMouseSimulation.kmboxA.KM_press(ctypes.c_char(vk_key))

    def down(self, vk_key: int):
        """
        \n
        键盘函数\n
        键盘指定按键一直保持按下 \n
        输入：    HID键值表\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_down(unsigned char vk_key); c++\n
        down(vk_key); python\n
        """
        # 按下
        KeyMouseSimulation.kmboxA.KM_down(ctypes.c_char(vk_key))

    def up(self, vk_key: int):
        """
        \n
        键盘函数\n
        键盘指定按键抬起（配合down函数使用） \n
        输入：    HID键值表\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_up(unsigned char vk_key); c++\n
        up(vk_key); python\n
        """
        # 弹起
        KeyMouseSimulation.kmboxA.KM_up(ctypes.c_char(vk_key))

    def left(self, vk_key: int):
        """
        \n
        鼠标左键控制 0松开 1按下\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_left(unsigned char vk_key); c++\n
        left(vk_key); python\n
        """
        # 左键
        KeyMouseSimulation.kmboxA.KM_left(ctypes.c_char(vk_key))

    def middle(self, vk_key: int):
        """
        \n
        鼠标中键控制 0松开 1按下\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_middle(unsigned char vk_key); c++\n
        middle(vk_key); python\n
        狗斯特发的64位dll有BUG，右键和中键互换\n
        """
        # 中键
        KeyMouseSimulation.kmboxA.KM_right(ctypes.c_char(vk_key))

    def right(self, vk_key: int):
        """
        \n
        鼠标右键控制 0松开 1按下\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_middle(unsigned char vk_key); c++\n
        right(vk_key); python\n
        狗斯特发的64位dll有BUG，右键和中键互换\n
        """
        # 右键
        KeyMouseSimulation.kmboxA.KM_middle(ctypes.c_char(vk_key))

    def move(self, short_x: int, short_y: int):
        """
        \n
        鼠标相对移动\n
        x		:鼠标X轴方向移动距离\n
        y		:鼠标Y轴方向移动距离\n
        返回值：\n
                -1：发送失败\n
                0：发送成功\n
        是否测试：是\n
        测试时间：2022/5/12 by 小云\n
        \n
        int KM_move(short x,short y);\n
        """
        # 移动
        KeyMouseSimulation.kmboxA.KM_move(short_x, short_y)

    def cursor_point(self):
        """
        获取当前鼠标位置
        """
        pos = win32api.GetCursorPos()
        return int(pos[0]), int(pos[1])


# 本页面直接运行简单例子：
# km = KeyMouseSimulation("66882021")  # 实例化模拟键鼠
# km.move(100, 100)
km = None
device_id = None


def load():
    global km, device_id
    print("重新加载kmbox")
    device_id = global_config.available_mouse_models["kmbox"]["VID/PID"]
    km = KeyMouseSimulation(device_id)
    return km


def get():
    global km, device_id
    new_id = global_config.available_mouse_models["kmbox"]["VID/PID"]
    if km is None or device_id != new_id:
        km = load()
    return km
# 其他页面调用运行简单例子：
# import kma
# a=kma.KeyMouseSimulation() # 实例化模拟键鼠
# a.move(100, 100)
