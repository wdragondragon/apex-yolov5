import threading
import time

from apex_yolov5.Tools import Tools
from apex_yolov5.log import LogFactory


class GameWindowsStatus:
    """
        游戏窗口状态检测
    """

    def __init__(self):
        self.status = False
        self.logger = LogFactory.getLogger(self.__class__)
        self.timing_get_status_thread()

    def timing_get_status_thread(self):
        """
            新线程检测
        """
        threading.Thread(target=self.timing_get_status).start()

    def timing_get_status(self):
        """
            检测窗口
        """
        while True:
            status = Tools.is_apex_windows()
            if self.status != status:
                self.status = status
                self.logger.print_log(f"窗口状态切换{self.status}")
            time.sleep(2)

    def get_game_windows_status(self):
        """
            获取状态
        """
        return self.status


game_status = None


def init():
    global game_status
    game_status = GameWindowsStatus()


def get_game_status():
    return game_status
