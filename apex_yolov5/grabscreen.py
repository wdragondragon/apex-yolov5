import io
import os
import time
import traceback
from datetime import datetime

import cv2
import mss
import mss.tools
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import get_aims


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


def grab_screen_int_array2(sct, monitor=None):
    return sct.grab(monitor)


save_sign = False
last_save_time = time.time()
start_save_time = time.time()
start_save_time_format = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
save_has_aim_image_path = "{}images/{}/".format(global_config.auto_save_path, start_save_time_format)
save_has_aim_label_path = "{}labels/{}/".format(global_config.auto_save_path, start_save_time_format)
save_no_aim_image_path = "{}images_no_aim/{}/".format(global_config.auto_save_path, start_save_time_format)
save_no_aim_label_path = "{}labels_no_aim/{}/".format(global_config.auto_save_path, start_save_time_format)
save_count = 0

save_manual_operation_path = "{}labels_manual/{}/".format(global_config.auto_save_path, start_save_time_format)


def save_screen_to_file():
    with mss.mss() as sct:
        screenshot = grab_screen_int_array2(sct=sct, monitor=global_config.auto_save_monitor)
    rgb = screenshot.rgb
    img = np.frombuffer(rgb, dtype='uint8')
    img = img.reshape((global_config.auto_save_monitor["height"], global_config.auto_save_monitor["width"], 3))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    image = Image.fromarray(img)
    now = datetime.now()
    # 格式化日期为字符串
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs(save_manual_operation_path, exist_ok=True)
    image.save(save_manual_operation_path + formatted_date + ".png", 'PNG')


def save_screen_and_aims_save_to_file():
    try:
        global last_save_time, save_sign
        if not global_config.auto_save or time.time() - last_save_time < 3 or save_sign:
            return
        save_sign = True
        last_save_time = time.time()
        with mss.mss() as sct:
            screenshot = grab_screen_int_array2(sct=sct, monitor=global_config.auto_save_monitor)
        rgb = screenshot.rgb
        img = np.frombuffer(rgb, dtype='uint8')
        img = img.reshape((global_config.auto_save_monitor["height"], global_config.auto_save_monitor["width"], 3))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # img0 = cv2.resize(img0, (global_config.imgsz, global_config.imgszy))
        aims = get_aims(img)
        if len(aims) == 0:
            save_image_path = save_no_aim_image_path
            save_label_path = save_no_aim_label_path
        else:
            save_image_path = save_has_aim_image_path
            save_label_path = save_has_aim_label_path
        now = datetime.now()
        # 格式化日期为字符串
        formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
        # 保存图像到文件
        os.makedirs(save_image_path, exist_ok=True)
        os.makedirs(save_label_path, exist_ok=True)

        image = Image.fromarray(img)
        image.save(save_image_path + formatted_date + ".png", 'PNG')
        with open(save_label_path + formatted_date + ".txt", 'w') as f:
            length = len(aims)
            for i in range(length):
                aim = aims[i]
                line = ' '.join(str(x) for x in aim)
                if i != length - 1:
                    f.write(line + '\n')
                else:
                    f.write(line)
        print("save image to file: {}".format(formatted_date))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
    save_sign = False
