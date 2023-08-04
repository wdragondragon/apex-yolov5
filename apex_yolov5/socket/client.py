import pickle
import socket
import time

import pynput

from apex_yolov5.auxiliary import get_lock_mode, on_click, on_move, on_press
from apex_yolov5.grabscreen import grab_screen_int_array
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import region, shot_Width, shot_Height, mouse, screen_width, screen_height

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
server_address = ('192.168.10.3', 8888)

# 连接服务器
client_socket.connect(server_address)
buffer_size = 4096
try:
    while True:
        # 截取屏幕并发送图像给服务器
        t0 = time.time()
        img = grab_screen_int_array(region=region)
        client_socket.sendall(str(len(img)).encode('utf-8'))
        server_ready = client_socket.recv(buffer_size)
        # print("截图时间:{}\n".format(time.time() - t0) * 1000)
        t0 = time.time()
        if server_ready == b'ready':  # 如果服务端返回一个二进制的'ready'，则标明服务端收到了长度
            client_socket.send(img)
        # print("发送时间:{}\n".format(time.time() - t0) * 1000)

        t0 = time.time()
        length = client_socket.recv(buffer_size)
        if not length:
            continue
        length = int(length.decode('utf-8'))  # 将长度解码，并转成数字型
        client_socket.send(b'ready')
        recv_size = 0  # 记录长度
        mouse_data = bytearray()
        while recv_size < length:
            if length - recv_size < buffer_size:
                data = client_socket.recv(length - recv_size)
            else:
                data = client_socket.recv(buffer_size)
            mouse_data.extend(data)
            recv_size += len(data)
        aims = pickle.loads(mouse_data)
        if len(aims):
            if get_lock_mode():
                lock(aims, mouse, screen_width, screen_height, shot_width=shot_Width,
                     shot_height=shot_Height)  # x y 是分辨率
        # print("鼠标移动时间:{}\n".format(time.time() - t0) * 1000)
finally:
    # 关闭连接
    client_socket.close()
