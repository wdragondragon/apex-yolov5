import pickle
import socket
import time

import cv2
import numpy as np
from config import global_config
import yolov5_handler
import socket_util
import log_ui


def main():
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
        print('客户端已连接:', client_address)
        try:
            start_time = time.time()
            while True:
                t0 = time.time()
                # 接收客户端发送的图像数据
                img_data = socket_util.recv(client_socket, buffer_size=buffer_size)
                total_size += len(img_data)
                # 将接收到的数据转换为图像
                img = np.frombuffer(bytes(img_data), dtype='uint8')
                left, top, x2, y2 = global_config.region
                width = x2 - left + 1
                height = y2 - top + 1
                img = img.reshape((height, width, 4))
                img0 = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                # 在这里可以对图像进行进一步处理

                aims = yolov5_handler.get_aims(img0)
                aims_data = pickle.dumps(aims)
                socket_util.send(client_socket, aims_data, buffer_size=buffer_size)

                if global_config.is_show_debug_window:
                    log_ui.show(aims, img0, start_time, t0, total_size)
                print("服务端处理时间：{}\n".format((time.time() - t0)) * 1000)
        except:
            pass
        finally:
            # 关闭连接
            try:
                client_socket.close()
            except:
                pass
            log_ui.destroy()


main()
