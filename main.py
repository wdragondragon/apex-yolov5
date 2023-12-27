import sys
import threading

import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5_main
import apex_yolov5_main_asyn

from apex_yolov5 import check_run, auxiliary
from apex_yolov5.JoyListener import joy_listener
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.circle_window import get_circle_window

from apex_yolov5.config_window import ConfigWindow
from apex_yolov5.socket.config import global_config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    listener = pynput.mouse.Listener(
        on_click=apex_mouse_listener.on_click)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    # names = model.module.names if hasattr(model, 'module') else model.names

    threading.Thread(target=auxiliary.start).start()

    log_window = ConfigWindow(global_config)
    check_run.check(log_window)
    if global_config.show_config:
        log_window.show()

    if global_config.show_circle:
        get_circle_window().show()

    if global_config.joy_move:
        joy_listener.start(log_window)
    if global_config.screenshot_frequency_mode == "asyn":
        threading.Thread(target=apex_yolov5_main_asyn.main).start()
        threading.Thread(target=apex_yolov5_main_asyn.handle, args=(log_window,)).start()
    else:
        threading.Thread(target=apex_yolov5_main.main, args=(log_window,)).start()
    sys.exit(app.exec_())
