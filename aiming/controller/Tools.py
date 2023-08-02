import time
import tkinter
from io import BytesIO
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity
from shutil import copyfile


class Tools:
    @staticmethod
    def get_resolution():
        screen = tkinter.Tk()
        xw = screen.winfo_screenwidth()
        yh = screen.winfo_screenheight()
        screen.destroy()
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
