import socket

import cv2

from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.socket.config import region

# 创建一个TCP/IP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 服务器地址和端口
server_address = ('localhost', 8888)

# 连接服务器
client_socket.connect(server_address)
buffer_size = 1024
try:
    while True:
        # 截取屏幕并发送图像给服务器
        img = grab_screen_int_array(region=region)
        client_socket.sendall(str(len(img)).encode('utf-8'))
        server_ready = client_socket.recv(buffer_size)
        if server_ready == b'ready':  # 如果服务端返回一个二进制的'ready'，则标明服务端收到了长度
            client_socket.send(img)
finally:
    # 关闭连接
    client_socket.close()
