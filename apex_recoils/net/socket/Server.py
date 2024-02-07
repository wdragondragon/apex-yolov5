import pickle
import socket
import threading
import traceback

from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.screentaker.ScreenTaker import ScreenTaker
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover
from net.socket import SocketUtil


class Server:
    """
        识别服务端
    """

    def __init__(self, logger: Logger, server_address, image_comparator, select_gun: ReaSnowSelectGun,
                 mouse_mover: MouseMover, screen_taker: ScreenTaker):
        self.logger = logger
        self.server_address = server_address
        self.image_comparator = image_comparator
        self.mouse_mover = mouse_mover
        self.select_gun = select_gun
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
            data = SocketUtil.recv(client_socket)
            data = pickle.loads(data)
            self.logger.print_log("客户端类型：{}".format(data))
            threading.Thread(target=self.listener, args=(client_socket, data)).start()
            # try:
            #     while True:
            #         data = SocketUtil.recv(client_socket)
            #         data = pickle.loads(data)
            #         data_type = data["type"]
            #         data = data["data"]
            #         if data_type == "compare_with_path":
            #             result = self.image_comparator.compare_with_path(*data)
            #             result_data = pickle.dumps(result)
            #             SocketUtil.send(client_socket, result_data)
            #         elif data_type == "move":
            #             result = self.image_comparator.compare_with_path(*data)
            #             result_data = pickle.dumps(result)
            #             SocketUtil.send(client_socket, result_data)
            # except Exception as e:
            #     print(e)
            #     traceback.print_exc()
            # finally:
            #     # 关闭连接
            #     try:
            #         client_socket.close()
            #     except Exception as e:
            #         print(e)
            #         traceback.print_exc()

    def listener(self, client_socket, data_type):
        """

        :param data_type:
        :param client_socket:
        """
        try:
            while True:
                data = SocketUtil.recv(client_socket)
                data = pickle.loads(data)
                if data_type == "compare_with_path":
                    result = self.image_comparator.compare_with_path(*data)
                    result_data = pickle.dumps(result)
                    SocketUtil.send(client_socket, result_data)
                elif data_type == "key_trigger":
                    self.select_gun.trigger_button(*data)
                elif data_type == "mouse_mover":
                    func_name, param = data
                    self.logger.print_log(f"mouse_mover:{func_name}({param})) ")
                    f = getattr(self.mouse_mover, func_name)
                    f(*param)
                elif data_type == "screen_taker":
                    images = self.screen_taker.get_images_from_bbox(data)
                    result_data = pickle.dumps(images)
                    SocketUtil.send(client_socket, result_data)
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
