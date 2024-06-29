import time
import traceback

import cv2
import mss
import numpy as np

from apex_yolov5 import global_img_info
from apex_yolov5.auxiliary import get_lock_mode
from apex_yolov5.grabscreen import grab_screen_int_array2, save_rescreen_and_aims_to_file_with_thread
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import get_aims
from apex_yolov5.windows.aim_show_window import get_aim_show_window


def main(log_window):
    screen_count = 0
    sct = mss.mss()
    print_count = 0
    compute_time = time.time()
    last_status = False
    while True:
        try:
            if not global_config.ai_toggle or not get_lock_mode():
                time.sleep(0.006)
                run_time = time.time() - compute_time
                if last_status and run_time < 1:
                    log_window.add_frame_rate_plot((int(print_count / run_time), int(screen_count / run_time)))
                last_status = False
                continue
            else:
                if not last_status:
                    compute_time = time.time()
                    print_count = 0
                    screen_count = 0
                last_status = True

            img_origin = grab_screen_int_array2(sct, monitor=global_config.monitor)
            img = np.frombuffer(img_origin.rgb, dtype='uint8')
            img = img.reshape((global_config.monitor["height"], global_config.monitor["width"], 3))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            global_img_info.set_current_img(img_origin, img)
            aims = get_aims(img)
            bboxes = []
            averager = (0, 0, 0, 0)
            if len(aims):
                if not global_config.only_save:
                    averager = lock(aims, global_config.mouse, global_config.desktop_width,
                                    global_config.desktop_height,
                                    shot_width=global_img_info.get_current_img().shot_width,
                                    shot_height=global_img_info.get_current_img().shot_height)  # x y 是分辨率
                if global_config.is_show_debug_window:
                    for i, det in enumerate(aims):
                        tag, x_center, y_center, width, height = det
                        x_center, width = global_img_info.get_current_img().shot_width * float(
                            x_center), global_img_info.get_current_img().shot_width * float(
                            width)
                        y_center, height = global_img_info.get_current_img().shot_height * float(
                            y_center), global_img_info.get_current_img().shot_height * float(
                            height)
                        top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                        bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                        bboxes.append((tag, top_left, bottom_right))
            else:
                if global_config.show_aim:
                    get_aim_show_window().clear_box()
            print_count += 1
            screen_count += 1
            now = time.time()
            if now - compute_time > 1:
                log_window.add_frame_rate_plot((print_count, screen_count))
                if global_config.auto_save:
                    save_rescreen_and_aims_to_file_with_thread(img_origin, img, aims)
                print_count = 0
                screen_count = 0
                compute_time = now
            if global_config.is_show_debug_window:
                log_window.set_image(img, bboxes=bboxes)
            if global_config.only_save:
                time.sleep(1)
            global_config.sign_shot_xy(averager)
            global_config.change_shot_xy()
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
