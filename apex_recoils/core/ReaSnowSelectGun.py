import json
import os.path as op

from apex_yolov5.Tools import Tools
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory


class ReaSnowSelectGun:
    """
        转换器自动识别按键宏触发
    """

    def __init__(self, config_name='ReaSnowGun'):
        self.logger = LogFactory.getLogger(self.__class__)
        self.config_path = f".\\config\\{config_name}.json"

        if op.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as global_file:
                self.key_dict = json.load(global_file)
        if "close_key" in self.key_dict:
            self.no_macro_key = self.key_dict["close_key"]
        else:
            self.no_macro_key = "0x35"

        if "no_found_click_close_key" in self.key_dict:
            self.no_found_click_close_key = self.key_dict["no_found_click_close_key"]
        else:
            self.no_found_click_close_key = True

        if "auto_caps" in self.key_dict:
            self.auto_caps = self.key_dict["auto_caps"]
        else:
            self.auto_caps = True

        self.no_macro_key = Tools.convert_to_decimal(self.no_macro_key)

    def trigger_button(self, select_gun, select_scope, hot_pop):
        """

        :param select_gun:
        :param select_scope:
        :param hot_pop:
        :return:
        """
        if select_gun is None or select_scope is None:
            self.logger.print_log(f"未识别到枪械{'，关闭宏' if self.no_found_click_close_key else ''}")
            if self.no_found_click_close_key:
                MoverFactory.mouse_mover().click_key(self.no_macro_key)
            return

        gun_scope_dict = self.key_dict.get(select_gun)
        if gun_scope_dict is None:
            self.logger.print_log(f"枪械[{select_gun}]没有数据{'，关闭宏' if self.no_found_click_close_key else ''}")
            if self.no_found_click_close_key:
                MoverFactory.mouse_mover().click_key(self.no_macro_key)
            return

        if hot_pop is not None and hot_pop in gun_scope_dict:
            gun_scope_dict = gun_scope_dict[hot_pop]

        first_char = select_scope[0]

        caps_lock = True
        if "caps_" + first_char in gun_scope_dict:
            caps_lock = gun_scope_dict["caps_" + first_char]
        elif "caps" in gun_scope_dict:
            caps_lock = gun_scope_dict["caps"]

        if first_char in gun_scope_dict:
            scope_data = gun_scope_dict[first_char]
        else:
            scope_data = None
        if "0" in gun_scope_dict:
            scope_data = gun_scope_dict["0"]
            self.logger.print_log(f"枪械[{select_gun}使用通用数据]")
        if scope_data is not None:
            self.logger.print_log(f"枪械[{select_gun}]按下键位[{scope_data}]切换数据")
            MoverFactory.mouse_mover().click_key(Tools.convert_to_decimal(scope_data))
            if self.auto_caps:
                MoverFactory.mouse_mover().toggle_caps_lock(caps_lock)
