import pickle
import queue
import socket
import sys
import threading
import time

import mss
import pynput
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import get_lock_mode, start
from apex_yolov5.grabscreen import grab_screen_int_array, save_bitmap_to_file, grab_screen_int_array2
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config


class GetBlockQueue:
    def __init__(self, name, maxsize=1):
        self.name = name
        self.lock = threading.Lock()
        self.queue = queue.Queue(maxsize=maxsize)

    def get(self):
        # print("[{}]get操作前队列大小：{}".format(self.name, self.queue.qsize()))
        o = self.queue.get()
        # print("[{}]get操作后队列大小：{}".format(self.name, self.queue.qsize()))
        return o

    def put(self, data):
        while True:
            try:
                self.queue.put(data, block=False)
                break
            except queue.Full:
                try:
                    self.queue.get_nowait()
                except queue.Empty:
                    pass
        # print("[{}]put操作后队列大小：{}".format(self.name, self.queue.qsize()))

    def clear(self):
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
            # print("[{}]清空队列".format(self.name))


def socket_start():
    sct = mss.mss()
    while True:
        init_socket(global_config.listener_ports)
        try:
            while True:
                # img = grab_screen_int_array(region=global_config.region)
                img = grab_screen_int_array2(sct, monitor=global_config.monitor)
                image_block_queue.put(img)
        except Exception as e:
            print(e)
        finally:
            # 关闭连接
            for client_socket_info in client_socket_list:
                client_socket_info["socket"].close()
            client_socket_list.clear()


def init_socket(listener_ports):
    # ...or, in a non-blocking fashion:
    # 创建一个TCP/IP套接字
    for listener_port in listener_ports:
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # 服务器地址和端口
                server_address = (global_config.listener_ip, listener_port)
                # 连接服务器
                client_socket.connect(server_address)
                client_socket_info = {"port": listener_port, "socket": client_socket}
                client_socket_list.append(client_socket_info)
                usable_client_socket.put(client_socket_info)
            except Exception as e:
                print(e)
                print("连接失败，等待重连...")
                time.sleep(1)
                continue
            break


def consumption_picture():
    while True:
        with consumption_picture_lock:
            client_socket_info = usable_client_socket.get()
            img = image_block_queue.get()
        threading.Thread(target=asyn_compute_picture, args=(client_socket_info, img)).start()


last_save_pic_time = time.time()


def asyn_compute_picture(client_socket_info, img):
    client_socket = client_socket_info["socket"]
    try:
        send_start_time = time.time()
        socket_util.send(client_socket, img.rgb, buffer_size=buffer_size)
        mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
        if send_start_time > last_recv_mouse_data["send_time"] and mouse_data is not None:
            last_recv_mouse_data["send_time"] = send_start_time
            last_recv_mouse_data["recv_time"] = time.time()
            last_recv_mouse_data["mouse_data"] = mouse_data
            aims = pickle.loads(mouse_data)
            mouse_block_queue.put(aims)
            # 获取位图数据
            save_bitmap_to_file(img.rgb, aims)
        usable_client_socket.put(client_socket_info)
    except Exception as e:
        client_socket.close()
        client_socket_list.remove(client_socket_info)
        init_socket([client_socket_info["port"]])


def consumption_mouse_data():
    print_count = 0
    compute_time = time.time()
    while True:
        # mouse_data = mouse_block_queue.get()
        aims = mouse_block_queue.get()
        # aims = pickle.loads(mouse_data)
        print_count += 1
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
        log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        log_window.show()

    listener = pynput.mouse.Listener(
        on_click=apex_mouse_listener.on_click)
    listener.start()
    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    client_socket_list = []
    reconnect_socket_list = []
    usable_client_socket = GetBlockQueue(name="socket_queue", maxsize=len(global_config.listener_ports))

    buffer_size = global_config.buffer_size
    image_block_queue = GetBlockQueue("image_queue", maxsize=1)
    mouse_block_queue = GetBlockQueue("image_queue", maxsize=1)
    last_recv_mouse_data = {"send_time": 0.0, "recv_time": 0.0, "mouse_data": None}

    # 主线程，用于初始化socket后截图

    threading.Thread(target=socket_start).start()
    # 鼠标移动线程
    threading.Thread(target=start).start()
    # 图片消费线程，用于发送到服务端
    consumption_picture_lock = threading.Lock()
    for i in range(len(global_config.listener_ports)):
        threading.Thread(target=consumption_picture).start()
    # 鼠标数据消费线程，用于处理鼠标数据
    threading.Thread(target=consumption_mouse_data).start()
    sys.exit(app.exec_())
