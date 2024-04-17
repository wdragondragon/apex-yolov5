from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.auxiliary import set_intention
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
    current_mouse_x, current_mouse_y = mouse.position
    dist_list = []
    aims_copy = aims.copy()
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
    tag, target_x, target_y, target_width, target_height = det
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

    if in_moving_raduis(targetRealX, targetRealY, shot_width, shot_height, current_mouse_x, current_mouse_y):
        set_intention(targetRealX - current_mouse_x, targetRealY - current_mouse_y)
    return 0, 0, 0, 0


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
