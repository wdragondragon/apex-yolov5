import threading
import traceback

import pygame
from PyQt5.QtWidgets import QMessageBox

from apex_yolov5.log import LogFactory


class JoyListener:
    """
        手柄监听器
    """

    def __init__(self):
        self.axis = dict()
        self.logger = LogFactory.getLogger(self.__class__)
        self.run_sign = False
        self.axis_list = []
        self.call_back_list = []
        self.call_back_joystick = {}
        self.joy_listener = True

    def start(self, main_windows):
        """
            开始监听
        :param main_windows:
        :return:
        """
        try:
            if self.run_sign:
                return
            pygame.joystick.init()
            pygame.joystick.Joystick(0)
            self.logger.print_log("手柄初始化成功")
            pygame.joystick.quit()
            threading.Thread(target=self.aync).start()
        except:
            self.logger.print_log("未插手柄")
            QMessageBox.warning(main_windows, "错误", "未插手柄，请插入手柄后，重新勾选手柄模式")
            return

    def aync(self):
        """
            监听手柄按键
        """
        self.run_sign = True
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        clock = pygame.time.Clock()
        while self.joy_listener:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.JOYAXISMOTION:
                    self.axis[event.axis] = event.value
                    for func in self.axis_list:
                        try:
                            func(event.axis, event.value)
                        except:
                            traceback.print_exc()
                elif event.type == pygame.JOYBUTTONDOWN:
                    for func in self.call_back_list:
                        try:
                            func('b' + str(event.button))
                        except:
                            traceback.print_exc()
                if event.type in self.call_back_joystick:
                    for func in self.call_back_joystick[event.type]:
                        try:
                            func(joystick, event)
                        except:
                            traceback.print_exc()
            clock.tick(20)
        self.axis.clear()
        pygame.joystick.quit()
        pygame.quit()
        self.run_sign = False
        self.logger.print_log("关闭手柄监听")

    def is_press(self, value):
        """
            判断手柄按键是否按下
        :param value:
        :return:
        """
        if value not in self.axis:
            return False
        return self.axis[value] > -1.0

    def connect_axis(self, func):
        """
            连接回调方法
        :param func:
        """
        self.axis_list.append(func)

    def connect_button(self, func):
        """
            连接回调方法
        :param func:
        """
        self.call_back_list.append(func)

    def connect_joystick(self, py_type, func):
        """
            监听整个joystick
        """
        if py_type not in self.call_back_joystick:
            self.call_back_joystick[py_type] = [func]
        else:
            self.call_back_joystick[py_type].append(func)

    def stop(self):
        """
            销毁
        """
        self.joy_listener = False


joy_listener = None


def get_joy_listener():
    return joy_listener
