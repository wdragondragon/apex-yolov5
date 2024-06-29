import pickle
import socket
import sys
import threading
import time
import traceback

import cv2
import numpy as np
import pynput
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from apex_recoils.core import SelectGun, ReaSnowSelectGun
from apex_recoils.core.image_comparator.NetImageComparator import NetImageComparator
from apex_recoils.core.screentaker.SocketScreenTaker import SocketScreenTaker
from apex_yolov5 import LogUtil, global_img_info
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.auxiliary import start
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_lock import lock
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket import socket_util
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import get_aims
from apex_yolov5.windows.config_window import ConfigWindow

log_util = LogUtil.LogUtil()


def main(log_window):
    # 创建一个TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定服务器地址和端口
    server_address = (global_config.listener_ip, global_config.listener_port)
    server_socket.bind(server_address)
    # 监听客户端连接
    server_socket.listen(1)
    buffer_size = global_config.buffer_size
    while True:
        total_size = 0
        print('等待客户端连接...')
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print('客户端已连接:{}'.format(client_address))
        try:
            print_count = 0
            compute_time = time.time()
            while True:
                data = socket_util.recv(client_socket, buffer_size=buffer_size)
                data = pickle.loads(data)
                img_origin = data["img_origin"]
                shot_width = data["shot_width"]
                shot_height = data["shot_height"]
                total_size += len(img_origin)
                # 将接收到的数据转换为图像
                img = np.frombuffer(img_origin, dtype='uint8')
                img = img.reshape((shot_height, shot_width, 3))
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                global_img_info.set_current_img_2(img_origin, img, shot_width, shot_height)

                aims = get_aims(img)
                bboxes = []
                averager = (0, 0, 0, 0)
                if len(aims):
                    averager = lock(aims, global_config.mouse, global_config.desktop_width,
                                    global_config.desktop_height,
                                    shot_width=shot_width, shot_height=shot_height)  # x y 是分辨率
                    if global_config.is_show_debug_window:
                        for i, det in enumerate(aims):
                            tag, x_center, y_center, width, height = det
                            x_center, width = global_img_info.get_current_img().shot_width * float(
                                x_center), global_img_info.get_current_img().shot_width * float(
                                width)
                            y_center, height = global_img_info.get_current_img().shot_height * float(
                                y_center), global_img_info.get_current_img().shot_height * float(
                                height)
                            top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                            bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                            bboxes.append((tag, top_left, bottom_right))

                averager_data = pickle.dumps(averager)
                socket_util.send(client_socket, averager_data, buffer_size=buffer_size)

                print_count += 1
                now = time.time()
                if now - compute_time > 1:
                    print("识别[{}]次，传输{:.1f}M/s".format(print_count, (1.0 * total_size / 1024 / 1024)))
                    log_window.add_frame_rate_plot((print_count, print_count))
                    total_size = 0
                    print_count = 0
                    compute_time = now
                if global_config.is_show_debug_window:
                    log_window.set_image(img, bboxes=bboxes)
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
        finally:
            # 关闭连接
            try:
                client_socket.close()
            except:
                pass


# main()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    LogFactory.init_logger()
    SelectGun.select_gun = SelectGun.SelectGun(bbox=global_config.select_gun_bbox,
                                               image_path=global_config.image_path,
                                               scope_bbox=global_config.select_scope_bbox,
                                               scope_path=global_config.scope_path,
                                               refresh_buttons=global_config.refresh_button,
                                               has_turbocharger=global_config.has_turbocharger,
                                               hop_up_bbox=global_config.select_hop_up_bbox,
                                               hop_up_path=global_config.hop_up_path,
                                               image_comparator=NetImageComparator(global_config.image_base_path),
                                               screen_taker=SocketScreenTaker(LogFactory.logger(), (
                                                   global_config.distributed_param["ip"],
                                                   global_config.distributed_param["port"])))

    rea_snow_select_gun = ReaSnowSelectGun.ReaSnowSelectGun()
    SelectGun.get_select_gun().connect(rea_snow_select_gun.trigger_button)

    listener = pynput.mouse.Listener(
        on_click=apex_mouse_listener.on_click)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    threading.Thread(target=start).start()
    MoverFactory.init_mover(
        mouse_model=global_config.mouse_model,
        mouse_mover_params=global_config.available_mouse_models)
    log_window = ConfigWindow(global_config, "服务端")
    log_window.show()
    if global_config.is_show_debug_window:
        log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        log_window.show()
    threading.Thread(target=main, args=(log_window,)).start()
    sys.exit(app.exec_())
