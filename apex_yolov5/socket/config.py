import json
import os
import os.path as op
import shutil

import jsonpath as jsonpath
import pynput

from apex_yolov5.Counter import sure_no_aim, reset_counter
from apex_yolov5.Tools import Tools

screenshot_resolution = {
    (1920, 1080): (1542, 959, 1695, 996),
    (2560, 1440): (2093, 1281, 2275, 1332),
    # (2560, 1440): (1905, 1092, 2087, 1143),
    (3440, 1440): (2093, 1281, 2275, 1332),
    (1920, 1200): (1539, 1142, 1728, 1142),
    (2048, 1152): (1927, 1172, 2089, 1208),

    (1680, 1050): (1350, 944, 1503, 979),
    (2560, 1600): (2076, 1441, 2276, 1490)
}

scope_screenshot_resolution = {
    (2560, 1440): [(2034, 1338, 2059, 1363), (2069, 1338, 2094, 1363), (2106, 1338, 2131, 1363)],
    (1920, 1080): [(1522, 1002, 1542, 1022), (1551, 1002, 1571, 1022), (1579, 1002, 1599, 1022)],
    (2048, 1152): [(1880, 1213, 1901, 1234), (1910, 1213, 1931, 1234), (1940, 1213, 1961, 1234)],

    (1680, 1050): [(1333, 982, 1350, 999), (1357, 982, 1374, 999), (1382, 982, 1399, 999)],
    (2560, 1600): [(2031, 1495, 2056, 1520), (2069, 1495, 2094, 1520), (2106, 1495, 2131, 1520)]
}
hop_up_screenshot_resolution = {
    (2560, 1440): [(2142, 1338, 2167, 1363), (2180, 1338, 2205, 1363)],
    (1920, 1080): [(1607, 1002, 1627, 1022), (1635, 1002, 1655, 1022)],
    (2048, 1152): [(1970, 1213, 1991, 1234), (2000, 1213, 2021, 1234)],

    (1680, 1050): [(1406, 982, 1423, 999), (1430, 982, 1447, 999)],
    (2560, 1600): [(2144, 1495, 2169, 1520), (2181, 1495, 2206, 1520)]
}

(x, y) = Tools.get_resolution()

global_config_path = 'config\\global_config.json'
config_ref_path = 'config\\ref\\'
use_ref_path = 'config\\ref.txt'

sign_shot_xy_num = 0, 0, 0, 0


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
        self.version = "v3.53"
        self.listener_ip = self.get_config(self.config_data, 'listener_ip')
        self.listener_port = self.get_config(self.config_data, 'listener_port')
        self.listener_ports = self.get_config(self.config_data, 'listener_ports')
        self.buffer_size = self.get_config(self.config_data, 'buffer_size')
        self.device = self.get_config(self.config_data, 'device')
        if self.device == 'cuda':
            from torch.cuda import is_available
            self.device = 'cuda' if is_available() else 'cpu'
        elif self.device == 'dml':
            from torch_directml import is_available
            self.device = 'dml' if is_available() else 'cpu'
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

        self.mouse_model = self.get_config(self.config_data, "mouse_model", "win32api")
        self.available_mouse_models = self.get_config(self.config_data, "available_mouse_models", {
            "win32api": {},
            "km_box": {
                "VID/PID": "66882021"
            },
            "wu_ya": {
                "VID/PID": "046DC539"
            },
            "km_box_net": {
                "ip": "192.168.2.188",
                "port": "35368",
                "uuid": "8A6E5C53"
            },
            "fei_yi_lai": {
                "VID/PID": "C2160102"
            },
            "fei_yi_lai_single": {
                "VID/PID": "C2160301"
            },
            "logitech": {},
            "pan_ni": {
                "VID/PID": "1C1FC18A"
            }
        })

        self.available_mouse_smoothing = self.get_config(self.config_data, "available_mouse_smoothing",
                                                         ["win32api", "wu_ya"])

        self.move_step = self.get_config(self.config_data, "move_step")
        self.move_step_max = self.get_config(self.config_data, "move_step_max", self.move_step)
        self.move_step_y = self.get_config(self.config_data, "move_step_y", self.move_step)
        self.move_step_y_max = self.get_config(self.config_data, "move_step_y_max", self.move_step_y)
        # 移动路径倍率
        self.move_path_nx = self.get_config(self.config_data, "move_path_nx")  # 锁定模式下鼠标移动速度
        self.move_path_ny = self.get_config(self.config_data, "move_path_ny", self.move_path_nx)  # 锁定模式下鼠标移动速度

        self.aim_move_step = self.get_config(self.config_data, "aim_move_step", self.move_step)
        self.aim_move_step_max = self.get_config(self.config_data, "aim_move_step_max", self.move_step)
        self.aim_move_step_y = self.get_config(self.config_data, "aim_move_step_y", self.move_step_y)
        self.aim_move_step_y_max = self.get_config(self.config_data, "aim_move_step_y_max", self.move_step_y)
        # 移动路径倍率
        self.aim_move_path_nx = self.get_config(self.config_data, "aim_move_path_nx", self.move_path_nx)  # 锁定模式下鼠标移动速度
        self.aim_move_path_ny = self.get_config(self.config_data, "aim_move_path_ny", self.move_path_ny)  # 锁定模式下鼠标移动速度

        self.mouse_move_frequency = self.get_config(self.config_data, "mouse_move_frequency", 0.001)  # 锁定模式下鼠标移动速度
        self.mouse_move_frequency_switch = self.get_config(self.config_data, "mouse_move_frequency_switch",
                                                           False)
        self.mouse_smoothing_switch = self.get_config(self.config_data, "mouse_smoothing_switch", True)
        self.aiming_delay_min = self.get_config(self.config_data, "aiming_delay_min", 100)
        self.aiming_delay_max = self.get_config(self.config_data, "aiming_delay_max", 200)

        self.lock_index = self.get_config(self.config_data, "lock_index")  # 锁定目标的索引
        self.aim_type = self.get_config(self.config_data, "aim_type")  # 锁定目标的索引
        self.refresh_button = self.get_config(self.config_data, "refresh_button")  # 刷新按钮
        self.click_gun = self.get_config(self.config_data, "click_gun")  # 点击枪械
        self.shot_width = self.get_config(self.config_data, "shot_width")
        self.shot_height = self.get_config(self.config_data, "shot_height")
        self.auto_save = self.get_config(self.config_data, "auto_save")
        self.auto_save_path = self.get_config(self.config_data, "auto_save_path")
        self.only_save = self.get_config(self.config_data, "only_save")
        self.frame_rate_monitor = self.get_config(self.config_data, "frame_rate_monitor", False)
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
        self.recoils_toggle = self.get_config(self.config_data, "recoils_toggle", False)
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
        self.dynamic_mouse_move = self.get_config(self.config_data, "dynamic_mouse_move", False)

        self.show_circle = self.get_config(self.config_data, "show_circle", False)
        self.show_aim = self.get_config(self.config_data, "show_aim", False)

        # 动态识别范围

        self.dynamic_screenshot = self.get_config(self.config_data, "dynamic_screenshot", False)

        self.dynamic_upper_width = self.get_config(self.config_data, "dynamic_upper_width", 640)
        self.dynamic_upper_height = self.get_config(self.config_data, "dynamic_upper_height", 640)
        self.dynamic_lower_width = self.get_config(self.config_data, "dynamic_lower_width", 160)
        self.dynamic_lower_height = self.get_config(self.config_data, "dynamic_lower_height", 160)
        self.dynamic_screenshot_step = self.get_config(self.config_data, "dynamic_screenshot_step", 8)
        self.dynamic_screenshot_collection_window = self.get_config(self.config_data,
                                                                    "dynamic_screenshot_collection_window", 20)
        self.dynamic_screenshot_reduce_threshold = self.get_config(self.config_data,
                                                                   "dynamic_screenshot_reduce_threshold", 0.4)

        self.dynamic_screenshot_increase_threshold = self.get_config(self.config_data,
                                                                     "dynamic_screenshot_increase_threshold", 0.6)

        self.dynamic_screenshot_reduce_threshold_y = self.get_config(self.config_data,
                                                                     "dynamic_screenshot_reduce_threshold_y", 0.2)

        self.dynamic_screenshot_increase_threshold_y = self.get_config(self.config_data,
                                                                       "dynamic_screenshot_increase_threshold_y", 0.7)

        self.lead_time_toggle = self.get_config(self.config_data, "lead_time_toggle", False)
        self.lead_time_frame = self.get_config(self.config_data, "lead_time_frame", 1)
        self.lead_time_decision_frame = self.get_config(self.config_data, "lead_time_decision_frame", 5)

        # 延迟瞄准
        self.delayed_aiming = self.get_config(self.config_data, "delayed_aiming", True)
        self.delayed_aiming_factor_x = self.get_config(self.config_data, "delayed_aiming_factor_x", 0.4)
        self.delayed_aiming_factor_y = self.get_config(self.config_data, "delayed_aiming_factor_y", 0.4)
        self.re_cut_size = self.get_config(self.config_data, "re_cut_size", 0)

        # 自动识别
        self.comparator_mode = self.get_config(self.config_data, 'comparator_mode', "local")
        self.read_image_mode = self.get_config(self.config_data, 'read_image_mode', "local")
        self.key_trigger_mode = self.get_config(self.config_data, 'key_trigger_mode', "local")
        self.screen_taker = self.get_config(self.config_data, "screen_taker", "local")
        self.image_base_path = "images/" if self.read_image_mode == "local" else "http://1.15.138.227:9000/apex/images/"
        self.has_turbocharger = self.get_config(self.config_data, "has_turbocharger", [
            "专注",
            "哈沃克"
        ])
        self.delayed_activation_key_list = self.get_config(self.config_data, "delayed_activation_key_list", {})
        self.toggle_hold_key = {}
        self.joy_to_key_map = self.get_config(self.config_data, "joy_to_key_map", {})
        self.distributed_param = self.get_config(self.config_data, "distributed_param", {
            "ip": "127.0.0.1",
            "port": 12345
        })

        self.rea_snow_gun_config_name = self.get_config(self.config_data, "rea_snow_gun_config_name", "")

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

        if self.game_solution in scope_screenshot_resolution:
            self.select_scope_bbox = scope_screenshot_resolution[self.game_solution]
        else:
            self.select_scope_bbox = scope_screenshot_resolution[(1920, 1080)]

        if self.game_solution in hop_up_screenshot_resolution:
            self.select_hop_up_bbox = hop_up_screenshot_resolution[self.game_solution]
        else:
            self.select_hop_up_bbox = hop_up_screenshot_resolution[(1920, 1080)]

        self.image_path = '{}x{}/'.format(*self.game_solution)  # 枪械图片路径
        self.scope_path = 'scope/{}x{}/'.format(*self.game_solution)  # 镜子图片路径
        self.hop_up_path = 'hop_up/{}x{}/'.format(*self.game_solution)  # 镜子图片路径

        self.mouse = pynput.mouse.Controller()  # 鼠标对象

    def sign_shot_xy(self, averager=(0, 0, 0, 0)):
        global sign_shot_xy_num
        sign_shot_xy_num = averager

    def change_shot_xy(self):
        global sign_shot_xy_num
        sign_shot_x, sign_shot_y, sign_shot_origin_x, sign_shot_origin_y = sign_shot_xy_num
        # shot_size = (
        #     global_img_info.get_current_img().shot_width, global_img_info.get_current_img().shot_height)
        # origin_size = (global_config.default_shot_width, global_config.default_shot_height)
        if not self.dynamic_screenshot:
            return
        if sign_shot_x == 0 or sign_shot_y == 0:
            # 重置
            if sure_no_aim(self.dynamic_screenshot_collection_window):
                self.reset_shot_xy()
            return
        # elif (
        #         sign_shot_x > self.dynamic_screenshot_increase_threshold or sign_shot_y > self.dynamic_screenshot_increase_threshold_y) \
        #         or (origin_size > shot_size and (
        #         sign_shot_origin_x > self.dynamic_screenshot_reduce_threshold * 1.5 or sign_shot_origin_y > self.dynamic_screenshot_reduce_threshold_y * 1.5)):
        #     print(f"增加：{sign_shot_xy_num}")
        #     self.increase_shot_xy(self.dynamic_screenshot_step)
        # elif (  # 小于减小阈值时减小，不为原始大小时小于原始增大阈值时减小
        #         sign_shot_x < self.dynamic_screenshot_reduce_threshold or sign_shot_y < self.dynamic_screenshot_reduce_threshold_y) \
        #         or (origin_size < shot_size and (
        #         sign_shot_origin_x < self.dynamic_screenshot_increase_threshold * 0.7 or sign_shot_origin_y < self.dynamic_screenshot_increase_threshold_y) * 0.7):
        #     print(f"减少：{sign_shot_xy_num}")
        #     self.reduce_shot_xy(self.dynamic_screenshot_step)
        elif sign_shot_x > self.dynamic_screenshot_increase_threshold or sign_shot_y > self.dynamic_screenshot_increase_threshold_y:
            self.increase_shot_xy(self.dynamic_screenshot_step)
        elif sign_shot_x < self.dynamic_screenshot_reduce_threshold or sign_shot_y < self.dynamic_screenshot_reduce_threshold_y:
            self.reduce_shot_xy(self.dynamic_screenshot_step)
        reset_counter()

    def reset_shot_xy(self):
        if (self.shot_width, self.shot_height) != (self.default_shot_width, self.default_shot_height):
            if self.shot_width > self.default_shot_width and self.shot_height > self.default_shot_height:
                self.reduce_shot_xy(self.dynamic_screenshot_step)
            elif self.shot_width < self.default_shot_width and self.shot_height < self.default_shot_height:
                self.increase_shot_xy(self.dynamic_screenshot_step)

    def increase_shot_xy(self, step=8):
        new_width = int(self.shot_width + step)
        new_height = int(self.shot_height + step)
        if new_width < self.dynamic_upper_width and new_height < self.dynamic_upper_height:
            self.shot_width = new_width
            self.shot_height = new_height
            self.update_shot_xy()
        #     print(f"增加shot大小{self.shot_width},{self.shot_height}")
        # else:
        #     print(f"无法增加shot大小{new_width},{new_height}")

    def reduce_shot_xy(self, step=8):
        new_width = int(self.shot_width - step)
        new_height = int(self.shot_height - step)
        if new_width > self.dynamic_lower_width and new_height > self.dynamic_lower_height:
            self.shot_width = new_width
            self.shot_height = new_height
            self.update_shot_xy()
        #     print(f"缩小shot大小{self.shot_width},{self.shot_height}")
        # else:
        #     print(f"无法缩小shot大小{new_width},{new_height}")

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
