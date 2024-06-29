import ctypes

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover


class FeiMover(MouseMover):
    def __init__(self, mouse_mover_param):
        # 进程内注册插件,模块所在的路径按照实际位置修改
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        self.init_dll()
        self.dll = self.init_dll()
        vid_pid = mouse_mover_param["VID/PID"]
        vid = int(vid_pid[:4], 16)
        pid = int(vid_pid[4:], 16)
        self.hdl = self.dll.M_Open_VidPid(vid, pid)

    def move_rp(self, short_x: int, short_y: int, re_cut_size=0):
        self.dll.M_MoveR(self.hdl, short_x, short_y)

    def move(self, short_x: int, short_y: int):
        self.dll.M_MoveR2(self.hdl, short_x, short_y)

    def left_click(self):
        self.dll.M_LeftClick(self.hdl, 1)

    def click_key(self, value):
        self.dll.M_KeyPress(self.hdl, value, 1)

    def init_dll(self):
        objdll = ctypes.cdll.LoadLibrary(r".\msdk.dll")
        # 定义函数原型
        M_Open = objdll.M_Open
        M_Open.argtypes = [ctypes.c_int]
        M_Open.restype = ctypes.c_void_p

        M_Open_VidPid = objdll.M_Open_VidPid
        M_Open_VidPid.argtypes = [ctypes.c_int, ctypes.c_int]
        M_Open_VidPid.restype = ctypes.c_void_p

        M_KeyPress = objdll.M_KeyPress
        M_KeyPress.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        M_KeyPress.restype = ctypes.c_int

        M_KeyDown = objdll.M_KeyDown
        M_KeyDown.argtypes = [ctypes.c_void_p, ctypes.c_int]
        M_KeyDown.restype = ctypes.c_int

        M_KeyUp = objdll.M_KeyDown
        M_KeyUp.argtypes = [ctypes.c_void_p, ctypes.c_int]
        M_KeyUp.restype = ctypes.c_int

        M_LeftClick = objdll.M_LeftClick
        M_LeftClick.argtypes = [ctypes.c_void_p, ctypes.c_int]
        M_LeftClick.restype = ctypes.c_int

        M_LeftDown = objdll.M_LeftDown
        M_LeftDown.argtypes = [ctypes.c_void_p]
        M_LeftDown.restype = ctypes.c_int

        M_LeftUp = objdll.M_LeftUp
        M_LeftUp.argtypes = [ctypes.c_void_p, ctypes.c_int]
        M_LeftUp.restype = ctypes.c_int

        M_RightClick = objdll.M_RightClick
        M_RightClick.argtypes = [ctypes.c_void_p, ctypes.c_int]
        M_RightClick.restype = ctypes.c_int

        M_RightDown = objdll.M_RightDown
        M_RightDown.argtypes = [ctypes.c_void_p]
        M_RightDown.restype = ctypes.c_int

        M_RightUp = objdll.M_RightUp
        M_RightUp.argtypes = [ctypes.c_void_p]
        M_RightUp.restype = ctypes.c_int

        # 拟人移动
        M_MoveR2 = objdll.M_MoveR2
        M_MoveR2.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        M_MoveR2.restype = ctypes.c_int

        # 无拟人移动
        M_MoveR = objdll.M_MoveR
        M_MoveR.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        M_MoveR.restype = ctypes.c_int

        M_Close = objdll.M_Close
        M_Close.argtypes = [ctypes.c_void_p]
        M_Close.restype = ctypes.c_int
        return objdll
