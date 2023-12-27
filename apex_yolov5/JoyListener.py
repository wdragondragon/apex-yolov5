import threading

import pygame
from PyQt5.QtWidgets import QMessageBox

from apex_yolov5.socket.config import global_config


class JoyListener:
    def __init__(self):
        self.axis = dict()
        self.run_sign = False

    def start(self, main_windows):
        try:
            if self.run_sign:
                return
            pygame.joystick.init()
            pygame.joystick.Joystick(0)
            print("手柄初始化成功")
            pygame.joystick.quit()
            threading.Thread(target=self.aync).start()
        except:
            print("未插手柄")
            QMessageBox.warning(main_windows, "错误", "未插手柄，请插入手柄后，重新勾选手柄模式")
            return

    def aync(self):
        self.run_sign = True
        pygame.init()
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        clock = pygame.time.Clock()
        while global_config.joy_move:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.JOYAXISMOTION:
                    self.axis[event.axis] = event.value
            clock.tick(20)
        self.axis.clear()
        pygame.joystick.quit()
        pygame.quit()
        self.run_sign = False
        print("关闭手柄监听")

    def is_press(self, value):
        if value not in self.axis:
            return False
        return self.axis[value] > -1.0


joy_listener = JoyListener()
