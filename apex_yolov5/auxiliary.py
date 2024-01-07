import math
import threading
import time

from pynput.mouse import Button

from apex_yolov5.JoyListener import joy_listener
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.ScreenUtil import select_gun
from apex_yolov5.mouse_controller import set_mouse_position, set_mouse_position_rp, left_click
from apex_yolov5.socket.config import global_config

intention = None
executed_intention = (0, 0)
intention_base_sign = 0
change_coordinates_num = 0

last_click_time = 0
click_interval = 0.01
click_sign = False

intention_lock = threading.Lock()


def set_intention(x, y, current_x, current_y, base_sign=0):
    global intention, change_coordinates_num, intention_base_sign, executed_intention
    intention_lock.acquire()
    try:
        intention_base_sign = base_sign
        if apex_mouse_listener.get_aim_status():
            intention = (
                (x - current_x) * global_config.aim_move_path_nx, (y - current_y) * global_config.aim_move_path_ny)
        else:
            intention = ((x - current_x) * global_config.move_path_nx, (y - current_y) * global_config.move_path_ny)
        executed_intention = (0, 0)
        change_coordinates_num += 1
    finally:
        # 释放锁
        intention_lock.release()


def incr_executed_intention(move_x, move_y):
    global executed_intention
    executed_intention_x, executed_intention_y = executed_intention
    executed_intention = executed_intention_x + move_x, executed_intention_y + move_y


def get_executed_intention():
    return executed_intention


def set_click():
    global click_sign
    click_sign = True


def get_lock_mode():
    lock_mode = (("left" in global_config.aim_button and (
            apex_mouse_listener.is_press(Button.left) or joy_listener.is_press(4))) or
                 ("right" in global_config.aim_button and (
                         apex_mouse_listener.is_press(Button.right) or joy_listener.is_press(5))) or
                 ("x2" in global_config.aim_button and apex_mouse_listener.is_press(Button.x2)) or
                 ("x1" in global_config.aim_button and apex_mouse_listener.is_press(Button.x1)) or
                 ("x1&!x2" in global_config.aim_button and ((
                                                                    apex_mouse_listener.is_press(
                                                                        Button.left) and not apex_mouse_listener.is_press(
                                                                Button.right)) or (joy_listener.is_press(
                     4) and not joy_listener.is_press(5))))
                 )
    lock_mode = lock_mode or len(global_config.aim_button) == 0
    return lock_mode and global_config.ai_toggle


def start():
    global intention, change_coordinates_num, last_click_time, click_sign
    while True:
        if click_sign and time.time() - last_click_time > click_interval and select_gun.current_gun in global_config.click_gun:
            left_click()
            last_click_time = time.time()
            click_sign = False
        elif global_config.auto_charged_energy and select_gun.current_gun == '充能步枪' and time.time() - last_click_time > global_config.storage_interval and not apex_key_listener.is_open(
                global_config.auto_charged_energy_toggle):
            left_click()
            last_click_time = time.time()

        if get_lock_mode() and intention is not None:
            # t0 = time.time()
            (x, y) = intention
            if (global_config.mouse_model in global_config.available_mouse_smoothing
                    and global_config.mouse_smoothing_switch):
                # print("开始移动，移动距离:{}".format((x, y)))
                while (x != 0 or y != 0) and get_lock_mode():
                    intention_lock.acquire()
                    try:
                        (x, y) = intention
                        move_step_temp = global_config.aim_move_step if apex_mouse_listener.is_press(
                            Button.right) else global_config.move_step
                        move_step_y_temp = global_config.aim_move_step_y if apex_mouse_listener.is_press(
                            Button.right) else global_config.move_step_y

                        # 多级瞄速计算
                        if global_config.multi_stage_aiming_speed_toggle:
                            multi_stage_aiming_speed = global_config.aim_multi_stage_aiming_speed \
                                if apex_mouse_listener.is_press(
                                Button.right) else global_config.multi_stage_aiming_speed
                            move_step_temp = calculate_percentage_value(multi_stage_aiming_speed, x, move_step_temp,
                                                                        global_config.based_on_character_box)
                            move_step_y_temp = calculate_percentage_value(multi_stage_aiming_speed, y, move_step_y_temp,
                                                                          global_config.based_on_character_box)
                        # print(str(move_step_temp) + ":" + str(move_step_y_temp))
                        move_up = min(move_step_temp, abs(x)) * (1 if x > 0 else -1)
                        move_down = min(move_step_y_temp, abs(y)) * (1 if y > 0 else -1)
                        if x == 0:
                            move_up = 0
                        elif y == 0:
                            move_down = 0
                        x -= move_up
                        y -= move_down
                        intention = (x, y)
                        incr_executed_intention(move_up, move_down)
                    finally:
                        # 释放锁
                        intention_lock.release()
                    set_mouse_position_rp(int(move_up), int(move_down))
                    if not global_config.ai_toggle:
                        break
                    if not global_config.mouse_move_frequency_switch:
                        time.sleep(global_config.mouse_move_frequency)
                # print(
                #     "完成移动时间:{:.2f}ms,坐标变更次数:{}".format((time.time() - t0) * 1000, change_coordinates_num))
            else:
                # print("开始移动，移动距离:{}".format((x, y)))
                set_mouse_position(int(x), int(y))
                # print(
                #     "完成移动时间:{:.2f}ms,坐标变更次数:{}".format((time.time() - t0) * 1000, change_coordinates_num))
            intention = None
        elif not get_lock_mode():
            intention = None
        time.sleep(0.01)
        change_coordinates_num = 0


def calculate_distance(x, y):
    distance = math.sqrt(x ** 2 + y ** 2)
    # 将结果取整，如果为0则取1
    return max(1, round(distance))


def find_range_index(ranges, num):
    for i, (start_num, end) in enumerate(ranges):
        if start_num <= num <= end:
            return i
    return None


def calculate_percentage_value(arr, m, n, based_on_character_box):
    if not arr:
        return n
    arr_length = len(arr)
    if not based_on_character_box:
        index = find_range_index(arr, m)
    else:
        index = find_range_index_2(arr, m)
    if index is not None:
        # 计算 m 在数组中的下标 i 占整个数组长度的百分比
        percentage = (index + 1) / arr_length
        # 用 n 乘以百分比
        result = round(n * percentage)
        return max(1, result)
    else:
        return n


def find_range_index_2(ranges, num):
    for i, (start_num, end) in enumerate(ranges):
        if start_num * intention_base_sign <= num <= end * intention_base_sign:
            return i
    return None
