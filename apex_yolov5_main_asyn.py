import time
import traceback

import cv2
import mss
import numpy as np

from apex_yolov5.grabscreen import grab_screen_int_array2, save_rescreen_and_aims_to_file_with_thread
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import get_aims
from client_mult import GetBlockQueue

screen_count = 0
image_block_queue = GetBlockQueue("image_queue", maxsize=1)
def handle(log_window):
    global screen_count
    print_count = 0
    compute_time = time.time()
    while True:
        try:
            data = image_block_queue.get()
            img = data["img"]
            img_origin = data["img_origin"]
            aims = get_aims(img)
            bboxes = []
            if len(aims):
                if not global_config.only_save:
                    lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                         shot_width=global_config.shot_width,
                         shot_height=global_config.shot_height)  # x y 是分辨率
                if global_config.is_show_debug_window:
                    for i, det in enumerate(aims):
                        tag, x_center, y_center, width, height = det
                        x_center, width = global_config.shot_width * float(
                            x_center), global_config.shot_width * float(
                            width)
                        y_center, height = global_config.shot_height * float(
                            y_center), global_config.shot_height * float(
                            height)
                        top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                        bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                        bboxes.append((tag, top_left, bottom_right))
            print_count += 1
            now = time.time()
            if now - compute_time > 1:
                image_text = "一秒识别[{}]次:".format(print_count)
                print(image_text)
                image_text = "一秒截图[{}]次:".format(screen_count)
                print(image_text)
                log_window.update_frame_rate_plot_2(screen_count)
                log_window.update_frame_rate_plot(print_count)
                if global_config.auto_save:
                    save_rescreen_and_aims_to_file_with_thread(img_origin, img, aims)
                print_count = 0
                screen_count = 0
                compute_time = now
            if global_config.is_show_debug_window:
                log_window.set_image(img, bboxes=bboxes)
            if global_config.only_save:
                time.sleep(1)
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass


def main():
    global screen_count
    sct = mss.mss()
    while True:
        try:
            img_origin = grab_screen_int_array2(sct, monitor=global_config.monitor)
            img = np.frombuffer(img_origin.rgb, dtype='uint8')
            img = img.reshape((global_config.monitor["height"], global_config.monitor["width"], 3))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            image_block_queue.put({"img": img, "img_origin": img_origin})
            screen_count += 1
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass