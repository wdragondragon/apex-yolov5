import threading
import time

from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.MouseMover import MouseMover

intention = None


class IntentManager:
    """
        意图管理器，负责推送移动意图
    """

    def __init__(self, mouse_mover: MouseMover):
        self.logger = LogFactory.getLogger(self.__class__)
        self.intention = None
        self.change_coordinates_num = 0
        self.mouse_mover = mouse_mover
        self.intention_lock = threading.Lock()

    def set_intention(self, x, y):
        """
            设置移动意图
        :param x:
        :param y:
        """
        self.intention_lock.acquire()
        try:
            self.intention = (x, y)
            self.change_coordinates_num += 1
        finally:
            # 释放锁
            self.intention_lock.release()

    def start(self):
        """
            开始读取移动意图并移动
        """
        sleep_time = 0.01
        while True:
            if self.intention is not None:
                (x, y) = self.intention
                while x != 0 or y != 0:
                    self.intention_lock.acquire()
                    try:
                        (x, y) = self.intention
                        move_step_temp = 1
                        move_step_y_temp = 1
                        move_up = min(move_step_temp, abs(x)) * (1 if x > 0 else -1)
                        move_down = min(move_step_y_temp, abs(y)) * (1 if y > 0 else -1)
                        if x == 0:
                            move_up = 0
                        elif y == 0:
                            move_down = 0
                        x -= move_up
                        y -= move_down
                        self.intention = (x, y)
                    finally:
                        self.intention_lock.release()
                    self.mouse_mover.move_rp(int(move_up), int(move_down))
                self.intention = None
                sleep_time = 0.001
            time.sleep(sleep_time)
            self.change_coordinates_num = 0
