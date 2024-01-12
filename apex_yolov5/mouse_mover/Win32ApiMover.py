from ctypes import windll

from apex_yolov5.log.Logger import Logger
from apex_yolov5.mouse_mover.MouseMover import MouseMover

MOUSE_EVEN_TF_LEFT_DOWN = 0x2
MOUSE_EVEN_TF_LEFT_UP = 0x4
MOUSE_EVEN_TF_MIDDLE_DOWN = 0x20
MOUSE_EVEN_TF_MIDDLE_UP = 0x40
MOUSE_EVEN_TF_RIGHT_DOWN = 0x8
MOUSE_EVEN_TF_RIGHT_UP = 0x10
MOUSE_EVEN_TF_MOVE = 0x1


class Win32ApiMover(MouseMover):

    def __init__(self, logger: Logger, mouse_mover_param):
        super().__init__(mouse_mover_param)
        self.user32 = windll.user32
        self.logger = logger

    def move_rp(self, x: int, y: int):
        self.user32.mouse_event(MOUSE_EVEN_TF_MOVE, x, y)

    def move(self, x, y):
        self.move_rp(x, y)

    def left_click(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_DOWN, 0, 0, 0, 0)
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_UP, 0, 0, 0, 0)
