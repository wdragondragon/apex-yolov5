import math
import random
import traceback

from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.auxiliary import set_intention, set_click
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
        global_config.sign_shot_xy(0)
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

    averager = average_target_proportion(float(target_height))
    global_config.sign_shot_xy(averager)
    # if averager > 0.8:
    #     print(f"{averager}")
    #     global_config.increase_shot_xy()
    # elif averager < 0.2:
    #     print(f"{averager}")
    #     global_config.reduce_shot_xy()


def average_target_proportion(target_height):
    global target_proportion
    target_proportion.append(target_height)
    if len(target_proportion) > 40:
        target_proportion.pop(0)
    return calculate_average()


def calculate_average():
    global target_proportion
    if len(target_proportion) == 0:
        return 0  # 避免除以零错误
    return sum(target_proportion) / len(target_proportion)
