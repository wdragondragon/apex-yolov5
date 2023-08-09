import sys
import threading

import cv2
import numpy as np
import pynput.mouse
import time
import torch
import win32con
import win32gui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import on_click, get_lock_mode, on_move, on_press, start
from apex_yolov5.grabscreen import grab_screen
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import model
from utils.augmentations import letterbox
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh


def main():
    print_count = 0
    compute_time = time.time()
    image_text = ''
    while True:
        try:
            t0 = time.time()
            img0 = grab_screen(region=global_config.region)
            img0 = cv2.resize(img0, (global_config.shot_width, global_config.shot_height))
            # img0 = get_img()
            # if img0 is None:
            #     continue
            stride = model.stride
            img = letterbox(img0, (global_config.imgsz, global_config.imgszy), stride=stride, auto=model.pt)[0]
            img = img.transpose((2, 0, 1))[::-1]
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(model.device)
            img = img.half() if model.fp16 else img.float()
            img /= 255

            if len(img.shape) == 3:
                img = img[None]  # img = img.unsqueeze(0)

            pred = model(img, augment=False, visualize=False)
            pred = non_max_suppression(pred, global_config.conf_thres, global_config.iou_thres, agnostic=False,
                                       max_det=1)

            aims = []
            bboxes = []
            for i, det in enumerate(pred):
                gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
                if len(det):
                    det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        # bbox:(tag, x_center, y_center, x_width, y_width)
                        """
                        0 ct_head  1 ct_body  2 t_head  3 t_body
                        """
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh)  # label format
                        aim = ('%g ' * len(line)).rstrip() % line
                        aim = aim.split(' ')
                        aims.append(aim)
                if len(aims):
                    if get_lock_mode():
                        lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                             shot_width=global_config.shot_width,
                             shot_height=global_config.shot_height)  # x y 是分辨率
                    if global_config.is_show_debug_window:
                        for i, det in enumerate(aims):
                            tag, x_center, y_center, width, height = det
                            x_center, width = global_config.shot_width * float(
                                x_center), global_config.shot_width * float(
                                width)
                            y_center, height = global_config.shot_height * float(
                                y_center), global_config.shot_height * float(
                                height)
                            top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                            bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                            bboxes.append((tag, top_left, bottom_right))
            print_count += 1
            now = time.time()
            if now - compute_time > 1:
                image_text = "一秒识别[{}]次:".format(print_count)
                log_window.print_log(image_text)
                print_count = 0
                compute_time = now
            if global_config.is_show_debug_window:
                log_window.set_image(img0, bboxes=bboxes)
        except Exception as e:
            log_window.print_log(e)
            pass


# main()
if __name__ == "__main__":
    # ...or, in a non-blocking fashion:
    listener = pynput.mouse.Listener(
        on_click=on_click, on_move=on_move)
    listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=on_press,
    )
    key_listener.start()

    names = model.module.names if hasattr(model, 'module') else model.names

    threading.Thread(target=start).start()

    app = QApplication(sys.argv)
    log_window = LogWindow()

    if global_config.is_show_debug_window:
        log_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        log_window.show()
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
