import os.path as op
import json
import threading
import time

from pynput.mouse import Button

from apex_yolov5.auxiliary import set_intention
from apex_recoils.core.SelectGun import SelectGun
from apex_yolov5.KeyAndMouseListener import MouseListener
from apex_yolov5.log.Logger import Logger
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import Config


class RecoilsConfig:
    """
        枪械配置后座力配置
    """

    def __init__(self, logger: Logger):
        self.logger = logger
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
            self.logger.print_log("配置文件不存在: {}".format(config_file_path))

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


class RecoilsListener:
    """
        压枪监听，监听到开火，将识别到的枪械名称配置读取，然后推送到移动意图管理器中
    """

    def __init__(self,
                 logger: Logger,
                 mouse_listener: MouseListener,
                 select_gun: SelectGun, config: Config):
        self.logger = logger
        self.recoils_config = RecoilsConfig(logger=logger)
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
        sleep_time = 0.01
        while True:
            if not self.config.recoils_toggle:
                time.sleep(1)
                continue
            current_gun = self.select_gun.current_gun
            left_press = self.mouse_listener.is_press(Button.left)
            right_press = self.mouse_listener.is_press(Button.right)
            if current_gun is not None and left_press:
                spec = self.recoils_config.get_config(current_gun)
                if spec is not None:
                    sleep_time = 0.001
                    if start_time is None:
                        start_time = time.time()
                        self.logger.print_log("开始压枪")
                    if right_press:
                        time_points = spec['time_points']
                        point = (time.time() - start_time) * 1000
                        index = len(time_points) - 1 if point > time_points[-1] else next(
                            (i - 1 for i, time_point in enumerate(time_points) if time_point > point),
                            -1)
                        if index is not None and index >= 0 and num <= index:
                            # 获取对应下标的x和y
                            x_values = spec['x']
                            y_values = spec['y']
                            if len(x_values) >= num + 1:
                                x_value = x_values[num]
                                y_value = y_values[num]
                                self.logger.print_log(
                                    f'执行时间：[{time_points[num]}]<[{point}],正在压第{str(num + 1)}步，剩余{str(len(time_points) - (num + 1))}步，鼠标移动轨迹为({x_value},{y_value})')
                                # self.intent_manager.set_intention(x_value, y_value)
                                MoverFactory.mouse_mover().move_rp(x_value, y_value)
                                # set_intention(x_value, y_value, 0, 0, 0, 0, False)
                            else:
                                self.logger.print_log(
                                    f'缺失第[{num + 1}个轨迹，时间为{time_points[num]}])')
                            num += 1
                else:
                    self.logger.print_log(f"未找到[{current_gun}的压枪数据]")
            else:
                start_time = None
                num = 0
                sleep_time = 0.01
            if sleep_time != 0:
                time.sleep(sleep_time)
