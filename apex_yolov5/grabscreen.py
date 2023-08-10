import io
import os
import time
from datetime import datetime

import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

from apex_yolov5.socket.config import global_config


def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


screen_image = None


def loop_screen(region=None, shot_width=416, shot_height=416):
    global screen_image
    while True:
        screen_image = grab_screen(region=region)
        screen_image = cv2.resize(screen_image, (shot_width, shot_height))


def get_img():
    global screen_image
    temp = screen_image
    screen_image = None
    return temp


def grab_screen_int_array(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return signedIntsArray


last_save_time = time.time()


def save_bitmap_to_file(bitmap, region, aims):
    try:
        global last_save_time
        if time.time() - last_save_time < 1 or len(aims) == 0:
            return
        last_save_time = time.time()
        img = np.frombuffer(bytes(bitmap), dtype='uint8')
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
        img = img.reshape((height, width, 4))
        img0 = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img0 = cv2.resize(img0, (global_config.shot_width, global_config.shot_height))

        # 将位图数据转换为numpy数组

        # 创建一个图像对象
        image = Image.fromarray(img0)

        now = datetime.now()
        # 格式化日期为字符串
        formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 保存图像到文件

        os.makedirs(global_config.auto_save_path + "images/", exist_ok=True)
        os.makedirs(global_config.auto_save_path + "labels/", exist_ok=True)

        # cv2.imwrite(global_config.auto_save_path + "images/" + formatted_date + ".png", img)

        image.save(global_config.auto_save_path + "images/" + formatted_date + ".png", 'PNG')
        with open(global_config.auto_save_path + "labels/" + formatted_date + ".txt", 'w') as f:
            length = len(aims)
            for i in range(length):
                aim = aims[i]
                line = ' '.join(str(x) for x in aim)
                if i != length - 1:
                    f.write(line + '\n')
                else:
                    f.write(line)
    except Exception as e:
        print(e)
        pass
