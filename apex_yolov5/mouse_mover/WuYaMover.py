from ctypes import *

import win32com.client

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover


class WuYaMover(MouseMover):
    def __init__(self, mouse_mover_param):
        # 进程内注册插件,模块所在的路径按照实际位置修改
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        vid_pid = mouse_mover_param["VID/PID"]
        hkm_dll = windll.LoadLibrary(".\wy_hkm.dll")
        hkm_dll.DllInstall.argtypes = (c_long, c_longlong)
        if hkm_dll.DllInstall(1, 2) < 0:
            self.logger.print_log("注册失败!")
        vid = int(vid_pid[:4], 16)
        pid = int(vid_pid[4:], 16)
        try:
            self.wy_hkm = win32com.client.Dispatch("wyp.hkm")
        except Exception as e:
            self.logger.print_log("创建对象失败!")
            print(e)
        version = self.wy_hkm.GetVersion()
        self.logger.print_log("无涯键鼠盒子模块版本：" + hex(version))
        dev_id = self.wy_hkm.SearchDevice(vid, pid, 0)
        if dev_id == -1:
            self.logger.print_log("未找到无涯键鼠盒子")
        if not self.wy_hkm.Open(dev_id, 0):
            self.logger.print_log("打开无涯键鼠盒子失败")

    def move_rp(self, short_x: int, short_y: int, re_cut_size=0):
        self.wy_hkm.MoveRP(short_x, short_y)

    def move(self, short_x: int, short_y: int):
        self.wy_hkm.MoveR(short_x, short_y)

    def left_click(self):
        self.wy_hkm.LeftClick()
