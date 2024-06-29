from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover
from net.socket.Client import Client

from apex_yolov5.log import LogFactory


class SocketMouseMover(MouseMover):
    def __init__(self, mouse_mover_param):
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        self.client = Client((mouse_mover_param["ip"], mouse_mover_param["port"]), "mouse_mover")
        self.listener = None
        self.toggle_key_listener = None
        self.server_mouse_mover = None

    def move_rp(self, x: int, y: int):
        self.client.mouse_mover("move_rp", (x, y))

    def move(self, x: int, y: int):
        self.client.mouse_mover("move", (x, y))

    def left_click(self):
        self.client.mouse_mover("left_click", ())

    def key_down(self, value):
        self.client.mouse_mover("key_down", (value,))

    def key_up(self, value):
        self.client.mouse_mover("key_up", (value,))

    def get_position(self):
        return super().get_position()

    def is_num_locked(self):
        return super().is_num_locked()

    def is_caps_locked(self):
        return super().is_caps_locked()

    def click_key(self, value):
        self.client.mouse_mover("click_key", (value,))

    def destroy(self):
        """
            销毁
        """
        self.listener.stop()
        self.toggle_key_listener.destory()
