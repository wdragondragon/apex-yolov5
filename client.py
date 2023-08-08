import pickle
import socket
import sys
import threading
import time
import zlib

import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5 import LogUtil
from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import get_lock_mode, on_click, on_move, on_press, start
from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config

listener = pynput.mouse.Listener(
    on_click=on_click, on_move=on_move)
listener.start()

key_listener = pynput.keyboard.Listener(
    on_press=on_press,
)
key_listener.start()

threading.Thread(target=start).start()


def main():
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
            try:
                print_count = 0
                compute_time = time.time()
                while True:
                    print_count += 1
                    t0 = time.time()
                    img = grab_screen_int_array(region=global_config.region)
                    LogUtil.set_time("截图", time.time() - t0)
                    t1 = time.time()
                    # img = zlib.compress(img)
                    LogUtil.set_time("压缩图片", time.time() - t1)
                    # print("发送数据大小：{}".format(len(img)))
                    t2 = time.time()
                    socket_util.send(client_socket, img, buffer_size=buffer_size)
                    LogUtil.set_time("发送图片", time.time() - t2)
                    t3 = time.time()
                    mouse_data = socket_util.recv(client_socket, buffer_size=buffer_size)
                    LogUtil.set_time("接收鼠标数据", time.time() - t3)
                    if not mouse_data:
                        continue
                    t4 = time.time()
                    aims = pickle.loads(mouse_data)
                    if len(aims) and get_lock_mode():
                        lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                             shot_width=global_config.shot_width, shot_height=global_config.shot_height)  # x y 是分辨率
                    LogUtil.set_time("处理鼠标数据", time.time() - t4)
                    now = time.time()
                    if now - compute_time > 1:
                        LogWindow().print_log("一秒识别[{}]次:".format(print_count))
                        LogUtil.print_time(print_count)
                        print_count = 0
                        compute_time = now
            except:
                pass
            finally:
                # 关闭连接
                client_socket.close()
        except:
            pass
        finally:
            time.sleep(1)
            LogWindow().print_log("连接断开，等待重连...")
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
