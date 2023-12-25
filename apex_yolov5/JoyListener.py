import pygame


class JoyListener:
    def __init__(self):
        self.axis = dict()

    def start(self):
        try:
            pygame.init()
            pygame.joystick.init()
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print("手柄初始化成功")
            clock = pygame.time.Clock()
            # EVENT PROCESSING STEP
            while True:
                for event in pygame.event.get():  # User did something
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis[event.axis] = event.value
                clock.tick(20)
        except:
            print("未插手柄")

    def is_press(self, value):
        if value not in self.axis:
            return False
        return self.axis[value] > -1.0


joy_listener = JoyListener()
