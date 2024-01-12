from ctypes import Structure, c_ulong, byref, windll


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

    def move_rp(self, x: int, y: int):
        """
            鼠标移动，原生移动
        :param x:
        :param y:
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

    def destroy(self):
        """
            销毁
        """
        pass
