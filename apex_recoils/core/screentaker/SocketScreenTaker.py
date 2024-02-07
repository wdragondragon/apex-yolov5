from apex_recoils.net.socket.Client import Client
from apex_yolov5.log.Logger import Logger


class SocketScreenTaker():
    """
        网络截图
    """

    def __init__(self, logger: Logger, socket_address=("127.0.0.1", 12345)):
        self.logger = logger
        self.client = Client(socket_address, "screen_taker")

    def get_images_from_bbox(self, bbox_list):
        return self.client.get_images_from_bbox(bbox_list)
