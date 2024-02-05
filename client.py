import pickle
import socket
import sys
import threading
import time
import traceback

import mss
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_yolov5 import global_img_info
from apex_yolov5.grabscreen import grab_screen_int_array2
from apex_yolov5.socket.config import global_config


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

            sct = mss.mss()
            try:
                while True:
                    if not global_config.ai_toggle:
                        time.sleep(0.1)
                        continue
                    screenshot = grab_screen_int_array2(sct=sct, monitor=global_config.monitor)
                    global_img_info.set_current_img_2(screenshot, screenshot, screenshot.width, screenshot.height)
                    data = {"img_origin": screenshot.rgb, "shot_width": screenshot.width,
                            "shot_height": screenshot.height}
                    data = pickle.dumps(data)
                    socket_util.send(client_socket, data, buffer_size=buffer_size)

                    averager_data = socket_util.recv(client_socket, buffer_size=buffer_size)
                    if averager_data is None:
                        continue
                    averager = pickle.loads(averager_data)

                    global_config.sign_shot_xy(averager)
                    global_config.change_shot_xy()
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
    app = QApplication(sys.argv)
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
