import math
import random
import traceback

from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.Tools import Tools
from apex_yolov5.auxiliary import set_intention, set_click, get_executed_intention
from apex_yolov5.socket.config import global_config
from apex_yolov5.windows.aim_show_window import get_aim_show_window
from apex_yolov5.windows.circle_window import get_circle_window

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
        return 0, 0, 0, 0
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

    if in_moving_raduis(targetRealX, targetRealY, shot_width, shot_height, current_mouse_x, current_mouse_y) and \
            not in_delayed(width, height, targetRealX, targetRealY, screenCenterX, screenCenterY):
        if global_config.lead_time_toggle:
            targetRealX, targetRealY = lead_time_xy(targetRealX, targetRealY, current_mouse_x, current_mouse_y,
                                                    global_config.lead_time_frame,
                                                    global_config.lead_time_decision_frame)
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
            set_intention(targetRealX - current_mouse_x, targetRealY - current_mouse_y, random_deviation,
                          min(width / 2.0, height / 2.0))
            if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                set_click()
        else:
            # 先判断漏枪周期是否达到
            if lock_time < global_config.intention_deviation_interval:
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    lock_time += 1
                # 正常追踪
                set_intention(targetRealX - current_mouse_x, targetRealY - current_mouse_y, random_deviation,
                              min(width / 2.0, height / 2.0))
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    set_click()
            elif no_lock_time < global_config.intention_deviation_duration:
                no_lock_time += 1
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    targetRealX = x1 if float(target_x) > 0.5 else x2
                if global_config.intention_deviation_force:
                    set_intention(targetRealX - current_mouse_x, targetRealY - current_mouse_y, random_deviation,
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
    return averager


def in_moving_raduis(targetRealX, targetRealY, shot_width, shot_height, current_mouse_x, current_mouse_y):
    if apex_mouse_listener.get_aim_status():
        mouse_moving_radius = global_config.aim_mouse_moving_radius
    else:
        mouse_moving_radius = global_config.mouse_moving_radius

    mouse_moving_radius = round(mouse_moving_radius * max(shot_width / global_config.default_shot_width,
                                                          shot_height / global_config.default_shot_height), 2)
    if global_config.show_circle:
        get_circle_window().update_circle_auto_change(mouse_moving_radius)
    return (mouse_moving_radius ** 2 >
            (targetRealX - current_mouse_x) ** 2 + (targetRealY - current_mouse_y) ** 2)


def in_delayed(width, height, targetRealX, targetRealY, screenCenterX, screenCenterY):
    if not global_config.delayed_aiming:
        return False
    delayed_width = width / 2.0 * global_config.delayed_aiming_factor_x
    delayed_height = height / 2.0 * global_config.delayed_aiming_factor_y
    delayed_aiming_xy1 = int(targetRealX - delayed_width), int(targetRealY - delayed_height)
    delayed_aiming_xy2 = int(targetRealX + delayed_width), int(targetRealY + delayed_height)
    return delayed_aiming_xy1[0] < screenCenterX < delayed_aiming_xy2[0] and \
        delayed_aiming_xy1[1] < screenCenterY < delayed_aiming_xy2[1]


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


history_move_x_queue = Tools.FixedSizeQueue(100)
history_executed_intention_x_queue = Tools.FixedSizeQueue(100)
history_move_diff_x_queue = Tools.FixedSizeQueue(100)

history_move_y_queue = Tools.FixedSizeQueue(100)
history_executed_intention_y_queue = Tools.FixedSizeQueue(100)
history_move_diff_y_queue = Tools.FixedSizeQueue(100)


def lead_time_xy(targetRealX, targetRealY, current_mouse_x, current_mouse_y, lead_time_frame, lead_time_decision_frame):
    executed_intention_x, executed_intention_y = get_executed_intention()
    return (lead_time_one('x', targetRealX,
                          current_mouse_x,
                          executed_intention_x,
                          lead_time_frame,
                          lead_time_decision_frame,
                          history_move_x_queue,
                          history_executed_intention_x_queue,
                          history_move_diff_x_queue),
            lead_time_one('y', targetRealY,
                          current_mouse_y,
                          executed_intention_y,
                          lead_time_frame,
                          lead_time_decision_frame,
                          history_move_y_queue,
                          history_executed_intention_y_queue,
                          history_move_diff_y_queue))


def lead_time_one(name, target_real,
                  current_mouse,
                  executed_intention,
                  lead_time_frame,
                  lead_time_decision_frame,
                  history_move_queue,
                  history_executed_intention_queue,
                  history_move_diff_queue):
    move = target_real - current_mouse

    last_move = history_move_queue.get_last()
    if last_move is None:
        history_move_queue.push(move)
        history_executed_intention_queue.push(executed_intention)
        return target_real
    last_move = history_move_queue.get_last()
    history_move_queue.push(move)
    history_executed_intention_queue.push(executed_intention)

    move_diff = move + executed_intention - last_move
    history_move_diff_queue.push(move_diff)
    # 移除之前的不同象限的移动
    current_quadrant = determine_quadrant(move_diff)
    lead_time = previous_movements(history_move_diff_queue, current_quadrant, lead_time_decision_frame)
    move_diff = history_move_diff_queue.get_last()
    if (not lead_time) or move_diff is None or abs(move_diff) < 10:
        return target_real

    last_move = move + executed_intention * lead_time_frame + current_mouse
    print(f"{name} move diff:({move_diff}) move intention:({executed_intention})")
    print(f"{name} Actual Move: ({move}), Last Move: ({move + executed_intention * lead_time_frame})")
    return last_move


def previous_movements(queue, current_quadrant, lead_time_decision_frame):
    # 从队列中移除之前的不同象限的移动
    return True
    # remove_num = 0
    # keep_num = 0
    # for i in range(len(queue.queue) - 1, -1, -1):
    #     prev_move = queue.queue[i]
    #     prev_quadrant = determine_quadrant(prev_move)
    #     if prev_quadrant == current_quadrant:
    #         remove_num = 0
    #         keep_num += 1
    #         if keep_num >= lead_time_decision_frame:
    #             return True
    #     else:
    #         remove_num += 1
    #         keep_num = 0
    #         if remove_num >= 5:
    #             return False
    # return keep_num >= lead_time_decision_frame


def determine_quadrant(move):
    # 确定移动所在的象限
    if move >= 0:
        return 1
    elif move <= 0:
        return -1
