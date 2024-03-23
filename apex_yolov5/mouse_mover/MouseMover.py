from ctypes import Structure, c_ulong, byref, windll
import win32api
import win32con


class PointAPI(Structure):
    """
        坐标API结构体
    """
    # PointAPI类型,用于获取鼠标坐标
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


class MouseMover:
    """
        鼠标移动抽象
    """

    def __init__(self, mouse_mover_param):
        self.mouse_mover_param = mouse_mover_param

    def move_rp(self, x: int, y: int, re_cut_size=0):
        """
            鼠标移动，原生移动
        :param x:
        :param y:
        :param re_cut_size:
        """
        pass

    def move(self, x: int, y: int):
        """
            鼠标移动，盒子移动
        :param x:
        :param y:
        """
        pass

    def left_click(self):
        """
            点击按键
        :param button:
        """
        pass

    def get_position(self):
        """
            获取鼠标位置
        """
        po = PointAPI()
        windll.user32.GetCursorPos(byref(po))
        return int(po.x), int(po.y)

    def is_num_locked(self):
        """
            使用ctypes获取键盘状态信息
            0x90 是Num Lock键的虚拟键码
            返回值是一个表示键盘状态的整数，最低位bit为1表示Num Lock被锁定
        :return:
        """
        key_state = windll.user32.GetKeyState(0x90)

        # 判断Num Lock键的状态
        # 第16位是最低位，如果为1表示Num Lock被锁定，否则未锁定
        num_lock_state = key_state & 1

        return num_lock_state == 1

    def is_caps_locked(self):
        """
        使用ctypes获取键盘状态信息
        0x14 是Caps Lock键的虚拟键码
        返回值是一个表示键盘状态的整数，最低位bit为1表示Caps Lock被锁定
        :return:
        """
        key_state = windll.user32.GetKeyState(0x14)

        # 判断Caps Lock键的状态
        # 第16位是最低位，如果为1表示Caps Lock被锁定，否则未锁定
        caps_lock_state = key_state & 1

        return caps_lock_state == 1

    def destroy(self):
        """
            销毁
        """
        pass

    def move_test(self, x: int, y: int):
        self.move_rp(x, y)

    def mouse_click(self, key, press):
        """
            点击鼠标
        :param key:
        :param press:
        """
        if key == "left":
            if press:
                self.left_down()
            else:
                self.left_up()
        elif key == "right":
            if press:
                self.right_down()
            else:
                self.right_up()

    def left_down(self):
        """
            左键按下
        """
        pass

    def left_up(self):
        """
            左键弹起
        """
        pass

    def right_down(self):
        """
            右键按下
        """
        pass

    def right_up(self):
        """
            右键弹起
        """
        pass

    def click_key(self, value):
        """

        :param value:
        :return:
        """
        pass

    def key_down(self, value):
        """
            按下按键
        """
        pass

    def key_up(self, value):
        """
            松开按键
        """
        pass

    def toggle_caps_lock(self, lock_status):
        """
        切换Caps Lock键的状态
        """
        if self.is_caps_locked() ^ lock_status:
            # 模拟按下Caps Lock键
            win32api.keybd_event(win32con.VK_CAPITAL, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
            # 模拟释放Caps Lock键
            win32api.keybd_event(win32con.VK_CAPITAL, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
