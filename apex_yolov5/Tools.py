import ctypes
import os
import time
from io import BytesIO
from shutil import copyfile

import cv2
import numpy as np
import win32gui
from skimage.metrics import structural_similarity


class Tools:
    @staticmethod
    def get_resolution():
        # screen = tkinter.Tk()
        # xw = screen.winfo_screenwidth()
        # yh = screen.winfo_screenheight()
        # screen.destroy()

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware(2)
        [xw, yh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        return xw, yh

    @staticmethod
    def compare_image(img, path_image):
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        image_a = cv2.imdecode(np.frombuffer(buffer.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
        buffer.close()
        image_b = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(gray_a, gray_b, full=True)
        return score

    @staticmethod
    def current_milli_time():
        return int(round(time.time() * 1000))

    @staticmethod
    def copy_file(source_path, target_path):
        op = os.path
        if isinstance(source_path, str):
            if op.exists(source_path):
                copyfile(source_path, target_path)
            else:
                print("源文件不存在")

    @staticmethod
    def is_apex_windows():
        window_handle = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(window_handle)
        return window_title == 'Apex Legends'
