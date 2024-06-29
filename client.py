import pickle
import socket
import sys
import threading
import time
import traceback

import mss
from PyQt5.QtWidgets import QApplication

import apex_yolov5.socket.socket_util as socket_util
from apex_recoils.core.GameWindowsStatus import GameWindowsStatus
from apex_recoils.core.screentaker.LocalScreenTaker import LocalScreenTaker
from apex_recoils.net.socket.Server import Server
from apex_yolov5 import global_img_info
from apex_yolov5.grabscreen import grab_screen_int_array2
from apex_yolov5.job_listener import JoyListener
from apex_yolov5.job_listener.JoyToKey import JoyToKey
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.Win32ApiMover import Win32ApiMover
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
            print("连接成功")
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
    LogFactory.init_logger()
    server = Server(server_address=(global_config.distributed_param["ip"], global_config.distributed_param["port"]),
                    screen_taker=LocalScreenTaker())
    threading.Thread(target=server.wait_client).start()

    game_windows_status = GameWindowsStatus()
    jtk = JoyToKey(joy_to_key_map=global_config.joy_to_key_map,
                   c1_mouse_mover=Win32ApiMover({}), game_windows_status=game_windows_status)
    JoyListener.joy_listener = JoyListener.JoyListener()
    JoyListener.joy_listener.connect_axis(jtk.axis_to_key)
    JoyListener.joy_listener.start(None)

    threading.Thread(target=main).start()
    sys.exit(app.exec_())
