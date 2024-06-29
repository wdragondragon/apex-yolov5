import math
import random
import threading
import time
import traceback

from pynput.mouse import Button

from apex_recoils.core import SelectGun
from apex_yolov5.job_listener.JoyListener import get_joy_listener
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_recoils.core.SelectGun import get_select_gun
from apex_yolov5.Tools import Tools
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import global_config

intention = None
executed_intention = (0, 0)
real_intention = (0, 0)
intention_base_sign = 0
change_coordinates_num = 0

last_click_time = 0
click_interval = 0.01
click_sign = False

block_queue = Tools.GetBlockQueue(name='auxiliary_queue')
intention_lock = threading.Lock()
intention_exec_sign = False


def set_intention(x, y, lead_x, lead_y, random_deviation, base_sign=0, move_path_n=True):
    global intention, change_coordinates_num, intention_base_sign, executed_intention, real_intention
    intention_lock.acquire()
    try:
        intention_base_sign = base_sign
        if move_path_n:
            if apex_mouse_listener.get_aim_status():
                x = x * global_config.aim_move_path_nx
                y = y * global_config.aim_move_path_ny
                random_deviation_x = random_deviation * global_config.aim_move_path_nx
                random_deviation_y = random_deviation * global_config.aim_move_path_ny
            else:
                x = x * global_config.move_path_nx
                y = y * global_config.move_path_ny
                random_deviation_x = random_deviation * global_config.move_path_nx
                random_deviation_y = random_deviation * global_config.move_path_ny
        else:
            random_deviation_x = random_deviation
            random_deviation_y = random_deviation
        intention = (x + random_deviation_x + lead_x, y + random_deviation_y + lead_y)
        real_intention = (x, y)
        executed_intention = (0, 0)
        change_coordinates_num += 1
        if not intention_exec_sign:
            block_queue.put(True)
    finally:
        # 释放锁
        intention_lock.release()


def get_intention():
    return intention


def incr_executed_intention(move_x, move_y):
    global executed_intention
    real_intention_x, real_intention_y = real_intention
    executed_intention_x, executed_intention_y = executed_intention
    # if abs(executed_intention_x + move_x) < abs(real_intention_x):
    executed_intention_x = executed_intention_x + move_x
    # else:
    #     executed_intention_x = real_intention_x

    # if abs(executed_intention_y + move_y) < abs(real_intention_y):
    executed_intention_x = executed_intention_y + move_y
    # else:
    #     executed_intention_y = real_intention_y

    executed_intention = executed_intention_x, executed_intention_y


def get_executed_intention():
    return executed_intention


def set_click():
    global click_sign
    click_sign = True


lock_time = None
move_x_arr = []
move_y_arr = []
time_point_arr = []

lock_delay = 0


def get_lock_mode():
    global lock_time, lock_delay
    mouse_fire = apex_mouse_listener.is_press(Button.left)
    controller_fire = get_joy_listener().is_press(4)
    mouse_aim = apex_mouse_listener.is_press(Button.right)
    controller_aim = get_joy_listener().is_press(5)
    mouse_only_fire = apex_mouse_listener.is_press(Button.left) and not apex_mouse_listener.is_press(Button.right)
    controller_only_fire = get_joy_listener().is_press(4) and not get_joy_listener().is_press(5)
    no_lock = global_config.base_scope_no_aim and SelectGun.get_select_gun().real_current_scope is None
    fire, aim, only_fire = (controller_fire, controller_aim, controller_only_fire) \
        if global_config.joy_move \
        else (mouse_fire, mouse_aim, mouse_only_fire)
    lock_mode = (
            ("left" in global_config.aim_button and fire) or
            ("right" in global_config.aim_button and aim) or
            ("x2" in global_config.aim_button and apex_mouse_listener.is_press(Button.x2)) or
            ("x1" in global_config.aim_button and apex_mouse_listener.is_press(Button.x1)) or
            ("x1&!x2" in global_config.aim_button and only_fire)
    )
    lock_mode = lock_mode or len(global_config.aim_button) == 0
    lock = lock_mode and global_config.ai_toggle and not (no_lock and aim)
    if lock:
        if lock_time is None:
            lock_time = time.time()
            if global_config.aiming_delay_min == global_config.aiming_delay_max:
                lock_delay = global_config.aiming_delay_min
            else:
                lock_delay = random.randint(global_config.aiming_delay_min, global_config.aiming_delay_max)
            move_x_arr.clear()
            move_y_arr.clear()
            time_point_arr.clear()
    else:
        if lock_time is not None:
            lock_time = None
            lock_delay = 0
            if len(time_point_arr) > 0:
                LogFactory.logger().print_log(move_x_arr)
                LogFactory.logger().print_log(move_y_arr)
                LogFactory.logger().print_log(time_point_arr)
    return lock


def get_lock_mode_shoot():
    return get_lock_mode() and lock_delay <= int((time.time() - lock_time) * 1000)


def start():
    global intention, change_coordinates_num, last_click_time, click_sign, intention_exec_sign, lock_time
    sum_move_x, sum_move_y = 0, 0
    start_time = time.time()
    while_frequency = 0
    while True:
        # sleep_time = 0.01
        block_queue.get()
        intention_exec_sign = True
        if click_sign and time.time() - last_click_time > click_interval and get_select_gun().current_gun in global_config.click_gun:
            MoverFactory.mouse_mover().left_click()
            last_click_time = time.time()
            click_sign = False
        elif global_config.auto_charged_energy and get_select_gun().current_gun == '充能步枪' and time.time() - last_click_time > global_config.storage_interval and not apex_key_listener.is_open(
                global_config.auto_charged_energy_toggle):
            MoverFactory.mouse_mover().left_click()
            last_click_time = time.time()
        lock_mode_shoot = get_lock_mode_shoot()
        if lock_mode_shoot and intention is not None:
            # t0 = time.time()
            (x, y) = intention
            if (global_config.mouse_model in global_config.available_mouse_smoothing
                    and global_config.mouse_smoothing_switch):
                # print("开始移动，移动距离:{}".format((x, y)))
                while (x != 0 or y != 0) and get_lock_mode_shoot():
                    intention_lock.acquire()
                    try:
                        (x, y) = intention
                        if apex_mouse_listener.is_press(Button.right):
                            move_step_temp, move_step_y_temp = random_move(x, y,
                                                                           (global_config.aim_move_step,
                                                                            global_config.aim_move_step_y),
                                                                           (global_config.aim_move_step_max,
                                                                            global_config.aim_move_step_y_max))
                        else:
                            move_step_temp, move_step_y_temp = random_move(x, y,
                                                                           (global_config.move_step,
                                                                            global_config.move_step_y),
                                                                           (global_config.move_step_max,
                                                                            global_config.move_step_y_max))

                        if global_config.dynamic_mouse_move:
                            move_step_temp = max(apex_mouse_listener.move_avg_x, move_step_temp)
                            move_step_y_temp = max(apex_mouse_listener.move_avg_y, move_step_y_temp)

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
                        intention, move_up, move_down = split_coordinate(x, y, move_step_temp, move_step_y_temp)
                        incr_executed_intention(move_up, move_down)
                    finally:
                        # 释放锁
                        intention_lock.release()
                    try:
                        MoverFactory.mouse_mover().move_rp(int(move_up), int(move_down), global_config.re_cut_size)
                    except Exception as e:
                        print(e)
                        traceback.print_exception(e)
                    sum_move_x, sum_move_y = sum_move_x + abs(move_up), sum_move_y + abs(move_down)
                    if not global_config.ai_toggle:
                        break
                    if not global_config.mouse_move_frequency_switch:
                        time.sleep(global_config.mouse_move_frequency)
                # cost_time = int((time.time() - t0) * 1000)
                # print(
                #     "完成移动时间:{:.2f}ms,坐标变更次数:{}".format(cost_time, change_coordinates_num))
            else:
                # print("开始移动，移动距离:{}".format((x, y)))
                x, y = int(round(x, 0)), int(round(y, 0))
                move_x_arr.append(x)
                move_y_arr.append(y)
                time_point_arr.append(int((time.time() - lock_time) * 1000))
                MoverFactory.mouse_mover().move(x, y)
                incr_executed_intention(x, y)
                # print(
                #     "完成移动时间:{:.2f}ms,坐标变更次数:{}".format((time.time() - t0) * 1000, change_coordinates_num))
            intention = None
            # sleep_time = 0.001
        elif not lock_mode_shoot:
            intention = None
        while_frequency += 1
        if int((time.time() - start_time) * 1000) > 1000:
            LogFactory.logger().print_log(f"鼠标移动频率为：{while_frequency}")
            while_frequency = 0
            start_time = time.time()
        change_coordinates_num = 0
        intention_exec_sign = False
        # time.sleep(sleep_time)


def random_move(x, y, move_step, move_step_max, move_optimization=True):
    """
        随机移动方法
    :param x:
    :param y:
    :param move_step:
    :param move_step_max
    :param move_optimization
    :return:
    """
    move_step_temp, move_step_y_temp = move_step
    move_step_temp_max, move_step_y_temp_max = move_step_max

    move_step, move_step_y = (random.randint(move_step_temp, move_step_temp_max),
                              random.randint(move_step_y_temp, move_step_y_temp_max))
    if move_optimization and x > 0 and y > 0:
        x_moving_ratio = x / y
        if x_moving_ratio <= 0.5:
            random_number = random.random()
            if x_moving_ratio > random_number:
                move_step = 1
            else:
                move_step = 0
        elif x_moving_ratio >= 2:
            y_moving_ratio = y / x
            random_number = random.random()
            if y_moving_ratio > random_number:
                move_step_y = 1
            else:
                move_step_y = 0
    return move_step, move_step_y


def split_coordinate(x, y, move_step_temp, move_step_y_temp):
    move_up = min(move_step_temp, abs(x)) * (1 if x > 0 else -1)
    move_down = min(move_step_y_temp, abs(y)) * (1 if y > 0 else -1)
    if x == 0:
        move_up = 0
    elif y == 0:
        move_down = 0
    x -= move_up
    y -= move_down
    return (x, y), move_up, move_down


def calculate_distance(x, y):
    distance = math.sqrt(x ** 2 + y ** 2)
    # 将结果取整，如果为0则取1
    return max(1, round(distance))


def find_range_index(ranges, num):
    for i, range_arr in enumerate(ranges):
        for (start_num, end) in range_arr:
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
    for i, range_arr in enumerate(ranges):
        for (start_num, end) in range_arr:
            if start_num * intention_base_sign <= num <= end * intention_base_sign:
                return i
    return None
