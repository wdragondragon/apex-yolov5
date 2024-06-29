import time

from apex_recoils.core.SelectGun import SelectGun
from apex_recoils.net.socket.Client import Client
from apex_yolov5.log import LogFactory


class ReaSnowSelectGunSocket:
    """
        通过网络socket触发按键
    """

    def __init__(self, select_gun: SelectGun, socket_address=("127.0.0.1", 12345)):
        self.logger = LogFactory.getLogger(self.__class__)
        self.client = Client(socket_address, "key_trigger")
        select_gun.connect(self.trigger_button)

    def trigger_button(self, select_gun, select_scope, hot_pop):
        """

        :param select_gun:
        :param select_scope:
        :param hot_pop:
        :return:
        """
        if select_gun is None or select_scope is None:
            return
        start = time.time()
        self.client.key_trigger(select_gun, select_scope, hot_pop)
        self.logger.print_log(f"该次按键触发耗时：{int(1000 * (time.time() - start))}ms")
