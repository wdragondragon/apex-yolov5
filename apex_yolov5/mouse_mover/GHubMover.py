from ctypes import CDLL

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover


class GHubMover(MouseMover):
    def __init__(self, mouse_mover_param):
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        try:
            self.gm = CDLL(r'./ghub_device.dll')
            self.gmok = self.gm.device_open() == 1
            if not self.gmok:
                print('未安装ghub或者lgs驱动!!!')
            else:
                print('初始化成功!')
        except FileNotFoundError:
            print('缺少文件')

    def move_rp(self, x: int, y: int, re_cut_size=0):
        self.move(x, y)

    def move(self, x: int, y: int):
        self.gm.moveR(int(x), int(y), False)

    def left_click(self):
        self.click_mouse_button(1)

    def click_mouse_button(self, button):
        self.press_mouse_button(button)
        self.release_mouse_button(button)

    # 按下鼠标按键
    def press_mouse_button(self, button):
        if self.gmok:
            self.gm.mouse_down(button)

    # 松开鼠标按键
    def release_mouse_button(self, button):
        if self.gmok:
            self.gm.mouse_up(button)
