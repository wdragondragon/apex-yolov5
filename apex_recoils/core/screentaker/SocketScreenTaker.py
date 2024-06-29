from apex_recoils.net.socket.Client import Client
from apex_yolov5.log import LogFactory
from apex_yolov5.log.Logger import Logger


class SocketScreenTaker:
    """
        网络截图
    """

    def __init__(self, logger: Logger, socket_address=("127.0.0.1", 12345)):
        self.logger = LogFactory.getLogger(self.__class__)
        self.socket_address = socket_address
        self.client = Client(socket_address, "screen_taker")
        self.client.open()

    def get_images_from_bbox(self, bbox_list):
        try:
            return self.client.get_images_from_bbox(bbox_list)
        except:
            self.client.close()
            self.open()

    def open(self):
        while not self.client.open_sign:
            try:
                self.client.open()
            except:
                pass
