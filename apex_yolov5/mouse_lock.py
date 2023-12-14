from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.auxiliary import set_intention, set_click
from apex_yolov5.socket.config import global_config

lock_time = 0
no_lock_time = 0


def lock(aims, mouse, screen_width, screen_height, shot_width, shot_height):
    global lock_time, no_lock_time
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

    if apex_mouse_listener.get_aim_status():
        mouse_moving_radius = global_config.aim_mouse_moving_radius
    else:
        mouse_moving_radius = global_config.mouse_moving_radius

    if (mouse_moving_radius ** 2 >
            (targetRealX - current_mouse_x) ** 2 + (targetRealY - current_mouse_y) ** 2):
        (x1, y1) = (left_top_x + (int(targetShotX - width / 2.0)), (left_top_y + int(targetShotY - height / 2.0)))
        (x2, y2) = (left_top_x + (int(targetShotX + width / 2.0)), (left_top_y + int(targetShotY + height / 2.0)))
        if not global_config.intention_deviation_toggle:
            set_intention(targetRealX, targetRealY, current_mouse_x, current_mouse_y)
            if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                set_click()
        else:
            # 先判断漏枪周期是否达到
            if lock_time < global_config.intention_deviation_interval:
                lock_time += 1
                # 正常追踪
                set_intention(targetRealX, targetRealY, current_mouse_x, current_mouse_y)
                if x1 < screenCenterX < x2 and y1 < screenCenterY < y2:
                    set_click()
            elif no_lock_time < global_config.intention_deviation_duration:
                no_lock_time += 1
                if global_config.intention_deviation_force:
                    set_intention(x1 if float(target_x) > 0.5 else x2, targetRealY, current_mouse_x, current_mouse_y)
            # 重置标记
            if lock_time == global_config.intention_deviation_interval and no_lock_time == global_config.intention_deviation_duration:
                lock_time = 0
                no_lock_time = 0
