import pickle
import socket
import time

import cv2
import numpy as np
import win32con
import win32gui


from apex_yolov5.socket.config import *
from apex_yolov5.socket.yolov5_handler import get_aims

start_img = "send image".encode()
end_img = "send image end".encode()
# 创建一个TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定服务器地址和端口
server_address = ('192.168.10.3', 8888)
server_socket.bind(server_address)
# 监听客户端连接
server_socket.listen(1)
batch_size = 4096
print('等待客户端连接...')
total_size = 0
while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print('客户端已连接:', client_address)
    try:
        start_time = time.time()
        while True:
            t0 = time.time()
            # 接收客户端发送的图像数据
            length = client_socket.recv(batch_size)
            if not length:
                continue
            client_socket.send(b'ready')

            length = int(length.decode('utf-8'))  # 将长度解码，并转成数字型
            # print("图片大小:{:.1f}M".format((1.0 * length) / 1024 / 1024))
            total_size += length
            recv_size = 0  # 记录长度
            img_data = bytearray()
            while recv_size < length:
                if length - recv_size < batch_size:
                    data = client_socket.recv(length - recv_size)
                else:
                    data = client_socket.recv(batch_size)
                img_data.extend(data)
                recv_size += len(data)
            # 将接收到的数据转换为图像
            img = np.frombuffer(bytes(img_data), dtype='uint8')
            # img0 = cv2.imdecode(img, cv2.IMREAD_COLOR)
            # img.shape = (height, width, 4)
            left, top, x2, y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
            img = img.reshape((height, width, 4))
            img0 = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # 在这里可以对图像进行进一步处理

            aims = get_aims(img0)
            aims_data = pickle.dumps(aims)
            client_socket.sendall(str(len(aims_data)).encode('utf-8'))
            client_ready = client_socket.recv(batch_size)
            if client_ready == b'ready':
                client_socket.sendall(aims_data)

            if len(aims):
                # if get_lock_mode():
                #     lock(aims, mouse, screen_width, screen_height, shot_width=shot_Width,
                #          shot_height=shot_Height)  # x y 是分辨率
                for i, det in enumerate(aims):
                    tag, x_center, y_center, width, height = det
                    x_center, width = shot_Width * float(x_center), shot_Width * float(width)
                    y_center, height = shot_Height * float(y_center), shot_Height * float(height)
                    top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                    bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                    color = (0, 0, 255)  # BGR
                    if isShowDebugWindow:
                        cv2.rectangle(img0, top_left, bottom_right, color, thickness=3)
            # print("FPS:{:.1f},{:.1f}M/s".format(1.0 / (time.time() - t0),
            #                                     (1.0 * total_size / 1024 / 1024) / (time.time() - start_time)))
            # 发送响应给客户端
            if isShowDebugWindow:
                cv2.namedWindow(window_Name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(window_Name, shot_Width // 2, shot_Height // 2)
                cv2.putText(img0, "FPS:{:.1f},{:.1f}M/s".format(1.0 / (time.time() - t0),
                                                                (1.0 * total_size / 1024 / 1024) / (
                                                                        time.time() - start_time)),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 0), 4)
                # global t0
                cv2.imshow(window_Name, img0)

                t0 = time.time()
                hwnd = win32gui.FindWindow(None, window_Name)
                CVRECT = cv2.getWindowImageRect(window_Name)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            print("服务端处理时间：{}\n".format((time.time() - t0)) * 1000)
    finally:
        # 关闭连接
        client_socket.close()
