import math
import random
import traceback

import numpy as np

from PID import Pid
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.Tools import Tools
from apex_yolov5.auxiliary import set_intention, set_click, get_executed_intention
from apex_yolov5.socket.config import global_config
from apex_yolov5.windows.aim_show_window import get_aim_show_window

lock_time = 0
no_lock_time = 0

random_time = 0
random_float = 0.0

target_proportion = []


def lock(aims, mouse, screen_width, screen_height, shot_width, shot_height):
    global lock_time, no_lock_time, random_time, random_float
    # shot_width 截图高度，shot_height 截图区域高度
    # x,y 是分辨率
    # mouse_x,mouse_y = mouse.position
    current_mouse_x, current_mouse_y = mouse.position
    # current_mouse_x, current_mouse_y = global_config.screen_width // 2, global_config.screen_height // 2
    dist_list = []
    aims_copy = aims.copy()
    # print(aims_copy)
    aims_copy = [x for x in aims_copy if x[0] in global_config.lock_index]
    if len(aims_copy) == 0:
        if global_config.show_aim:
            get_aim_show_window().clear_box()
        global_config.sign_shot_xy()
        return
    for det in aims_copy:
        _, x_c, y_c, _, _ = det
        dist = (shot_width * float(x_c) - current_mouse_x) ** 2 + (shot_height * float(y_c) - current_mouse_y) ** 2
        dist_list.append(dist)
    det = aims_copy[dist_list.index(min(dist_list))]
    # print('当前鼠标坐标',mouse.position)
    tag, target_x, target_y, target_width, target_height = det
    # targetRealHeight = shot_height * float(target_height)
    targetShotX = shot_width * float(target_x)  # 目标在截图范围内的坐标
    targetShotY = shot_height * float(target_y)
    screenCenterX = screen_width // 2
    screenCenterY = screen_height // 2
    left_top_x, left_top_y = screenCenterX - shot_width // 2, screenCenterY - shot_height // 2  # 截图框的左上角坐标
    # tag, x_center, y_center, width, height = det
    width = shot_width * float(target_width)
    height = shot_height * float(target_height)

    targetRealX = left_top_x + targetShotX  # 目标在屏幕的坐标
    targetRealY = left_top_y + targetShotY - int(global_config.cross_hair / 2 * height)
    if global_config.show_aim:
        try:
            get_aim_show_window().update_box((left_top_x, left_top_y), det)
        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
    if apex_mouse_listener.get_aim_status():
        mouse_moving_radius = global_config.aim_mouse_moving_radius
    else:
        mouse_moving_radius = global_config.mouse_moving_radius
    if global_config.lead_time_toggle:
        targetRealX, targetRealY = lead_time(targetRealX, targetRealY, current_mouse_x, current_mouse_y)
    if (mouse_moving_radius ** 2 >
            (targetRealX - current_mouse_x) ** 2 + (targetRealY - current_mouse_y) ** 2):
        (x1, y1) = (left_top_x + (int(targetShotX - width / 2.0)), (left_top_y + int(targetShotY - height / 2.0)))
        (x2, y2) = (left_top_x + (int(targetShotX + width / 2.0)), (left_top_y + int(targetShotY + height / 2.0)))
        # 随机弹道计算
        if global_config.random_aim_toggle:
            random_coefficient = global_config.random_coefficient
            random_change_frequency = global_config.random_change_frequency
            if random_time > random_change_frequency:
                # 生成在 -random_x_deviation 到 random_x_deviation 之间的随机小数
                random_float = random.uniform(-random_coefficient, random_coefficient)
                random_time = 0
            else:
                random_time += 1

            # 保留小数点后两位
            random_float = round(random_float, 2)
            random_deviation = min(width / 2.0, height / 2.0)
            random_deviation = math.floor(random_float * random_deviation)
        else:
            random_deviation = 0

        # 漏枪逻辑cc
        if not global_config.intention_deviation_toggle:
            set_intention(targetRealX + random_deviation, targetRealY + random_deviation, current_mouse_x,
                          current_mouse_y, min(width / 2.0, height / 2.0))
            if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                set_click()
        else:
            # 先判断漏枪周期是否达到
            if lock_time < global_config.intention_deviation_interval:
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    lock_time += 1
                # 正常追踪
                set_intention(targetRealX + random_deviation, targetRealY + random_deviation, current_mouse_x,
                              current_mouse_y, min(width / 2.0, height / 2.0))
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    set_click()
            elif no_lock_time < global_config.intention_deviation_duration:
                no_lock_time += 1
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    targetRealX = x1 if float(target_x) > 0.5 else x2
                if global_config.intention_deviation_force:
                    set_intention(targetRealX, targetRealY, current_mouse_x, current_mouse_y,
                                  min(width / 2.0, height / 2.0))
            # 重置标记
            if lock_time == global_config.intention_deviation_interval and no_lock_time == global_config.intention_deviation_duration:
                lock_time = 0
                no_lock_time = 0

    target_width_origin, target_height_origin = float(
        target_width) * shot_width / global_config.default_shot_width, float(
        target_height) * shot_height / global_config.default_shot_height

    averager = *average_target_proportion(
        (float(target_width), float(target_height))), float(target_width_origin), float(target_height_origin)

    global_config.sign_shot_xy(averager)
    # if averager > 0.8:
    #     print(f"{averager}")
    #     global_config.increase_shot_xy()
    # elif averager < 0.2:
    #     print(f"{averager}")
    #     global_config.reduce_shot_xy()


def average_target_proportion(target_size):
    global target_proportion
    target_proportion.append(target_size)
    while len(target_proportion) > global_config.dynamic_screenshot_collection_window:
        target_proportion.pop(0)
    return calculate_average()


def calculate_average():
    global target_proportion
    if not target_proportion:
        return 0, 0  # 避免除以零错误
    if len(target_proportion) == 0:
        return 0, 0  # 避免除以零错误

    # 计算 x 和 y 的平均值
    average_x = sum(coord[0] for coord in target_proportion) / len(target_proportion)
    average_y = sum(coord[1] for coord in target_proportion) / len(target_proportion)

    return average_x, average_y


# 初始化 x 和 y 方向上的 PID 控制器
history_xy = Tools.FixedSizeQueue(100)
history_pid_xy = Tools.FixedSizeQueue(100)

history_move_xy = Tools.FixedSizeQueue(100)
history_executed_intention = Tools.FixedSizeQueue(100)
history_move_diff_queue = Tools.FixedSizeQueue(100)


def lead_time(targetRealX, targetRealY, current_mouse_x, current_mouse_y):
    move_x, move_y = targetRealX - current_mouse_x, targetRealY - current_mouse_y
    executed_intention_x, executed_intention_y = get_executed_intention()

    last_move = history_move_xy.get_last()
    if last_move is None:
        history_move_xy.push((move_x, move_y))
        history_executed_intention.push((executed_intention_x, executed_intention_y))
        print(
            f"first Actual Move: ({move_x}, {move_y}), Last Move: ({move_x},{move_y})")
        return targetRealX, targetRealY
    last_move_x, last_move_y = history_move_xy.get_last()
    history_move_xy.push((move_x, move_y))
    history_executed_intention.push((executed_intention_x, executed_intention_y))

    move_x_diff, move_y_diff = move_x + executed_intention_x - last_move_x, move_y + executed_intention_y - last_move_y
    history_move_diff_queue.push((move_x_diff, move_y_diff))
    # 移除之前的不同象限的移动
    current_quadrant = determine_quadrant(move_x, move_y)
    remove_previous_movements(history_move_diff_queue, current_quadrant)
    move_diff = history_move_diff_queue.get_last()
    if move_diff is None:
        print(f"move_diff is None")
        return targetRealX, targetRealY

    last_move = move_x + move_x_diff + current_mouse_x, move_y + move_y_diff + current_mouse_y
    print(f"move diff:({move_x_diff, move_y_diff})")
    print(f"Actual Move: ({move_x}, {move_y}), Last Move: ({move_x + move_x_diff},{move_y + move_y_diff})")
    return last_move


def pid(targetRealX, targetRealY, current_mouse_x, current_mouse_y):
    move_x, move_y = targetRealX - current_mouse_x, targetRealY - current_mouse_y
    current_quadrant = determine_quadrant(move_x, move_y)

    # 移除之前的不同象限的移动
    remove_previous_movements(history_xy, current_quadrant)
    history_xy.push((move_x, move_y))

    # 判断是否达到队列长度要求
    if len(history_xy.queue) < 15:
        return targetRealX, targetRealY

    pid_controller_x = Pid(kp=0.2, ki=0.03, kd=0.15)
    pid_controller_y = Pid(kp=0.1, ki=0.01, kd=0.1)

    # 从队列的尾部开始，每隔10个历史记录点进行一次 PID 控制计算
    # 计算 PID 控制
    pid_x, pid_y = 0, 0
    for move_x, move_y in history_xy.queue:
        pid_x = pid_controller_x.cmd_pid(move_x)
        pid_y = pid_controller_y.cmd_pid(move_y)

    # 记录预测轨迹
    last_pid_xy = history_pid_xy.get_last()
    if last_pid_xy is not None:
        x, y = last_pid_xy
        print(
            f"Actual Trajectory: ({move_x}, {move_y}), Predicted Trajectory: ({x}, {y})")

    # 将 PID 输出添加到历史队列
    history_pid_xy.push((pid_x, pid_y))

    for i in range(40):
        pid_x = pid_controller_x.cmd_pid(pid_x)
        pid_y = pid_controller_y.cmd_pid(pid_y)
    print(
        f"Actual Move: ({move_x}, {move_y}), Last Move: ({pid_x}, {pid_y})")
    return pid_x + current_mouse_x, pid_y + current_mouse_y


def remove_previous_movements(queue, current_quadrant):
    # 从队列中移除之前的不同象限的移动
    index_to_remove = -1
    for i, (prev_move_x, prev_move_y) in enumerate(queue.queue):
        prev_quadrant = determine_quadrant(prev_move_x, prev_move_y)
        if prev_quadrant != current_quadrant:
            index_to_remove = i
        else:
            break

    if index_to_remove >= 0:
        for _ in range(index_to_remove + 1):
            queue.queue.popleft()


def determine_quadrant(move_x, move_y):
    # 确定移动所在的象限
    if move_x >= 0 and move_y >= 0:
        return 1
    elif move_x < 0 <= move_y:
        return 2
    elif move_x < 0 and move_y < 0:
        return 3
    elif move_x >= 0 > move_y:
        return 4
    else:
        return 0  # 处理移动为原点的情况
