import pickle
import socket

import pynput

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5.auxiliary import get_lock_mode, on_click, on_move, on_press
from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.mouse_lock import lock
import config


def main():
    # ...or, in a non-blocking fashion:
    listener = pynput.mouse.Listener(
        on_click=on_click, on_move=on_move)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=on_press,
    )
    key_listener.start()
    # 创建一个TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 服务器地址和端口
    server_address = (config.listener_ip, config.listener_port)

    # 连接服务器
    client_socket.connect(server_address)
    buffer_size = config.buffer_size
    try:
        while True:
            img = grab_screen_int_array(region=config.region)
            socket_util.send(client_socket, img, buffer_size=buffer_size)
            mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
            aims = pickle.loads(mouse_data)
            if len(aims) and get_lock_mode():
                lock(aims, config.mouse, config.screen_width, config.screen_height,
                     shot_width=config.shot_width, shot_height=config.shot_height)  # x y 是分辨率
    finally:
        # 关闭连接
        client_socket.close()


main()
