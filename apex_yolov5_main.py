import sys
import threading
import time
import traceback

import cv2
import mss
import numpy as np
import pynput.mouse
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from apex_yolov5 import check_run
from apex_yolov5.KeyAndMouseListener import apex_key_listener, apex_mouse_listener
from apex_yolov5.MainWindow import MainWindow
from apex_yolov5.Tools import Tools
from apex_yolov5.auxiliary import get_lock_mode, start
from apex_yolov5.grabscreen import grab_screen_int_array2, save_rescreen_and_aims_to_file
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import model, get_aims


def main():
    sct = mss.mss()
    print_count = 0
    compute_time = time.time()
    while True:
        try:
            # if not Tools.is_apex_windows():
            #     print("不是apex窗口")
            #     time.sleep(1)
            #     continue
            img_origin = grab_screen_int_array2(sct, monitor=global_config.monitor)
            img = np.frombuffer(img_origin.rgb, dtype='uint8')
            img = img.reshape((global_config.monitor["height"], global_config.monitor["width"], 3))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            aims = get_aims(img)
            bboxes = []
            if len(aims):
                if get_lock_mode() and not global_config.only_save:
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
                threading.Thread(target=save_rescreen_and_aims_to_file, args=(img_origin, img, aims)).start()
                print_count = 0
                compute_time = now
            if global_config.is_show_debug_window:
                log_window.set_image(img, bboxes=bboxes)
            if global_config.only_save:
                time.sleep(1)
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass


# main()
if __name__ == "__main__":
    # ...or, in a non-blocking fashion:
    check_run.check()
    listener = pynput.mouse.Listener(
        on_click=apex_mouse_listener.on_click)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    names = model.module.names if hasattr(model, 'module') else model.names

    threading.Thread(target=start).start()

    app = QApplication(sys.argv)
    log_window = MainWindow()

    if global_config.is_show_debug_window:
        # log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        log_window.show()
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
