import pynput
from torch.cuda import is_available
import os.path as op
import jsonpath as jsonpath
import json

from apex_yolov5.Tools import Tools

screenshot_resolution = {
    (1920, 1080): (1542, 959, 1695, 996),
    (2560, 1440): (2093, 1281, 2275, 1332),
    # (2560, 1440): (1905, 1092, 2087, 1143),
    (3440, 1440): (2093, 1281, 2275, 1332)
}
(x, y) = Tools.get_resolution()

config_data = dict()
global_config_path = 'config\\global_config.json'
if op.exists(global_config_path):
    with open(global_config_path, 'r', encoding='utf-8') as global_file:
        config_data = json.load(global_file)


class Config:
    def __init__(self, data):
        self.config_data = data
        self.init()

    def init(self):
        self.weights = self.get_config(self.config_data, 'weights')
        self.data = self.get_config(self.config_data, 'data')
        self.listener_ip = self.get_config(self.config_data, 'listener_ip')
        self.listener_port = self.get_config(self.config_data, 'listener_port')
        self.listener_ports = self.get_config(self.config_data, 'listener_ports')
        self.buffer_size = self.get_config(self.config_data, 'buffer_size')
        self.device = self.get_config(self.config_data, 'device')
        if self.device == 'cuda':
            self.device = 'cuda' if is_available() else 'cpu'
        self.imgsz = self.get_config(self.config_data, 'imgszx')
        self.imgszy = self.get_config(self.config_data, 'imgszy')
        self.conf_thres = self.get_config(self.config_data, 'conf_thres')
        self.iou_thres = self.get_config(self.config_data, 'iou_thres')
        # 分辨率
        self.screen_width = self.get_config(self.config_data, 'screen_width')
        self.screen_height = self.get_config(self.config_data, 'screen_height')
        # 截屏区域
        self.offset_shot_screen_x = self.get_config(self.config_data, 'offset_shot_screen_x')
        self.offset_shot_screen_y = self.get_config(self.config_data, 'offset_shot_screen_y')
        self.is_show_debug_window = self.get_config(self.config_data, "is_show_debug_window")  # 可修改为True，会出现调试窗口
        # self.move_mouse_speed = self.get_config(data, "move_mouse_speed")  # 游戏内鼠标灵敏
        # 最终鼠标移动单次像素
        self.move_step = self.get_config(self.config_data, "move_step")
        # 移动路径倍率
        self.move_path_nx = self.get_config(self.config_data, "move_path_nx")  # 锁定模式下鼠标移动速度
        self.lock_index = self.get_config(self.config_data, "lock_index")  # 锁定目标的索引
        self.aim_type = self.get_config(self.config_data, "aim_type")  # 锁定目标的索引
        self.refresh_button = self.get_config(self.config_data, "refresh_button")  # 刷新按钮
        self.click_gun = self.get_config(self.config_data, "click_gun")  # 点击枪械
        self.shot_width = self.get_config(self.config_data, "shot_width")
        self.shot_height = self.get_config(self.config_data, "shot_height")
        self.auto_save = self.get_config(self.config_data, "auto_save")
        self.auto_save_path = self.get_config(self.config_data, "auto_save_path")
        self.only_save = self.get_config(self.config_data, "only_save")
        if self.only_save:
            self.shot_height = 640
            self.shot_width = 640

        self.half = self.device != 'cpu'
        # 默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
        # 屏幕中心坐标
        self.screen_center_x, self.screen_center_y = self.screen_width // 2, self.screen_height // 2
        if self.shot_width == 0 and self.shot_height == 0:
            # 截屏区域的实际大小需要乘以2，因为是计算的中心点
            self.half_shot_width, self.half_shot_height = (self.offset_shot_screen_x * 16,
                                                           self.offset_shot_screen_y * 9)
            self.shot_width, self.shot_height = (2 * self.half_shot_width,
                                                 2 * self.half_shot_height)
        else:
            self.half_shot_width, self.half_shot_height = self.shot_width // 2, self.shot_height // 2

        self.left_top_x, self.left_top_y = (self.screen_center_x - self.half_shot_width,
                                            self.screen_center_y - self.half_shot_height)
        self.right_bottom_x, self.right_bottom_y = (self.screen_center_x + self.half_shot_width,
                                                    self.screen_center_y + self.half_shot_height)

        self.region = (self.left_top_x, self.left_top_y, self.right_bottom_x, self.right_bottom_y)
        self.monitor = {"top": self.left_top_y, "left": self.left_top_x, "width": self.shot_width,
                        "height": self.shot_height}

        self.auto_save_monitor = {"top": self.screen_center_y - 320, "left": self.screen_center_x - 320, "width": 640,
                                  "height": 640}

        self.window_name = "apex-gun"
        self.select_gun_bbox = screenshot_resolution[(x, y)]  # 选择枪械的区域
        self.image_path = 'images/' + '{}x{}/'.format(x, y)  # 枪械图片路径

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

    def set_config(self, key, value):
        self.config_data[key] = value

    def save_config(self):
        with open(global_config_path, "w", encoding="utf8") as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=4)
        self.init()


global_config = Config(config_data)
