import time

from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.mouse_controller import get_mouse_position, is_numlock_locked, set_mouse_position
from pynput.keyboard import Controller as KeyController, Key
from apex_yolov5.socket.config import global_config

intention = None
intention_handler = False
isRightKeyDown = False
isLeftKeyDown = False
mouseFlag = 0  # 0, 1 2 3
lock_mode = False  # don's edit this
step = 1
num_lock_pressed = True
keyboard = KeyController()
middle_toggle = False

change_coordinates_num = 0


def set_intention(x, y):
    global intention, change_coordinates_num
    # print("set_intention: {}".format((x, y)))
    (current_x, current_y) = get_mouse_position()
    # intention = ((x - current_x) * lock_move_speed, (y - current_y) * lock_move_speed)
    intention = ((x - current_x), (y - current_y))
    change_coordinates_num += 1


def get_lock_mode():
    # return True
    return lock_mode and num_lock_pressed and middle_toggle


def set_lock_mode(lock):
    global lock_mode
    lock_mode = lock


def start():
    global intention, intention_handler, change_coordinates_num
    while True:
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
        elif not lock_mode:
            intention = None
        time.sleep(0.01)
        change_coordinates_num = 0


def on_press(key):
    global num_lock_pressed

    try:
        # 检查按下的键是否为 Num Lock 键
        if key == Key.num_lock:
            num_lock_pressed = is_numlock_locked()
            print(f"Num Lock is {'ON' if num_lock_pressed else 'OFF'}")
    except AttributeError:
        pass


def on_click(x, y, button, pressed):
    global lock_mode, isLeftKeyDown, isRightKeyDown, mouseFlag, middle_toggle
    if pressed:
        if button == button.left:
            lock_mode = True
            isLeftKeyDown = True
        if button == button.right:
            lock_mode = True
            isRightKeyDown = True
        if button == button.middle:
            middle_toggle = not middle_toggle
    else:
        if button == button.left:
            isLeftKeyDown = False
        if button == button.right:
            isRightKeyDown = False
        if isLeftKeyDown or isRightKeyDown:
            lock_mode = True
        else:
            lock_mode = False


def on_move(x, y):
    # print("on_move: {}".format((x, y)))
    pass
