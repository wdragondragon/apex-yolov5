import pickle
import socket
import threading
import traceback

from apex_recoils.core.screentaker.LocalScreenTaker import LocalScreenTaker
from apex_yolov5.log import LogFactory
from apex_yolov5.socket import socket_util


class Server:
    """
        识别服务端
    """

    def __init__(self, server_address, screen_taker: LocalScreenTaker):
        self.logger = LogFactory.getLogger(self.__class__)
        self.server_address = server_address
        self.screen_taker = screen_taker
        self.server_socket = None
        self.buffer_size = 4096
        self.open()

    def open(self):
        """
            打开服务端
        """
        # 创建一个TCP/IP套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务器地址和端口
        self.server_socket.bind(self.server_address)
        # 监听客户端连接
        self.server_socket.listen(1)

    def wait_client(self):
        """
            监听
        """
        while True:
            self.logger.print_log('等待客户端连接...')
            # 等待客户端连接
            client_socket, client_address = self.server_socket.accept()
            self.logger.print_log('客户端已连接:{}'.format(client_address))
            data = socket_util.recv(client_socket)
            data = pickle.loads(data)
            self.logger.print_log("客户端类型：{}".format(data))
            threading.Thread(target=self.listener, args=(client_socket, data)).start()

    def listener(self, client_socket, data_type):
        """

        :param data_type:
        :param client_socket:
        """
        try:
            while True:
                data = socket_util.recv(client_socket)
                data = pickle.loads(data)
                if data_type == "screen_taker":
                    images = self.screen_taker.get_images_from_bbox(data)
                    result_data = pickle.dumps(images)
                    socket_util.send(client_socket, result_data)
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            # 关闭连接
            try:
                client_socket.close()
            except Exception as e:
                print(e)
                traceback.print_exc()
