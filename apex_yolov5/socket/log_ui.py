import time

import cv2
import win32con
import win32gui
from apex_yolov5.socket.config import global_config


def show(aims, img0, start_time, t0, total_size):
    if len(aims):
        for i, det in enumerate(aims):
            tag, x_center, y_center, width, height = det
            x_center, width = global_config.shot_width * float(x_center), global_config.shot_width * float(width)
            y_center, height = global_config.shot_height * float(y_center), global_config.shot_height * float(height)
            top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
            bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
            color = (0, 0, 255)  # BGR
            cv2.rectangle(img0, top_left, bottom_right, color, thickness=3)
    # 发送响应给客户端
    cv2.namedWindow(global_config.window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(global_config.window_name, global_config.shot_width, global_config.shot_height)
    cv2.putText(img0, "FPS:{:.1f},{:.1f}M/s".format(1.0 / (time.time() - t0),
                                                    (1.0 * total_size / 1024 / 1024) / (
                                                            time.time() - start_time)),
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 255, 0), 4)
    # global t0
    cv2.imshow(global_config.window_name, img0)
    hwnd = win32gui.FindWindow(None, global_config.window_name)
    CVRECT = cv2.getWindowImageRect(global_config.window_name)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return False
    return True


def destroy():
    cv2.destroyAllWindows()
