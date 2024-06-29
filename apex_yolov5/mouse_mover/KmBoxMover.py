import ctypes

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover


class KmBoxMover(MouseMover):

    def __init__(self, mouse_mover_param):
        # 初始化
        # dll地址
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        vid_pid = mouse_mover_param["VID/PID"]
        self.km_box_A = ctypes.cdll.LoadLibrary(r".\kmbox_dll_64bit.dll")
        self.km_box_A.KM_init.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
        self.km_box_A.KM_init.restype = ctypes.c_ushort
        self.km_box_A.KM_move.argtypes = [ctypes.c_short, ctypes.c_short]
        self.km_box_A.KM_move.restype = ctypes.c_int
        vid = int(vid_pid[:4], 16)
        pid = int(vid_pid[4:], 16)
        # 连接km_box_VER a
        ts = self.km_box_A.KM_init(ctypes.c_ushort(vid), ctypes.c_ushort(pid))
        self.logger.print_log("初始化:{}".format(ts))

    def left_click(self):
        # 左键
        self.left(1)
        self.left(0)

    def left(self, vk_key: int):
        """
            鼠标左键控制 0松开 1按下
        """
        # 左键
        self.km_box_A.KM_left(ctypes.c_char(vk_key))

    def move_rp(self, short_x: int, short_y: int, re_cut_size=0):
        self.move(short_x, short_y)

    def move(self, short_x: int, short_y: int):
        """
        鼠标相对移动
        x		:鼠标X轴方向移动距离
        y		:鼠标Y轴方向移动距离
        返回值：
                -1：发送失败\n
                0：发送成功\n
        """
        self.km_box_A.KM_move(short_x, short_y)
