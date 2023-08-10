import time

from pynput.mouse import Button

from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
from apex_yolov5.ScreenUtil import select_gun
from apex_yolov5.mouse_controller import get_mouse_position, set_mouse_position, left_click
from apex_yolov5.socket.config import global_config

intention = None
intention_handler = False
step = global_config.move_step
change_coordinates_num = 0

last_click_time = 0
click_interval = 0.1
click_sign = False


def set_intention(x, y):
    global intention, change_coordinates_num
    # print("set_intention: {}".format((x, y)))
    (current_x, current_y) = get_mouse_position()
    # intention = ((x - current_x) * lock_move_speed, (y - current_y) * lock_move_speed)
    intention = ((x - current_x), (y - current_y))
    change_coordinates_num += 1


def set_click():
    global click_sign
    click_sign = True


def get_lock_mode():
    lock_mode = apex_mouse_listener.is_press(Button.left) or apex_mouse_listener.is_press(
        Button.right) or apex_mouse_listener.is_press(Button.x2)
    return (lock_mode and apex_mouse_listener.middle_toggle) or select_gun.current_gun in global_config.click_gun


def start():
    global intention, intention_handler, change_coordinates_num, last_click_time, click_sign
    while True:
        if click_sign and time.time() - last_click_time > click_interval and select_gun.current_gun in global_config.click_gun:
            left_click()
            last_click_time = time.time()
            click_sign = False
        if get_lock_mode() and intention is not None:
            t0 = time.time()
            (x, y) = intention
            # LogWindow().print_log("开始移动，移动距离:{}".format((x, y)))
            while x != 0 or y != 0:
                (x, y) = intention
                move_up = min(step, abs(x)) * (1 if x > 0 else -1)
                move_down = min(step, abs(y)) * (1 if y > 0 else -1)
                if x == 0:
                    move_up = 0
                elif y == 0:
                    move_down = 0
                x -= move_up
                y -= move_down
                intention = (x, y)
                set_mouse_position(int(move_up * global_config.lock_move_speed),
                                   int(move_down * global_config.lock_move_speed))
                time.sleep(0.001)
            intention = None
            # LogWindow().print_log(
            #     "完成移动时间:{:.2f}ms,坐标变更次数:{}".format((time.time() - t0) * 1000, change_coordinates_num))
        elif not get_lock_mode():
            intention = None
        time.sleep(0.01)
        change_coordinates_num = 0