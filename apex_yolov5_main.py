import time
import traceback

import cv2
import mss
import numpy as np

from apex_yolov5 import global_img_info
from apex_yolov5.grabscreen import grab_screen_int_array2
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import get_aims


def main(log_window):
    screen_count = 0
    sct = mss.mss()
    print_count = 0
    while True:
        try:
            if not global_config.ai_toggle:
                time.sleep(6)
                continue
            img_origin = grab_screen_int_array2(sct, monitor=global_config.monitor)
            img = np.frombuffer(img_origin.rgb, dtype='uint8')
            img = img.reshape((global_config.monitor["height"], global_config.monitor["width"], 3))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            global_img_info.set_current_img(img_origin, img)
            aims = get_aims(img)
            if len(aims):
                if not global_config.only_save:
                    lock(aims, global_config.mouse, global_config.desktop_width, global_config.desktop_height,
                         shot_width=global_img_info.get_current_img().shot_width,
                         shot_height=global_img_info.get_current_img().shot_height)  # x y 是分辨率
            print_count += 1
            screen_count += 1
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
