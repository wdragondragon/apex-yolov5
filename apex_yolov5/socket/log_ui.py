import cv2

from apex_yolov5.windows.DebugWindow import DebugWindow
from apex_yolov5.socket.config import global_config


def show(aims, img0):
    bboxes = []
    if len(aims):
        for i, det in enumerate(aims):
            tag, x_center, y_center, width, height = det
            x_center, width = global_config.shot_width * float(x_center), global_config.shot_width * float(width)
            y_center, height = global_config.shot_height * float(y_center), global_config.shot_height * float(height)
            top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
            bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
            bboxes.append((tag, top_left, bottom_right))
    if global_config.is_show_debug_window:
        DebugWindow().set_image(img0, bboxes=bboxes)
    return True


def destroy():
    cv2.destroyAllWindows()
