import pickle
import socket
import sys
import threading
import time

import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import get_lock_mode, on_click, on_move, on_press, start
from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket import config


def main():
    # ...or, in a non-blocking fashion:
    listener = pynput.mouse.Listener(
        on_click=on_click, on_move=on_move)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=on_press,
    )
    key_listener.start()

    threading.Thread(target=start).start()

    # 创建一个TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器地址和端口
    server_address = (config.listener_ip, config.listener_port)

    # 连接服务器
    client_socket.connect(server_address)
    buffer_size = config.buffer_size
    try:
        print_count = 0
        compute_time = time.time()
        while True:
            print_count += 1
            img = grab_screen_int_array(region=config.region)
            socket_util.send(client_socket, img, buffer_size=buffer_size)
            mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
            aims = pickle.loads(mouse_data)
            if len(aims) and get_lock_mode():
                lock(aims, config.mouse, config.screen_width, config.screen_height,
                     shot_width=config.shot_width, shot_height=config.shot_height)  # x y 是分辨率
            now = time.time()
            if now - compute_time > 1:
                LogWindow().print_log("一秒识别[{}]次:".format(print_count))
                print_count = 0
                compute_time = now
    finally:
        # 关闭连接
        client_socket.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
