import os
import shutil

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
    (3440, 1440): (2093, 1281, 2275, 1332),
    (1920, 1200): (1539, 1142, 1728, 1142),
    (2048, 1152): (1927, 1172, 2089, 1208)
}
(x, y) = Tools.get_resolution()

global_config_path = 'config\\global_config.json'
config_ref_path = 'config\\ref\\'
use_ref_path = 'config\\ref.txt'

sign_shot_xy_num = 0


def get_all_config_file_name(directory=config_ref_path):
    # 获取指定目录下的所有文件和子目录
    files = os.listdir(directory)
    files_name = []
    # 遍历所有文件和子目录
    for file in files:
        # 使用 os.path.join() 构建文件的完整路径
        file_path = os.path.join(directory, file)

        # 检查是否为文件
        if os.path.isfile(file_path):
            # 使用 os.path.splitext 分离文件名和扩展名
            filename, _ = os.path.splitext(file)
            files_name.append(filename)

    return files_name


def read_config_file_name(file_path=use_ref_path, default="global_config"):
    try:
        if not os.path.exists(file_path):
            return default
        # 使用 open 函数打开文件
        with open(file_path) as file:
            # 读取文件内容
            return file.read()
    except FileNotFoundError:
        print(f"文件 '{file_path}' 不存在.")
    except Exception as e:
        print(f"发生错误: {e}")


def writer_config_file_name(file_path=use_ref_path, content="global_config"):
    try:
        # 使用 open 函数以写入模式打开文件
        with open(file_path, 'w') as file:
            # 将内容写入文件
            file.write(content)
        print(f"成功写入文件: {file_path}")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")


def read_config():
    global global_config_path
    all_config_name = get_all_config_file_name()
    ref_config_name = read_config_file_name()
    if ref_config_name in all_config_name:
        print("读取预设配置：{0}".format(ref_config_name))
        global_config_path = '{0}{1}.json'.format(config_ref_path, ref_config_name)

    if op.exists(global_config_path):
        with open(global_config_path, encoding='utf-8') as global_file:
            return json.load(global_file)
    return None


def copy_config(target):
    try:
        source_path = '{0}{1}.json'.format(config_ref_path, read_config_file_name())
        target_path = '{0}{1}.json'.format(config_ref_path, target)
        # 使用 shutil.copy 复制文件
        shutil.copy(source_path, target_path)
        print(f"成功复制文件: {source_path} 到 {target_path}")

    except Exception as e:
        print(f"复制文件时发生错误: {e}")


class Config:
    def __init__(self):
        self.config_data = read_config()
        self.init()

    def update(self):
        self.config_data = read_config()
        self.init()

    def init(self):
        self.version = "v3.13"
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
        self.desktop_width = self.get_config(self.config_data, 'desktop_width', x)
        self.desktop_height = self.get_config(self.config_data, 'desktop_height', y)
        print(f"识别到桌面分辨率为:{self.desktop_width}x{self.desktop_height}")

        self.game_width = self.get_config(self.config_data, 'screen_width')
        self.game_height = self.get_config(self.config_data, 'screen_height')
        # 截屏区域
        self.offset_shot_screen_x = self.get_config(self.config_data, 'offset_shot_screen_x')
        self.offset_shot_screen_y = self.get_config(self.config_data, 'offset_shot_screen_y')
        self.is_show_debug_window = self.get_config(self.config_data, "is_show_debug_window")  # 可修改为True，会出现调试窗口
        # self.move_mouse_speed = self.get_config(data, "move_mouse_speed")  # 游戏内鼠标灵敏
        # 最终鼠标移动单次像素

        self.mouse_model = self.get_config(self.config_data, "mouse_model", "kmbox")
        self.available_mouse_models = self.get_config(self.config_data, "available_mouse_models", {
            "win32api": {},
            "kmbox": {
                "VID/PID": "66882021"
            },
            "logitech": {},
            "ty": {
                "VID/PID": "26121701"
            }
        })

        self.available_mouse_smoothing = self.get_config(self.config_data, "available_mouse_smoothing",
                                                         ["win32api", "ty"])

        self.move_step = self.get_config(self.config_data, "move_step")
        self.move_step_y = self.get_config(self.config_data, "move_step_y", self.move_step)
        # 移动路径倍率
        self.move_path_nx = self.get_config(self.config_data, "move_path_nx")  # 锁定模式下鼠标移动速度
        self.move_path_ny = self.get_config(self.config_data, "move_path_ny", self.move_path_nx)  # 锁定模式下鼠标移动速度

        self.aim_move_step = self.get_config(self.config_data, "aim_move_step", self.move_step)
        self.aim_move_step_y = self.get_config(self.config_data, "aim_move_step_y", self.move_step_y)
        # 移动路径倍率
        self.aim_move_path_nx = self.get_config(self.config_data, "aim_move_path_nx", self.move_path_nx)  # 锁定模式下鼠标移动速度
        self.aim_move_path_ny = self.get_config(self.config_data, "aim_move_path_ny", self.move_path_ny)  # 锁定模式下鼠标移动速度

        self.mouse_move_frequency = self.get_config(self.config_data, "mouse_move_frequency", 0.001)  # 锁定模式下鼠标移动速度
        self.mouse_move_frequency_switch = self.get_config(self.config_data, "mouse_move_frequency_switch",
                                                           False)
        self.mouse_smoothing_switch = self.get_config(self.config_data, "mouse_smoothing_switch", True)

        self.lock_index = self.get_config(self.config_data, "lock_index")  # 锁定目标的索引
        self.aim_type = self.get_config(self.config_data, "aim_type")  # 锁定目标的索引
        self.refresh_button = self.get_config(self.config_data, "refresh_button")  # 刷新按钮
        self.click_gun = self.get_config(self.config_data, "click_gun")  # 点击枪械
        self.shot_width = self.get_config(self.config_data, "shot_width")
        self.shot_height = self.get_config(self.config_data, "shot_height")
        self.auto_save = self.get_config(self.config_data, "auto_save")
        self.auto_save_path = self.get_config(self.config_data, "auto_save_path")
        self.only_save = self.get_config(self.config_data, "only_save")
        self.cross_hair = self.get_config(self.config_data, "cross_hair")
        self.available_guns = self.get_config(self.config_data, "available_guns")
        self.auto_charged_energy = self.get_config(self.config_data, "auto_charged_energy", False)
        self.storage_interval = self.get_config(self.config_data, "storage_interval", 0.109)
        self.auto_charged_energy_toggle = self.get_config(self.config_data, "auto_charged_energy_toggle", "shift")
        self.aim_button = self.get_config(self.config_data, "aim_button", ["left", "right", "x2"])
        self.available_models = self.get_config(self.config_data, "available_models", {
            "apex标准": {
                "weights": "./apex_model/best2.engine",
                "data": "./apex_model/data2.yaml"
            },
            "apex区分敌我": {
                "weights": "./apex_model/best.engine",
                "data": "./apex_model/data.yaml"
            }
        })
        self.current_model = self.get_config(self.config_data, "current_model", "apex区分敌我")
        self.ai_middle_toggle = self.get_config(self.config_data, "ai_middle_toggle", True)
        self.ai_toggle = self.get_config(self.config_data, "ai_toggle", False)
        self.ai_toggle_type = self.get_config(self.config_data, "ai_toggle_type", 'm')
        self.ai_toggle_key = self.get_config(self.config_data, "ai_toggle_key", 'middle')

        self.ai_available_toggle_type = self.get_config(self.config_data, "ai_available_toggle_type", ['m', 'k'])

        self.mouse_moving_radius = self.get_config(self.config_data, "mouse_moving_radius")
        self.aim_mouse_moving_radius = self.get_config(self.config_data, "aim_mouse_moving_radius",
                                                       self.mouse_moving_radius)

        self.aim_model = self.get_config(self.config_data, "aim_model", "按住")
        self.aim_models = self.get_config(self.config_data, "aim_models", ["按住", "切换"])

        # 同步syn  异步asyn
        self.screenshot_frequency_mode = self.get_config(self.config_data, "screenshot_frequency_mode", "asyn")

        self.show_config = self.get_config(self.config_data, "show_config", True)

        self.multi_stage_aiming_speed = self.get_config(self.config_data, "multi_stage_aiming_speed", [])
        self.aim_multi_stage_aiming_speed = self.get_config(self.config_data, "aim_multi_stage_aiming_speed", [])

        self.multi_stage_aiming_speed_toggle = self.get_config(self.config_data, "multi_stage_aiming_speed_toggle",
                                                               False)
        self.based_on_character_box = self.get_config(self.config_data, "based_on_character_box",
                                                      False)

        self.intention_deviation_toggle = self.get_config(self.config_data, "intention_deviation_toggle", False)
        self.intention_deviation_interval = self.get_config(self.config_data, "intention_deviation_interval", 100)
        self.intention_deviation_duration = self.get_config(self.config_data, "intention_deviation_duration", 10)
        self.intention_deviation_force = self.get_config(self.config_data, "intention_deviation_force", False)
        self.random_aim_toggle = self.get_config(self.config_data, "random_aim_toggle", False)
        self.random_coefficient = self.get_config(self.config_data, "random_coefficient", 0.3)
        self.random_change_frequency = self.get_config(self.config_data, "random_change_frequency", 20)
        self.joy_move = self.get_config(self.config_data, "joy_move", False)

        self.show_circle = self.get_config(self.config_data, "show_circle", False)
        self.show_aim = self.get_config(self.config_data, "show_aim", False)

        if self.only_save:
            self.shot_height = 640
            self.shot_width = 640

        self.half = self.device != 'cpu'
        # 默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
        # 屏幕中心坐标
        self.screen_center_x, self.screen_center_y = self.desktop_width // 2, self.desktop_height // 2
        if self.shot_width == 0 and self.shot_height == 0:
            # 截屏区域的实际大小需要乘以2，因为是计算的中心点
            self.half_shot_width, self.half_shot_height = (self.offset_shot_screen_x * 16,
                                                           self.offset_shot_screen_y * 9)
            self.shot_width, self.shot_height = (2 * self.half_shot_width,
                                                 2 * self.half_shot_height)
        else:
            self.half_shot_width, self.half_shot_height = self.shot_width // 2, self.shot_height // 2
        self.default_shot_width, self.default_shot_height = self.shot_width, self.shot_height
        self.update_shot_other_data()

        self.auto_save_monitor = {"top": self.screen_center_y - 320, "left": self.screen_center_x - 320, "width": 640,
                                  "height": 640}

        self.window_name = "apex-gun"
        self.game_solution = (self.game_width, self.game_height)
        if self.game_solution in screenshot_resolution:
            self.select_gun_bbox = screenshot_resolution[self.game_solution]  # 选择枪械的区域
        else:
            self.select_gun_bbox = screenshot_resolution[(1920, 1080)]
        self.image_path = 'images/' + '{}x{}/'.format(*self.game_solution)  # 枪械图片路径

        self.mouse = pynput.mouse.Controller()  # 鼠标对象

    def sign_shot_xy(self, averager):
        global sign_shot_xy_num
        sign_shot_xy_num = averager

    def change_shot_xy(self):
        global sign_shot_xy_num
        if sign_shot_xy_num > 0.7:
            print(f"{sign_shot_xy_num}")
            self.increase_shot_xy()
        elif sign_shot_xy_num == 0:
            # 重置
            self.reset_shot_xy()
        elif sign_shot_xy_num < 0.2:
            print(f"{sign_shot_xy_num}")
            self.reduce_shot_xy()


    def reset_shot_xy(self):
        if (self.shot_width, self.shot_height) != (self.default_shot_width, self.default_shot_height):
            self.shot_width = self.default_shot_width
            self.shot_height = self.default_shot_height
            self.update_shot_xy()
            print("重置shot大小")

    def increase_shot_xy(self):
        new_width = int(self.shot_width * 1.5)
        new_height = int(self.shot_height * 1.5)
        if new_width < 640 and new_height < 640:
            self.shot_width = new_width
            self.shot_height = new_height
            self.update_shot_xy()
            print(f"增加shot大小{self.shot_width},{self.shot_height}")
        else:
            print(f"无法增加shot大小{new_width},{new_height}")

    def reduce_shot_xy(self):
        new_width = int(self.shot_width / 1.5)
        new_height = int(self.shot_height / 1.5)
        if new_width > 80 and new_height > 80:
            self.shot_width = new_width
            self.shot_height = new_height
            self.update_shot_xy()
            print(f"缩小shot大小{self.shot_width},{self.shot_height}")
        else:
            print(f"无法缩小shot大小{new_width},{new_height}")

    def update_shot_xy(self):
        self.half_shot_width, self.half_shot_height = self.shot_width // 2, self.shot_height // 2
        self.update_shot_other_data()

    def update_shot_other_data(self):
        self.left_top_x, self.left_top_y = (self.screen_center_x - self.half_shot_width,
                                            self.screen_center_y - self.half_shot_height)
        self.right_bottom_x, self.right_bottom_y = (self.screen_center_x + self.half_shot_width,
                                                    self.screen_center_y + self.half_shot_height)

        self.region = (self.left_top_x, self.left_top_y, self.right_bottom_x, self.right_bottom_y)
        self.monitor = {"top": self.left_top_y, "left": self.left_top_x, "width": self.shot_width,
                        "height": self.shot_height}

    @staticmethod
    def get_config(config, pattern=None, default=None):
        if pattern is not None:
            value = jsonpath.jsonpath(config, pattern)
            if value is None or not value:
                if default is not None:
                    config[pattern] = default
                    return default
                else:
                    return False
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
        print("保存配置文件到:{0}".format(global_config_path))
        self.init()

    # 检查配置文件夹是否存在
    if not os.path.exists(config_ref_path):
        try:
            print("识别到使用的是旧版配置系统，进行升级")
            # 使用 os.makedirs 创建文件夹（可以递归创建多层文件夹）
            os.makedirs(config_ref_path)
            new_path = '{0}{1}.json'.format(config_ref_path, "global_config")
            shutil.copy(global_config_path, new_path)
            writer_config_file_name()
            print(f"新版默认配置文件已移动到：{new_path}")
        except Exception as e:
            print(f"创建文件夹时发生错误: {e}")


global_config = Config()
