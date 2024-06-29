import json
import os.path as op
import threading
import time

import requests
from pynput.mouse import Button

from apex_recoils.core.SelectGun import SelectGun
from apex_yolov5.KeyAndMouseListener import MouseListener
from apex_yolov5.auxiliary import get_intention
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import Config


class RecoilsConfig:
    """
        枪械配置后座力配置
    """

    def __init__(self):
        self.logger = LogFactory.getLogger(self.__class__)
        self.specs_data = None
        self.load()

    def load(self):
        """
            加载压枪数据
        """
        config_file_path = 'config\\specs.json'
        if op.exists(config_file_path):
            with open(config_file_path, encoding='utf8') as file:
                self.specs_data = json.load(file)
                self.logger.print_log("加载配置文件: {}".format(config_file_path))
        else:
            config_json_str = RecoilsConfig.read_file_from_url("http://1.15.138.227:9000/apex/specs.json")
            self.specs_data = json.loads(config_json_str)
            self.logger.print_log("加载配置文件成功")

    def get_config(self, name):
        """
            根据枪协名称获取后座力数据
        :param name:
        :return:
        """
        for spec in self.specs_data:
            if spec['name'] == name:
                return spec
        return None

    @staticmethod
    def read_file_from_url(url):
        """

        :param url:
        :return:
        """
        try:
            # 发送GET请求获取文件内容
            # headers = random.choice(headers_list)
            response = requests.get(url)
            response.encoding = 'utf-8'
            # 检查请求是否成功
            if response.status_code == 200:
                # 根据换行符切割文件内容并返回列表
                text = response.text
                return text
            else:
                print(f"Failed to read file from URL. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class RecoilsListener:
    """
        压枪监听，监听到开火，将识别到的枪械名称配置读取，然后推送到移动意图管理器中
    """

    def __init__(self,
                 mouse_listener: MouseListener,
                 select_gun: SelectGun, config: Config):
        self.logger = LogFactory.getLogger(self.__class__)
        self.recoils_config = RecoilsConfig()
        self.mouse_listener = mouse_listener
        self.select_gun = select_gun
        self.recoils_listener_thread = None
        self.config = config

    def start(self):
        """
            开始监听
        """
        self.recoils_listener_thread = threading.Thread(target=self.run)
        self.recoils_listener_thread.start()

    def run(self):
        """
            开始监听
        """
        start_time = None
        num = 0
        sleep_time = 0.001
        last_left_press_time = None
        last_press_status = None
        go_on_num = 0
        while True:
            if (not self.config.recoils_toggle or
                    not MoverFactory.mouse_mover().is_caps_locked()):
                time.sleep(1)
                continue
            current_gun = self.select_gun.current_gun
            left_press = self.mouse_listener.is_press(Button.left)
            right_press = self.mouse_listener.is_press(Button.right)
            now = time.time()
            if last_press_status is not None and not last_press_status and left_press:
                if last_left_press_time is not None and now - last_left_press_time < 0.5:
                    self.logger.print_log(f"继续：{go_on_num}")
                else:
                    go_on_num = 0

            if current_gun is not None and left_press:
                current_hot_pop = self.select_gun.current_hot_pop
                spec = self.recoils_config.get_config(current_gun)
                if spec is not None:
                    last_left_press_time = time.time()
                    last_press_status = True
                    recoil_type = spec['type']
                    spec = spec['recoils']
                    if current_hot_pop is not None and current_hot_pop in spec:
                        spec = spec[current_hot_pop]
                    if start_time is None:
                        start_time = time.time()
                        self.logger.print_log("开始压枪")
                    if right_press:
                        spec = spec['aim']
                    else:
                        spec = spec['un_aim']
                    if recoil_type == 'serial':
                        num, sleep_time = self.handle_serial(spec, start_time, num)
                    else:
                        go_on_num, sleep_time = self.handle_intermittent(spec, go_on_num)
                else:
                    self.logger.print_log(f"未找到[{current_gun}的压枪数据]")
            else:
                last_press_status = False
                start_time = None
                num = 0
                sleep_time = 0.01
            if sleep_time != 0:
                time.sleep(sleep_time)

    def handle_serial(self, spec, start_time, num):
        """
            全自动枪械处理轨迹
        """
        time_points = spec['time_points']
        if len(time_points) == 0:
            return num, 0.01
        if self.move_index_xy(spec=spec, current_index=num, point=(time.time() - start_time) * 1000):
            num += 1
        return num, 0.001

    def handle_intermittent(self, spec, num):
        """
            连发枪处理轨迹
        """
        spec_len = len(spec)
        if spec_len > num:
            spec = spec[num]
            time_points = spec['time_points']
            time_points_len = len(time_points)
            if time_points_len == 0:
                return num + 1, 0.001
            start_time = time.time()
            sub_num = 0
            while time_points_len > sub_num and self.mouse_listener.is_press(Button.left):
                if self.move_index_xy(spec=spec, current_index=sub_num, point=(time.time() - start_time) * 1000):
                    sub_num += 1
                time.sleep(0.001)
            return num + 1, 0.001
        else:
            return num, 0.01

    def move_index_xy(self, spec, current_index, point):
        """
            真实的移动轨迹方法
        """
        time_points = spec['time_points']
        # 获取对应下标的x和y
        x_values = spec['x']
        y_values = spec['y']
        index = len(time_points) - 1 if point > time_points[-1] else next(
            (i - 1 for i, time_point in enumerate(time_points) if time_point > point),
            -1)
        if index is not None and index >= 0 and current_index <= index:
            if len(x_values) >= current_index + 1:
                x_value = x_values[current_index]
                y_value = y_values[current_index]
                self.logger.print_log(
                    f'执行时间：[{time_points[current_index]}]<[{point}],正在压第{str(current_index + 1)}步，剩余{str(len(time_points) - (current_index + 1))}步，鼠标移动轨迹为({x_value},{y_value})')
                # self.intent_manager.set_intention(x_value, y_value)
                if get_intention() is None:
                    MoverFactory.mouse_mover().move_rp(x_value, y_value)
                # set_intention(x_value, y_value, 0, 0, 0, 0, False)
            else:
                self.logger.print_log(
                    f'缺失第[{current_index + 1}个轨迹，时间为{time_points[current_index]}])')
            return True
        return False


def merge_x_y(x, y, time_points_x, time_points_y):
    new_x = []
    new_y = []
    new_time_points = []

    x_length = len(time_points_x)
    y_length = len(time_points_y)

    xi = 0
    yi = 0
    while xi < x_length or yi < y_length:
        if xi >= x_length:
            new_y.append(y[yi])
            new_x.append(0)
            new_time_points.append(time_points_y[yi])
            yi += 1
            continue
        if yi >= y_length:
            new_x.append(x[xi])
            new_y.append(0)
            new_time_points.append(time_points_x[xi])
            xi += 1
            continue

        if time_points_x[xi] == time_points_y[yi]:
            new_x.append(x[xi])
            new_y.append(y[yi])
            new_time_points.append(time_points_x[xi])
            xi += 1
            yi += 1
        elif time_points_x[xi] < time_points_y[yi]:
            new_x.append(x[xi])
            new_y.append(0)
            new_time_points.append(time_points_x[xi])
            xi += 1
        elif time_points_x[xi] > time_points_y[yi]:
            new_y.append(y[yi])
            new_x.append(0)
            new_time_points.append(time_points_y[yi])
            yi += 1
    print(new_time_points)
    print(new_x)
    print(new_y)
    return new_time_points, new_x, new_y
