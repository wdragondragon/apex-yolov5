import time

from apex_recoils.core import GameWindowsStatus
from apex_yolov5.KmBoxNetListener import KmBoxNetListener
from apex_yolov5.Tools import Tools
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory


class ToggleKeyListener:
    """
        监听kmnet 关于辅助开关键的实现
    """

    def __init__(self, km_box_net_listener: KmBoxNetListener, delayed_activation_key_list,
                 toggle_hold_key):
        import kmNet
        self.kmNet = kmNet
        self.logger = LogFactory.getLogger(self.__class__)
        self.km_box_net_listener = km_box_net_listener
        # 自定义按住延迟转换
        self.delayed_activation_key_status_map = {}
        self.delayed_activation_key_list = [(Tools.convert_to_decimal(key), value) for key, value in
                                            delayed_activation_key_list.items()]
        km_box_net_listener.connect(self.delayed_activation)

        # 自定义切换按住键
        self.key_status_map = {}
        self.toggle_hold_key = toggle_hold_key
        self.toggle_close_key = {}

        for key in self.toggle_hold_key:
            close_keys = self.toggle_hold_key[key]
            for close_key in close_keys:
                if close_key not in self.toggle_close_key:
                    self.toggle_close_key[close_key] = []
                if Tools.convert_to_decimal(key) is None:
                    continue
                self.toggle_close_key[close_key].append(key)

        self.mask_toggle_key()
        km_box_net_listener.connect(self.toggle_change)

    def mask_toggle_key(self):
        self.kmNet.unmask_all()
        for key in self.toggle_hold_key:
            self.kmNet.mask_keyboard(Tools.convert_to_decimal(key))
            self.key_status_map[key] = ToggleKey()

    def toggle_change(self):
        if not GameWindowsStatus.get_game_status().get_game_windows_status():
            return
        for key in self.toggle_hold_key:
            num_key = Tools.convert_to_decimal(key)
            if num_key is None:
                continue
            hold_status = self.kmNet.isdown_keyboard(num_key) == 1
            toggle_key_status = self.key_status_map[key]

            if not toggle_key_status.last_hold_status and hold_status:
                toggle_key_status.toggle()
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"启动长按" + key)
                    MoverFactory.mouse_mover().key_down(num_key)
                else:
                    self.logger.print_log(f"关闭长按" + key)
                    MoverFactory.mouse_mover().key_up(num_key)
            toggle_key_status.hold(hold_status)

        for close_key in self.toggle_close_key:
            num_close_key = Tools.convert_to_decimal(close_key)
            if num_close_key is None:
                continue
            hold_status = self.kmNet.isdown_keyboard(num_close_key) == 1
            if not hold_status:
                continue
            keys = self.toggle_close_key[close_key]
            for key in keys:
                if key not in self.key_status_map:
                    continue
                toggle_key_status = self.key_status_map[key]
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"关闭长按" + key)
                    MoverFactory.mouse_mover().key_up(Tools.convert_to_decimal(key))
                    toggle_key_status.toggle()

    def controller_toggle_hold_change(self, key):
        if key in self.toggle_close_key:
            keys = self.toggle_close_key[key]
            for key in keys:
                if key not in self.key_status_map:
                    continue
                toggle_key_status = self.key_status_map[key]
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"关闭长按" + key)
                    MoverFactory.mouse_mover().key_up(Tools.convert_to_decimal(key))
                    toggle_key_status.toggle()

    def delayed_activation(self):
        if not GameWindowsStatus.get_game_status().get_game_windows_status():
            return
        for key, delayed_param in self.delayed_activation_key_list:
            key_time = delayed_param["delay"] if "delay" in delayed_param else None
            up_deactivation = delayed_param["up_deactivation"]
            down_deactivation = delayed_param["down_deactivation"]
            click_key = delayed_param["click_key"] if "click_key" in delayed_param else None
            click_keys = delayed_param["click_keys"] if "click_keys" in delayed_param else None

            hold_status = self.kmNet.isdown_keyboard(key) == 1

            if hold_status:
                if click_keys is None:
                    if key not in self.delayed_activation_key_status_map:
                        self.delayed_activation_key_status_map[key] = DelayedActivationKey()

                    delayed_activation_key_status = self.delayed_activation_key_status_map[key]
                    if down_deactivation:
                        if (int((time.time() - delayed_activation_key_status.hold_time) * 1000) >= key_time
                                and not delayed_activation_key_status.handle):
                            delayed_activation_key_status.handle = True
                            self.logger.print_log(f"持续按下{key},{key_time}ms，转换器开关按下：[{click_key}]")
                            # 转换器切换键
                            MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(click_key))
                else:
                    if down_deactivation:
                        for click_key_item in click_keys:
                            key_time = click_key_item["delay"]
                            click_key = click_key_item["click_key"]
                            if key not in self.delayed_activation_key_status_map:
                                self.delayed_activation_key_status_map[key] = DelayedActivationKey()

                            delayed_activation_key_status = self.delayed_activation_key_status_map[key]
                            if (int((time.time() - delayed_activation_key_status.hold_time) * 1000) >= key_time
                                    and not delayed_activation_key_status.in_handle_list(key_time)):
                                delayed_activation_key_status.list_handle(key_time)
                                self.logger.print_log(f"持续按下{key},{key_time}ms，转换器开关按下：[{click_key}]")
                                # 转换器切换键
                                MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(click_key))
            else:
                if key in self.delayed_activation_key_status_map:
                    if up_deactivation:
                        delayed_activation_key_status = self.delayed_activation_key_status_map[key]
                        # 转换器切换键
                        if delayed_activation_key_status.handle:
                            self.logger.print_log(f"持续按下{key}后弹起，转换器开关按下：[{click_key}]")
                            MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(click_key))
                        else:
                            if click_keys is None:
                                if int((time.time() - delayed_activation_key_status.hold_time) * 1000) >= key_time:
                                    self.logger.print_log(f"按下{key}开关，转换器开关按下：[{click_key}]")
                                    MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(click_key))
                            else:
                                click_keys = sorted(click_keys, key=lambda x: x["delay"], reverse=True)
                                for click_key_item in click_keys:
                                    key_time = click_key_item["delay"]
                                    click_key = click_key_item["click_key"]
                                    if int((time.time() - delayed_activation_key_status.hold_time) * 1000) >= key_time:
                                        if click_key is not None:
                                            self.logger.print_log(
                                                f"符合按键时长{key_time}，按下{key}开关，转换器开关按下：[{click_key}]")
                                            MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(click_key))
                                        break
                    self.delayed_activation_key_status_map.pop(key)

    def destory(self):
        self.kmNet.unmask_all()


class DelayedActivationKey:
    """
        开关状态
    """

    def __init__(self):
        self.hold_time = time.time()
        self.handle = False
        self.handle_list = dict()

    def in_handle_list(self, delay):
        return delay in self.handle_list and self.handle_list[delay]

    def list_handle(self, delay):
        self.handle_list[delay] = True


class ToggleKey:
    """
        开关状态
    """

    def __init__(self):
        self.last_hold_status = False
        self.toggle_status = False

    def toggle(self):
        self.toggle_status = not self.toggle_status

    def hold(self, status):
        self.last_hold_status = status
