import time

import win32api
import win32con

from apex_yolov5.auxiliary import set_intention
from apex_yolov5.socket.config import global_config


def mouse_To1(des_X, des_Y, current_mouse_x=0, current_mouse_y=0):
    up = des_X - current_mouse_x
    down = des_Y - current_mouse_y
    up = int(up)
    down = int(down)

    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, up, down)
    # 计算移动的单位数
    move_up = min(1, abs(up)) * (1 if up > 0 else -1)
    move_down = min(1, abs(down)) * (1 if down > 0 else -1)
    t0 = time.time()
    while up != 0 or down != 0:
        time.sleep(0.00001)
        if up == 0:
            move_up = 0
        elif down == 0:
            move_down = 0
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_up, move_down)
        up -= move_up
        down -= move_down
        # print("up: {}, down: {}".format(up, down))
    print("完成移动时间：{}ms".format((time.time() - t0) * 1000))
    # pyautogui.moveRel(up, down, duration=0.1)


def mouse_To(des_X, des_Y, current_mouse_x=0, current_mouse_y=0):
    # 效果不好
    up = des_X - current_mouse_x
    down = des_Y - current_mouse_y
    if up == 0 and down == 0:
        return
    up = int(up)
    down = int(down)
    movingUp = up // 2
    movingDown = down // 2
    abs_up = up if up > 0 else -up
    abs_down = down if down > 0 else -down
    Max = max(abs_down, abs_up)
    ite = Max
    for i in range(ite):
        if (2 ** i) > Max:
            break
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, movingUp, movingDown)
        movingUp = movingUp // 2
        movingDown = movingDown // 2

    # mouse_xy(int(up),int(down))
    # des_Y = int(des_Y)
    # des_X = int(des_X)
    # pydirectinput.moveTo(int(des_X),int(des_Y))


def lock(aims, mouse, screen_width, screen_height, shot_width, shot_height):
    # shot_width 截图高度，shot_height 截图区域高度
    # x,y 是分辨率
    # mouse_x,mouse_y = mouse.position

    current_mouse_x = screen_width / 2  # 当前鼠标坐标，为屏幕中心
    current_mouse_y = screen_height / 2  # 同上
    current_mouse_x, current_mouse_y = mouse.position
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
    targetRealX = left_top_x + targetShotX  # 目标在屏幕的坐标
    targetRealY = left_top_y + targetShotY

    # dist = (targetRealX - current_mouse_x) ** 2 + (targetRealY - current_mouse_y) ** 2
    set_intention(targetRealX, targetRealY)

    # if(dist < 100000):
    # if (dist < 20000):
    #     mouse_To1(des_X=targetRealX, des_Y=targetRealY, current_mouse_x=current_mouse_x,
    #               current_mouse_y=current_mouse_y)
