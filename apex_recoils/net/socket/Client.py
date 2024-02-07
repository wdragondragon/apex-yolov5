import pickle  # 用于序列化/反序列化数据
import socket

from apex_yolov5.socket import socket_util

client_cache = {}


class Client:
    """
        识别客户端
    """

    def __init__(self, socket_address, client_type):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(socket_address)
        data = pickle.dumps(client_type)
        socket_util.send(self.client_socket, data)

    def compare_with_path(self, path, images, lock_score, discard_score):
        """

        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        data = (path, images, lock_score, discard_score)
        # data = {"type": "compare_with_path", "data": (path, images, lock_score, discard_score)}
        data = pickle.dumps(data)
        socket_util.send(self.client_socket, data)
        result_data = socket_util.recv(self.client_socket)
        result = pickle.loads(result_data)
        return result

    def key_trigger(self, select_gun, select_scope, hot_pop):
        """

        :param select_gun:
        :param select_scope:
        :param hot_pop:
        """
        data = (select_gun, select_scope, hot_pop)
        data = pickle.dumps(data)
        socket_util.send(self.client_socket, data)

    def mouse_mover(self, func_name, param):
        """

        :param func_name:
        :param param:
        :return:
        """
        data = (func_name, param)
        data = pickle.dumps(data)
        socket_util.send(self.client_socket, data)

    def get_images_from_bbox(self, bbox_list):
        """
            从服务获取截图，反向架构
        """
        data = bbox_list
        data = pickle.dumps(data)
        socket_util.send(self.client_socket, data)
        result_data = socket_util.recv(self.client_socket)
        result = pickle.loads(result_data)
        return result
