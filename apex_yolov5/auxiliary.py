import math
import threading
import time
import traceback

from pynput.mouse import Button

from apex_yolov5.job_listener.JoyListener import get_joy_listener
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_recoils.core.SelectGun import get_select_gun
from apex_yolov5.Tools import Tools
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import global_config

intention = None

last_click_time = 0
click_interval = 0.01
click_sign = False

block_queue = Tools.GetBlockQueue(name='auxiliary_queue')
intention_lock = threading.Lock()
intention_exec_sign = False


def set_intention(x, y):
    global intention
    intention_lock.acquire()
    try:
        if get_lock_mode():
            x, y = int(round(x, 0)), int(round(y, 0))
            time_point_arr.append(int((time.time() - lock_time) * 1000))
            move_x_arr.append(x)
            move_y_arr.append(y)
            MoverFactory.mouse_mover().move(x, y)
    finally:
        # 释放锁
        intention_lock.release()


def set_click():
    global click_sign
    click_sign = True


lock_time = None
move_x_arr = []
move_y_arr = []
time_point_arr = []


def get_lock_mode():
    global lock_time
    lock_mode = (("left" in global_config.aim_button and (
            apex_mouse_listener.is_press(Button.left) or get_joy_listener().is_press(4))) or
                 ("right" in global_config.aim_button and (
                         apex_mouse_listener.is_press(Button.right) or get_joy_listener().is_press(5))) or
                 ("x2" in global_config.aim_button and apex_mouse_listener.is_press(Button.x2)) or
                 ("x1" in global_config.aim_button and apex_mouse_listener.is_press(Button.x1)) or
                 ("x1&!x2" in global_config.aim_button and ((
                                                                    apex_mouse_listener.is_press(
                                                                        Button.left) and not apex_mouse_listener.is_press(
                                                                Button.right)) or (get_joy_listener().is_press(
                     4) and not get_joy_listener().is_press(5))))
                 )
    lock_mode = lock_mode or len(global_config.aim_button) == 0
    lock = lock_mode and global_config.ai_toggle
    if lock:
        if lock_time is None:
            lock_time = time.time()
            move_x_arr.clear()
            move_y_arr.clear()
            time_point_arr.clear()
    else:
        if lock_time is not None:
            lock_time = None
            print(f'"time_points": {time_point_arr},')
            print(f'"x": {move_x_arr},')
            print(f'"y": {move_y_arr}')
    return lock
