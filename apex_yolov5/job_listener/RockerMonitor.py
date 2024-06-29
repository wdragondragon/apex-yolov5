import time

import pygame

from apex_yolov5.job_listener.JoyListener import JoyListener
from apex_yolov5.log import LogFactory


class RockerMonitor:
    """
        监听摇杆
    """

    def __init__(self, joy_listener: JoyListener):
        self.logger = LogFactory.getLogger(self.__class__)
        self.rocker_cache = []
        self.exist_rocket_time = []
        self.hold_time = None
        joy_listener.connect_joystick(pygame.JOYAXISMOTION, self.monitor)

    def monitor(self, joystick, event):
        """
        :param joystick
        """
        left = joystick.get_axis(5)
        right = joystick.get_axis(4)
        axis_x = joystick.get_axis(2)
        axis_y = joystick.get_axis(3)
        if axis_x is None:
            axis_x = 0
        if axis_y is None:
            axis_y = 0
        if left == -1:
            if len(self.rocker_cache) > 0:
                log_text = ''
                length = len(self.rocker_cache)
                log_text += '---------------------压枪摇杆监听---------------------\n'
                for i, (t_time, xy) in enumerate(self.rocker_cache):
                    keep_time = 0
                    if i != length - 1:
                        next_time, _ = self.rocker_cache[i + 1]
                        keep_time = next_time - t_time
                    x, y = xy
                    log_text += f'{i + 1},触发时间：{t_time}ms, 摇杆：{round(x * 100, 4)}，{-(round(y * 100, 4))} 持续时间：{keep_time}ms\n'
                log_text += '---------------------压枪摇杆监听结束-----------------'
                self.rocker_cache.clear()
                self.exist_rocket_time.clear()
                self.hold_time = None
                self.logger.print_log(log_text)
        elif left > -1:
            if self.hold_time is None:
                self.hold_time = time.time()
            rocket_time = int((time.time() - self.hold_time) * 1000)
            if rocket_time not in self.exist_rocket_time:
                self.rocker_cache.append((rocket_time, (axis_x, axis_y)))
                self.exist_rocket_time.append(rocket_time)
