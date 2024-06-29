import threading
import time

import pygame

from apex_recoils.core.image_comparator.DynamicSizeImageComparator import DynamicSizeImageComparator
from apex_yolov5.Tools import Tools
from apex_yolov5.job_listener.JoyListener import JoyListener
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory


class S1SwitchMonitor:
    """
        监听s1切层
    """

    def __init__(self, joy_listener: JoyListener,
                 licking_state_path,
                 dynamic_size_image_comparator: DynamicSizeImageComparator, s1_switch_hold_map, retry=5):
        self.logger = LogFactory.getLogger(self.__class__)
        self.dynamic_size_image_comparator = dynamic_size_image_comparator
        self.licking_state_path = licking_state_path
        # self.click_state = False
        # self.threading_state = False
        self.threading_state_scene_map = {}
        self.retry = retry
        self.dict = {
            pygame.JOYBUTTONDOWN: "JOYBUTTONDOWN",
            pygame.JOYBUTTONUP: "JOYBUTTONUP"
        }
        self.s1_switch_hold_map = s1_switch_hold_map
        # self.hold_key = self.s1_switch_hold_map
        # self.toggle_key = self.s1_switch_hold_map["toggle_key"]
        self.hole_key_status_map = {}
        self.down_key_time = {}
        # todo 添加监听手柄按键类型
        joy_listener.connect_joystick(pygame.JOYBUTTONUP, self.monitor)
        joy_listener.connect_joystick(pygame.JOYBUTTONDOWN, self.monitor)

    def monitor(self, joystick, event):
        if event.type in self.dict:
            if event.type == pygame.JOYBUTTONDOWN:
                self.logger.print_log(f"检测到按下手柄按键:{event.button}")
                self.hole_key_status_map[event.button] = time.time()
            elif event.type == pygame.JOYBUTTONUP and event.button in self.hole_key_status_map:
                self.logger.print_log(f"检测到松开手柄按键:{event.button}")
                self.hole_key_status_map.pop(event.button)

            for (scene, key_map) in self.s1_switch_hold_map.items():
                if str(event.button) in key_map["key"] and scene not in self.threading_state_scene_map:
                    self.logger.print_log(f"切换层进入场景{scene}的识别")
                    self.threading_state_scene_map[scene] = True
                    threading.Thread(target=self.monitor_thread, args=(joystick, scene, key_map)).start()

    def monitor_thread(self, joystick, scene, key_map):
        # todo 需要添加监听手柄舔包键长按之后触发识别
        retry = 0
        # 触发后背包判断后，开始识别，识别到背包中则按下切层，直到未识别到背包则松开并退出循环
        # start = time.time()
        detect_time = None
        skip_detect = False
        skip_delay = 0
        toggle_key = key_map["toggle_key"]
        hold_key = key_map["key"]
        click_state = False
        down_key_time = time.time()
        while True:
            for key in hold_key:
                if key != "toggle_key" and int(key) in self.hole_key_status_map.keys():
                    start_time = self.hole_key_status_map[int(key)]
                    delay = hold_key[key]["delay"]

                    if self.time_out(start_time, delay):
                        detect_time = hold_key[key]["detect_time"]
                        skip_detect = hold_key[key]["skip_detect"]
                        if skip_detect:
                            skip_delay = hold_key[key]["skip_delay"]
                            if toggle_key in self.down_key_time and self.down_key_time[toggle_key]["scene"] != scene:
                                self.logger.print_log(f"已存在识别中的按键{toggle_key}，跳过不识别的检测")
                                self.finish_scence(scene)
                                return
                        self.logger.print_log(f"按下{key}超过{delay}ms，开始识别{detect_time}ms")
                        break
            if detect_time is not None:
                break
            time.sleep(0.001)

        start_time = time.time()
        detect_status = False
        if skip_delay > 0:
            time.sleep(skip_delay / 1000.0)

        while True:
            if not skip_detect or (skip_detect and click_state):
                select_name, score = self.dynamic_size_image_comparator.compare_with_path(
                    path=self.licking_state_path + scene + "/",
                    images=None,
                    lock_score=1,
                    discard_score=0.6)
                if score > 0.0:
                    detect_status = True
            else:
                select_name, score = "default", 1

            if not click_state:
                if score > 0.0:
                    click_state = True
                    down_key_time = time.time()
                    self.down_key_time[toggle_key] = {"down_key_time": down_key_time, "scene": scene}
                    MoverFactory.mouse_mover().key_down(Tools.convert_to_decimal(toggle_key))
                    self.logger.print_log(f"{scene}按下舔包键:{toggle_key}")
                else:
                    retry += 1
                    self.logger.print_log(f"{scene}未识别到，重试:{retry}")
                    if self.time_out(start_time, detect_time):
                        break
            elif click_state and score <= 0.0:
                if not skip_detect or (skip_detect and (detect_status or self.time_out(start_time, detect_time))):
                    if down_key_time == self.down_key_time[toggle_key]["down_key_time"]:
                        MoverFactory.mouse_mover().key_up(Tools.convert_to_decimal(toggle_key))
                        self.down_key_time.pop(toggle_key)
                        self.logger.print_log(f"{scene}松开舔包键:{toggle_key}")
                    else:
                        self.logger.print_log(f"{scene}跳过松开舔包键:{toggle_key}")
                    break
                else:
                    retry += 1
                    self.logger.print_log(f"{scene}未识别到，重试:{retry}")

        self.finish_scence(scene)

    def time_out(self, start_time, detect_time):
        return int((time.time() - start_time) * 1000) > detect_time

    def finish_scence(self, scene):
        self.threading_state_scene_map.pop(scene)
        self.logger.print_log(f"切换层结束场景{scene}的识别")
