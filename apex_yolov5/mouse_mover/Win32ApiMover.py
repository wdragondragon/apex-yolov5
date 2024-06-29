from ctypes import windll

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover

MOUSE_EVEN_TF_LEFT_DOWN = 0x2
MOUSE_EVEN_TF_LEFT_UP = 0x4
MOUSE_EVEN_TF_MIDDLE_DOWN = 0x20
MOUSE_EVEN_TF_MIDDLE_UP = 0x40
MOUSE_EVEN_TF_RIGHT_DOWN = 0x8
MOUSE_EVEN_TF_RIGHT_UP = 0x10
MOUSE_EVEN_TF_MOVE = 0x1


class Win32ApiMover(MouseMover):

    def __init__(self, mouse_mover_param):
        super().__init__(mouse_mover_param)
        self.user32 = windll.user32
        self.logger = LogFactory.getLogger(self.__class__)

    def move_rp(self, x: int, y: int, re_cut_size=0):
        if re_cut_size == 0:
            self.user32.mouse_event(MOUSE_EVEN_TF_MOVE, x, y)
        else:
            coordinates_arr = self.split_coordinates(x, y)
            for move_x, move_y in coordinates_arr:
                self.user32.mouse_event(MOUSE_EVEN_TF_MOVE, move_x, move_y)

    def move(self, x, y):
        self.move_rp(x, y)

    def left_click(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_DOWN, 0, 0, 0, 0)
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_UP, 0, 0, 0, 0)

    def move_test(self, x: int, y: int):
        self.user32.mouse_event(MOUSE_EVEN_TF_MOVE, x, y)

    def split_coordinates(self, x, y):
        result = []

        # 处理 x 坐标
        if x > 0:
            result.extend([(1, 0) for _ in range(x)])
        elif x < 0:
            result.extend([(-1, 0) for _ in range(abs(x))])

        # 处理 y 坐标
        if y > 0:
            result.extend([(0, 1) for _ in range(y)])
        elif y < 0:
            result.extend([(0, -1) for _ in range(abs(y))])

        return result

    def left_click(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_DOWN, 0, 0, 0, 0)
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_UP, 0, 0, 0, 0)

    def left_down(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_DOWN, 0, 0, 0, 0)

    def left_up(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_LEFT_UP, 0, 0, 0, 0)

    def right_down(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_RIGHT_DOWN, 0, 0, 0, 0)

    def right_up(self):
        self.user32.mouse_event(MOUSE_EVEN_TF_RIGHT_UP, 0, 0, 0, 0)
