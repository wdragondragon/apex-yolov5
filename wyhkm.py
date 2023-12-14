# 64位的Python使用64位的无涯键鼠盒子模块
# 本例子使用的无涯键鼠盒子模块是5.00
import win32com.client
from ctypes import *

from apex_yolov5.socket.config import global_config


class TianYaKeyMouseSimulation:
    def __init__(self, id):
        # 进程内注册插件,模块所在的路径按照实际位置修改
        hkmdll = windll.LoadLibrary(".\wyhkm.dll")
        hkmdll.DllInstall.argtypes = (c_long, c_longlong)
        if hkmdll.DllInstall(1, 2) < 0:
            print("注册失败!")
        vid = int(id[:4], 16)
        pid = int(id[4:], 16)
        try:
            self.wyhkm = win32com.client.Dispatch("wyp.hkm")
        except:
            print("创建对象失败!")
        version = self.wyhkm.GetVersion()
        print("无涯键鼠盒子模块版本：" + hex(version))
        DevId = self.wyhkm.SearchDevice(vid, pid, 0)
        if DevId == -1:
            print("未找到无涯键鼠盒子")
        if not self.wyhkm.Open(DevId, 0):
            print("打开无涯键鼠盒子失败")

    def move(self, short_x: int, short_y: int):
        self.wyhkm.MoveRP(short_x, short_y)

    def left_click(self):
        self.wyhkm.LeftClick()


ty = None
device_id = None


def load_ty():
    global ty, device_id
    print("重新加载天涯盒子")
    device_id = global_config.available_mouse_models["ty"]["VID/PID"]
    ty = TianYaKeyMouseSimulation(device_id)
    return ty


def get_ty():
    global ty, device_id
    new_id = global_config.available_mouse_models["ty"]["VID/PID"]
    if ty is None or device_id != new_id:
        ty = load_ty()
    return ty
