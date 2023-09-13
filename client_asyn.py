import pickle
import socket
import sys
import threading
import time
import traceback

import mss
import numpy as np
import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5 import LogUtil, check_run
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.MainWindow import MainWindow
from apex_yolov5.Tools import Tools
from apex_yolov5.auxiliary import get_lock_mode, start
from apex_yolov5.grabscreen import grab_screen_int_array, grab_screen_int_array2, save_rescreen_and_aims_to_file
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from client_mult import GetBlockQueue

listener = pynput.mouse.Listener(
    on_click=apex_mouse_listener.on_click)
listener.start()

key_listener = pynput.keyboard.Listener(
    on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
)
key_listener.start()

threading.Thread(target=start).start()


def handle():
    log_util = LogUtil.LogUtil()
    while True:
        try:
            # ...or, in a non-blocking fashion:
            # 创建一个TCP/IP套接字
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 服务器地址和端口
            server_address = (global_config.listener_ip, global_config.listener_port + 1)

            # 连接服务器
            client_socket.connect(server_address)
            buffer_size = global_config.buffer_size
            try:
                print_count = 0
                compute_time = time.time()
                while True:
                    if not Tools.is_apex_windows():
                        print("不是apex窗口")
                        time.sleep(1)
                        continue
                    if not global_config.ai_toggle:
                        time.sleep(0.1)
                        continue

                    t3 = time.time()
                    mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
                    log_util.set_time("接收鼠标数据", time.time() - t3)
                    if not mouse_data:
                        continue
                    aims = pickle.loads(mouse_data)
                    aims_data_block_queue.put(aims)
                    print_count += 1
                    now = time.time()
                    if now - compute_time > 1:
                        print("一秒移动[{}]次:".format(print_count))
                        log_util.print_time(print_count)
                        print_count = 0
                        compute_time = now
            except Exception as e:
                print(e)
                traceback.print_exc()
                pass
            finally:
                # 关闭连接
                client_socket.close()
        except:
            pass
        finally:
            time.sleep(1)
            print("连接断开，等待重连...")
            pass


def main():
    log_util = LogUtil.LogUtil()
    while True:
        try:
            # ...or, in a non-blocking fashion:
            # 创建一个TCP/IP套接字
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 服务器地址和端口
            server_address = (global_config.listener_ip, global_config.listener_port)

            # 连接服务器
            client_socket.connect(server_address)
            buffer_size = global_config.buffer_size

            sct = mss.mss()
            try:
                print_count = 0
                compute_time = time.time()
                while True:
                    if not Tools.is_apex_windows():
                        print("不是apex窗口")
                        time.sleep(1)
                        continue
                    if not global_config.ai_toggle:
                        time.sleep(0.1)
                        continue
                    t0 = time.time()
                    # img = grab_screen_int_array(region=global_config.region)
                    screenshot = grab_screen_int_array2(sct=sct, monitor=global_config.monitor)
                    socket_util.send(client_socket, screenshot.rgb, buffer_size=buffer_size)

                    screenshot = grab_screen_int_array2(sct=sct, monitor=global_config.monitor)
                    socket_util.send(client_socket, screenshot.rgb, buffer_size=buffer_size)
                    log_util.set_time("发送图片", time.time() - t0)

                    t4 = time.time()
                    aims = aims_data_block_queue.get()
                    if len(aims) and not global_config.only_save:
                        lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                             shot_width=global_config.shot_width, shot_height=global_config.shot_height)  # x y 是分辨率
                    log_util.set_time("处理鼠标数据", time.time() - t4)
                    print_count += 1
                    now = time.time()
                    if now - compute_time > 1:
                        print("一秒发送图片[{}]次:".format(print_count))
                        log_util.print_time(print_count)
                        print_count = 0
                        compute_time = now
                    time.sleep(0.001)
            except Exception as e:
                print(e)
                traceback.print_exc()
                pass
            finally:
                # 关闭连接
                client_socket.close()
        except:
            pass
        finally:
            time.sleep(1)
            print("连接断开，等待重连...")
            pass


if __name__ == "__main__":
    check_run.check()
    app = QApplication(sys.argv)
    log_window = MainWindow()
    if global_config.is_show_debug_window:
        log_window.show()
    aims_data_block_queue = GetBlockQueue("aims_data_block_queue", maxsize=1)
    threading.Thread(target=main).start()
    threading.Thread(target=handle).start()
    sys.exit(app.exec_())
