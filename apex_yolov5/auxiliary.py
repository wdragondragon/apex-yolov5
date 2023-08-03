import time
from apex_yolov5.mouse_controller import *
from pynput.keyboard import Controller as KeyController, Key

intention = None
intention_handler = False
isRightKeyDown = False
isLeftKeyDown = False
mouseFlag = 0  # 0, 1 2 3
lock_mode = False  # don's edit this
step = 5
num_lock_pressed = False
keyboard = KeyController()


def set_intention(x, y):
    global intention
    # print("set_intention: {}".format((x, y)))
    intention = (x, y)


def get_lock_mode():
    return lock_mode and num_lock_pressed


def set_lock_mode(lock):
    global lock_mode
    lock_mode = lock


def start():
    global intention, intention_handler
    while True:
        if lock_mode and num_lock_pressed and intention is not None:
            (current_x, current_y) = get_mouse_position()
            x = intention[0] - current_x
            y = intention[1] - current_y
            # step_x = step
            # step_y = step
            # if step > abs(x):
            #     step_x = x
            # elif x < 0:
            #     step_x = -step
            # if step > abs(y):
            #     step_y = y
            # elif y < 0:
            #     step_y = -step
            # set_mouse_position(int(step_x), int(step_y))
            set_mouse_position(int(x), int(y))
            intention = None
        elif not lock_mode:
            intention = None
        time.sleep(0.01)


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
    global lock_mode, isLeftKeyDown, isRightKeyDown, mouseFlag
    if pressed:
        if button == button.left:
            lock_mode = True
            isLeftKeyDown = True
        if button == button.right:
            lock_mode = True
            isRightKeyDown = True
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
