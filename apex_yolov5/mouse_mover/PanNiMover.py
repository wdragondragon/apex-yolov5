import ctypes
import random
import sys
import time

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover


class PanNiMover(MouseMover):
    def __init__(self, mouse_mover_param):
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        self.dev = None
        self.version = 0
        self.model = 0
        self.vid = 0
        self.pid = 0
        self.wait_respon = False
        if sys.platform == "win32":
            user32 = ctypes.windll.user32
            self.screenX = user32.GetSystemMetrics(78)
            self.screenY = user32.GetSystemMetrics(79)
        else:
            import tkinter
            root = tkinter.Tk()
            self.screenX = root.winfo_vrootwidth()
            self.screenY = root.winfo_vrootheight()
            root.quit()
        vid_pid = mouse_mover_param["VID/PID"]
        vid = int(vid_pid[:4], 16)
        pid = int(vid_pid[4:], 16)
        if not self.OpenDevice(vid, pid):
            print("设备连接失败")
            return
        print("型号:", chr(self.model + 64))
        print("版本:", self.version)
        print("序列号:", self.GetChipID())
        print("空间大小:", self.GetStorageSize())
        self.SetWaitRespon(True)

    def __del__(self):
        self.Close()

    def OpenDevice(self, pid, vid):
        """
            打开默认设备
        :return:
        """
        return self.OpenDeviceByID(pid, vid)

    def OpenDeviceByID(self, vid, pid):
        """
            通过pid vid打开设备
        :param vid:
        :param pid:
        :return:
        """
        dev = HID()
        devices = dev.enum_device()
        vidpid_str = "#vid_{:04x}&pid_{:04x}&".format(vid, pid)
        for device in devices:
            if device.find(vidpid_str) == -1:
                continue
            print("open", device)
            ret = dev.open(device)
            if not ret:
                dev.close()
            else:
                self.dev = dev
                ret = self._getVersion()
                if not ret:
                    continue
                self.version = ret[1]
                self.model = ret[0]
                return True
        return False

    def _getVersion(self):
        self.write_cmd(1)
        return self.read_data_timeout_promise(1, 10)

    def write_cmd(self, cmd, dat=None):
        """

        :param cmd:
        :param dat:
        :return:
        """
        if not self.dev:
            return -1
        if dat and len(dat) > 61:
            return -2
        buf = [32, 1, cmd]
        if dat:
            buf[1] = len(dat) + 1
            buf.extend(dat)
        buf.extend([0xff] * (64 - len(buf)))
        ret = self.dev.write(buf)
        # print(ret)
        if ret < 0:
            self.Close()
        return ret

    def read_data_timeout_promise(self, cmd, timeout=None):
        """

        :param cmd:
        :param timeout:
        :return:
        """
        if not self.dev:
            return None
        for i in range(0, 10):
            ret = self.read_data_timeout(timeout)
            if ret and ret[0] == cmd:
                return ret[1]
        return None

    def read_data_timeout(self, timeout=None):
        """

        :param timeout:
        :return:
        """
        if not self.dev:
            return None
        try:
            ret = self.dev.read(64, timeout)
            if ret and ret[0] == 31:
                return ret[2], ret[3:ret[1] + 2]
            else:
                return None
        except OSError:
            self.Close()
            return None

    def GetChipID(self):
        """

        :return:
        """
        self.write_cmd(12)
        ret = self.read_data_timeout_promise(9, 10)
        if not ret:
            return -1
        result = int.from_bytes(ret, byteorder='little', signed=True)
        result += 113666
        return ctypes.c_int32(result).value

    def GetStorageSize(self):
        """

        :return:
        """
        self.write_cmd(2)
        ret = self.read_data_timeout_promise(2, 10)
        if not ret:
            return -1
        result = int.from_bytes(ret, byteorder='little', signed=True)
        return result

    def SetWaitRespon(self, wait):
        """

        :param wait:
        """
        self.wait_respon = wait
        self.write_cmd(34)
        self.read_data_timeout_promise(39, 10)

    def Close(self):
        """
            关闭盒子
        """
        if self.dev:
            self.dev.close()
            self.dev = None
        self.version = 0
        self.model = 0
        self.vid = 0
        self.pid = 0
        self.wait_respon = False

    def mouse_event(self, e, x=0, y=0, extra1=0, extra2=0):
        """
            鼠标事件
        :param e:
        :param x:
        :param y:
        :param extra1:
        :param extra2:
        :return:
        """
        cmd = [0xff] * 12
        cmd[0] = e
        if e >= 1 and e <= 7:
            pass
        elif e == 8:
            if x < 0:
                x = 0
            if y < 0:
                y = 0

            screenx = self.screenX
            screeny = self.screenY
            if x >= screenx:
                x = screenx - 1
            if y >= screeny:
                y = screeny - 1

            x = int((x << 15) / screenx)
            y = int((y << 15) / screeny)
            cmd[1] = (x >> 8) & 0xff
            cmd[2] = x & 0xff
            cmd[3] = (y >> 8) & 0xff
            cmd[4] = y & 0xff
        elif e == 9:
            if x < -128 or x > 127 or y < -128 or y > 127:
                return
            cmd[1] = x
            cmd[2] = y
        elif e == 91:
            if x < -32768 or x > 32767 or y < -32768 or y > 32767:
                return
            cmd[1] = (x >> 8) & 0xff
            cmd[2] = x & 0xff
            cmd[3] = (y >> 8) & 0xff
            cmd[4] = y & 0xff
        elif e == 10:
            if x < -128 or x > 127:
                return
            cmd[1] = x
        elif e == 11:
            if x < 0:
                x = 0
            if y < 0:
                y = 0

            cmd[1] = (x >> 8) & 0xff
            cmd[2] = x & 0xff
            cmd[3] = (y >> 8) & 0xff
            cmd[4] = y & 0xff
            screenx = self.screenX
            screeny = self.screenY
            cmd[5] = (screenx >> 8) & 0xff
            cmd[6] = screenx & 0xff
            cmd[7] = (screeny >> 8) & 0xff
            cmd[8] = screeny & 0xff
            cmd[9] = extra1
            cmd[10] = extra2
        elif e == 12:
            cmd[1] = (x >> 8) & 0xff
            cmd[2] = x & 0xff
            cmd[3] = (y >> 8) & 0xff
            cmd[4] = y & 0xff
            screenx = self.screenX
            screeny = self.screenY
            cmd[5] = (screenx >> 8) & 0xff
            cmd[6] = screenx & 0xff
            cmd[7] = (screeny >> 8) & 0xff
            cmd[8] = screeny & 0xff
            cmd[9] = extra1
            cmd[10] = extra2
        elif e == 13 or e == 14:
            cmd[1] = x
        self.write_cmd(16, cmd)
        if self.wait_respon:
            self.read_data_timeout_promise(20, 10)

    def key_event(self, e, key):
        """
            键盘事件
        :param e:
        :param key:
        """
        cmd = [e, 0xff]
        if isinstance(key, str):
            key = self.GetScanCodeFromKeyName(key)
        cmd[1] = key
        self.write_cmd(17, cmd)
        if self.wait_respon:
            self.read_data_timeout_promise(20, 10)

    @staticmethod
    def DelayRandom(delay_min, delay_max):
        """

        :param delay_min:
        :param delay_max:
        """
        delay = 0
        if delay_max >= delay_min >= 0 and delay_max > 0:
            delay = random.randint(delay_min, delay_max)
        elif delay_max == 0 and delay_min > 0:
            delay = delay_min
        if delay > 0:
            time.sleep(delay / 1000)

    @staticmethod
    def GetScanCodeFromKeyName(keyname):
        """
            键值表
        :param keyname:
        :return:
        """
        keymap = {
            "a": 4, "b": 5, "c": 6, "d": 7, "e": 8, "f": 9, "g": 10, "h": 11, "i": 12, "j": 13, "k": 14, "l": 15,
            "m": 16, "n": 17, "o": 18, "p": 19, "q": 20,
            "r": 21, "s": 22, "t": 23, "u": 24, "v": 25, "w": 26, "x": 27, "y": 28, "z": 29, "1": 30, "2": 31, "3": 32,
            "4": 33, "5": 34, "6": 35, "7": 36,
            "8": 37, "9": 38, "0": 39, "enter": 40, "esc": 41, "backspace": 42, "tab": 43, "space": 44, " ": 44,
            "空格键": 44, "-": 45, "=": 46, "[": 47, "]": 48,
            "\\": 49, ";": 51, "'": 52, "`": 53, ",": 54, ".": 55, "/": 56, "capslock": 57, "f1": 58, "f2": 59,
            "f3": 60, "f4": 61, "f5": 62, "f6": 63, "f7": 64,
            "f8": 65, "f9": 66, "f10": 67, "f11": 68, "f12": 69, "printscreen": 70, "scrolllock": 71, "pause": 72,
            "break": 72, "insert": 73, "home": 74,
            "pageup": 75, "delete": 76, "end": 77, "pagedown": 78, "right": 79, "left": 80, "down": 81, "up": 82,
            "numlock": 83, "小键盘/": 84, "小键盘*": 85,
            "小键盘-": 86, "小键盘+": 87, "小键盘enter": 88, "小键盘1": 89, "小键盘2": 90, "小键盘3": 91, "小键盘4": 92,
            "小键盘5": 93, "小键盘6": 94,
            "小键盘7": 95, "小键盘8": 96, "小键盘9": 97, "小键盘0": 98, "小键盘.": 99, "menu": 101, "小键盘=": 103,
            "静音": 127, "音量加": 128, "音量减": 129,
            "lctrl": 224, "lshift": 225, "lalt": 226, "lwin": 227, "rctrl": 228, "rshift": 229, "ralt": 230,
            "rwin": 231,
            "ctrl": 224, "shift": 225, "alt": 226, "win": 227
        }
        keyname = keyname.lower()
        if keyname in keymap:
            return keymap[keyname]
        else:
            return 0

    def move_rp(self, x: int, y: int, re_cut_size=0):
        self.mouse_event(91, x, y)

    def move(self, x: int, y: int):
        move_max = max(x, y)
        if move_max == 0:
            return
        move_max = min(255, move_max)
        self.mouse_event(12, x, y, 1, move_max)

    def left_click(self):
        self.left_down()
        self.DelayRandom(0, 50)
        self.left_up()

    def mouse_click(self, key, press):
        print("未实现 mouse_click")

    def left_down(self):
        self.mouse_event(1)

    def left_up(self):
        self.mouse_event(2)

    def right_down(self):
        self.mouse_event(3)

    def right_up(self):
        self.mouse_event(4)

    def click_key(self, value):
        self.key_down(value)
        self.DelayRandom(0, 20)
        self.key_up(value)

    def key_down(self, value):
        self.key_event(1, value)

    def key_up(self, value):
        self.key_event(2, value)


# -*- coding: utf-8 -*-

from ctypes import *
import platform


class GUID(Structure):
    _fields_ = [("Data1", c_ulong),
                ("Data2", c_ushort),
                ("Data3", c_ushort),
                ("Data4", c_ubyte * 8)]


class SP_DEVICE_INTERFACE_DATA(Structure):
    _fields_ = [("cbSize", c_ulong),
                ("InterfaceClassGuid", GUID),
                ("Flags", c_ulong),
                ("Reserved", c_ulong)]


def SP_DATA_A_factory(length):
    class SP_DEVICE_INTERFACE_DETAIL_DATA_A(Structure):
        _fields_ = [("cbSize", c_ulong), ("DevicePath", c_char * (length - 4))]

    return SP_DEVICE_INTERFACE_DETAIL_DATA_A


class HID:
    """

    """

    def __init__(self):
        self.setupapi_dll = WinDLL("setupapi.dll")
        info_value = [c_ulong(0x4d1e55b2), c_ushort(0xf16f), c_ushort(0x11cf),
                      (c_ubyte * 8)(0x88, 0xcb, 0x00, 0x11, 0x11, 0x00, 0x00, 0x30)]
        self.InterfaceClassGuid = GUID(*info_value)
        self.handle = None
        self.setupapi_dll.SetupDiGetClassDevsA.restype = c_void_p
        self.setupapi_dll.SetupDiEnumDeviceInterfaces.argtypes = (
            c_void_p, c_void_p, POINTER(GUID), c_ulong, POINTER(SP_DEVICE_INTERFACE_DATA))

    def __del__(self):
        self.close()

    def enum_device(self):
        """

        :return:
        """
        result = []
        device_info_set = self.setupapi_dll.SetupDiGetClassDevsA(pointer(self.InterfaceClassGuid), None, None, 0x12)
        if device_info_set != -1:
            # print(device_info_set)
            device_index = 0
            while True:
                if platform.architecture()[0] == "64bit":
                    info_value = [c_ulong(32), self.InterfaceClassGuid, 0, 0]
                else:
                    info_value = [c_ulong(28), self.InterfaceClassGuid, 0, 0]
                device_interface_data = SP_DEVICE_INTERFACE_DATA(*info_value)
                ret = self.setupapi_dll.SetupDiEnumDeviceInterfaces(device_info_set, None,
                                                                    pointer(self.InterfaceClassGuid), device_index,
                                                                    byref(device_interface_data))
                if not ret:
                    err = GetLastError()
                    if err != 259:
                        print("SetupDiEnumDeviceInterfaces return:", err)
                    break
                required_size = c_ulong(0)
                SP_DATA_A = SP_DATA_A_factory(8)
                self.setupapi_dll.SetupDiGetDeviceInterfaceDetailA.argtypes = (
                    c_void_p, POINTER(SP_DEVICE_INTERFACE_DATA), POINTER(SP_DATA_A), c_ulong, POINTER(c_ulong),
                    c_void_p)
                ret = self.setupapi_dll.SetupDiGetDeviceInterfaceDetailA(device_info_set,
                                                                         pointer(device_interface_data), None, 0,
                                                                         byref(required_size), None)
                # print(required_size.value)
                SP_DATA_A = SP_DATA_A_factory(required_size.value)
                self.setupapi_dll.SetupDiGetDeviceInterfaceDetailA.argtypes = (
                    c_void_p, POINTER(SP_DEVICE_INTERFACE_DATA), POINTER(SP_DATA_A), c_ulong, POINTER(c_ulong),
                    c_void_p)
                if platform.architecture()[0] == "64bit":
                    device_interface_detail_data = SP_DATA_A(*[8, b''])
                else:
                    device_interface_detail_data = SP_DATA_A(*[5, b''])
                ret = self.setupapi_dll.SetupDiGetDeviceInterfaceDetailA(device_info_set,
                                                                         pointer(device_interface_data),
                                                                         byref(device_interface_detail_data),
                                                                         required_size, None, None)
                # print(ret)
                if ret:
                    # print(device_interface_detail_data.DevicePath)
                    device_path = device_interface_detail_data.DevicePath.decode("gbk")
                    # print(device_path)
                    if device_path.find("pid") != -1:
                        # print(device_path)
                        if device_path.find("&mi_00#") != -1:
                            result.append(device_path)
                else:
                    print("SetupDiGetDeviceInterfaceDetailA return:", GetLastError())
                device_index += 1
        return result

    def open(self, path):
        """

        :param path:
        :return:
        """
        handle = windll.kernel32.CreateFileA(c_char_p(bytes(path, "gbk")), 0xc0000000, 3, None, 3, 0x00000080, 0)
        if handle == -1:
            return False
        self.handle = handle
        return True

    def close(self):
        """

        """
        if self.handle:
            windll.kernel32.CancelIo(self.handle)
            windll.kernel32.CloseHandle(self.handle)
            self.handle = None

    def write(self, data):
        """

        :param data:
        :return:
        """
        if self.handle == -1:
            return -1
        length = len(data)
        buf = bytearray(data)
        ret = windll.kernel32.WriteFile(self.handle, c_char_p(bytes(buf)), length, None, None)
        return ret

    def read(self, len, timeout):
        """

        :param len:
        :param timeout:
        :return:
        """
        if self.handle == -1:
            return -1
        buf = create_string_buffer(len)
        bytes_read = c_ulong(0)
        ret = windll.kernel32.ReadFile(self.handle, buf, len, byref(bytes_read), None)
        if ret:
            return bytes(buf)
        else:
            return None
