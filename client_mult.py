import pickle
import queue
import socket
import sys
import threading
import time

import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5 import LogUtil
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import get_lock_mode, start
from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config


class GetBlockQueue:
    def __init__(self, maxsize=1):
        self.lock = threading.Lock()
        self.queue = queue.Queue(maxsize=maxsize)

    def get(self):
        return self.queue.get()

    def put(self, data):
        if self.queue.full():
            self.queue.get()
        self.queue.put(data)


def socket_start():
    while True:
        try:
            # ...or, in a non-blocking fashion:
            # 创建一个TCP/IP套接字
            listener_ports = global_config.listener_ports
            for listener_port in listener_ports:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # 服务器地址和端口
                server_address = (global_config.listener_ip, listener_port)
                # 连接服务器
                client_socket.connect(server_address)
                client_socket_list.append(client_socket)
                usable_client_socket.put(client_socket)
            try:
                while True:
                    t0 = time.time()
                    img = grab_screen_int_array(region=global_config.region)
                    LogUtil.set_time("截图", time.time() - t0)
                    image_block_queue.put(img)
            except:
                pass
            finally:
                # 关闭连接
                for client_socket in client_socket_list:
                    client_socket.close()
        except:
            pass
        finally:
            time.sleep(1)
            LogWindow().print_log("连接断开，等待重连...")
            pass


def consumption_picture():
    while True:
        client_socket = usable_client_socket.get()
        img = image_block_queue.get()
        threading.Thread(target=asyn_compute_picture, args=(client_socket, img)).start()


def asyn_compute_picture(client_socket, img):
    send_start_time = time.time()
    socket_util.send(client_socket, img, buffer_size=buffer_size)
    mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
    recv_mouse_end_time = time.time()
    if send_start_time > last_recv_mouse_data["send_time"]:
        last_recv_mouse_data["send_time"] = send_start_time
        last_recv_mouse_data["recv_time"] = recv_mouse_end_time
        last_recv_mouse_data["mouse_data"] = mouse_data
        mouse_block_queue.put(mouse_data)
    usable_client_socket.put(client_socket)
    return mouse_data


def consumption_mouse_data():
    print_count = 0
    compute_time = time.time()
    while True:
        mouse_data = mouse_block_queue.get()
        print_count += 1
        aims = pickle.loads(mouse_data)
        if len(aims) and get_lock_mode():
            lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                 shot_width=global_config.shot_width, shot_height=global_config.shot_height)  # x y 是分辨率
        now = time.time()
        if now - compute_time > 1:
            LogWindow().print_log("一秒移动[{}]次:".format(print_count))
            print_count = 0
            compute_time = now


if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    if global_config.is_show_debug_window:
        log_window.show()

    listener = pynput.mouse.Listener(
        on_click=apex_mouse_listener.on_click)
    listener.start()
    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    client_socket_list = []
    usable_client_socket = queue.Queue(maxsize=len(global_config.listener_ports))

    buffer_size = global_config.buffer_size
    image_block_queue = GetBlockQueue(maxsize=1)
    mouse_block_queue = GetBlockQueue(maxsize=1)
    last_recv_mouse_data = {"send_time": 0.0, "recv_time": 0.0, "mouse_data": None}

    # 主线程，用于初始化socket后截图
    threading.Thread(target=socket_start).start()
    # 鼠标移动线程
    threading.Thread(target=start).start()
    # 图片消费线程，用于发送到服务端
    for i in range(len(global_config.listener_ports)):
        threading.Thread(target=consumption_picture).start()
    # 鼠标数据消费线程，用于处理鼠标数据
    threading.Thread(target=consumption_mouse_data).start()
    sys.exit(app.exec_())
