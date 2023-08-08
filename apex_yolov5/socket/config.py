import pynput
from torch.cuda import is_available
import os.path as op
import jsonpath as jsonpath
import json

global_config = dict()
global_config_path = 'config\\global_config.json'
if op.exists(global_config_path):
    with open(global_config_path, 'r') as global_file:
        global_config = json.load(global_file)


class Config:
    def __init__(self, data):
        self.listener_ip = self.get_config(data, 'listener_ip')
        self.listener_port = self.get_config(data, 'listener_port')
        self.buffer_size = self.get_config(data, 'buffer_size')
        self.device = self.get_config(data, 'device')
        if self.device == 'cuda':
            self.device = 'cuda' if is_available() else 'cpu'
        self.imgsz = self.get_config(data, 'imgszx')
        self.imgszy = self.get_config(data, 'imgszy')
        self.conf_thres = self.get_config(data, 'conf_thres')
        self.iou_thres = self.get_config(data, 'iou_thres')
        # 分辨率
        self.screen_width = self.get_config(data, 'screen_width')
        self.screen_height = self.get_config(data, 'screen_height')
        # 截屏区域
        self.offset_shot_screen_x = self.get_config(data, 'offset_shot_screen_x')
        self.offset_shot_screen_y = self.get_config(data, 'offset_shot_screen_y')
        self.is_show_debug_window = self.get_config(data, "is_show_debug_window")  # 可修改为True，会出现调试窗口
        self.move_mouse_speed = self.get_config(data, "move_mouse_speed")  # 游戏内鼠标灵敏

        self.half = self.device != 'cpu'
        # 默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
        self.left_top_x = self.screen_width // 2 - self.offset_shot_screen_x * 16
        self.left_top_y = self.screen_height // 2 - self.offset_shot_screen_y * 9
        self.right_bottom_x = self.screen_width // 2 + self.offset_shot_screen_x * 16
        self.right_bottom_y = self.screen_height // 2 + self.offset_shot_screen_y * 9
        self.shot_width = 2 * self.offset_shot_screen_x * 16  # 截屏区域的实际大小需要乘以2，因为是计算的中心点
        self.shot_height = 2 * self.offset_shot_screen_y * 9
        self.region = (self.left_top_x, self.left_top_y, self.right_bottom_x, self.right_bottom_y)
        self.window_name = "apex-gun"
        self.lock_move_speed = 2 / self.move_mouse_speed  # 锁定模式下鼠标移动速度

        self.mouse = pynput.mouse.Controller()  # 鼠标对象

    @staticmethod
    def get_config(config, pattern=None):
        if pattern is not None:
            value = jsonpath.jsonpath(config, pattern)
            if isinstance(value, list) and len(value) == 1:
                return value[0]
            else:
                return value
        else:
            return config


global_config = Config(global_config)
