import sys
import threading

import cv2
import numpy as np
import pynput.mouse
import time
import torch
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication

from apex_yolov5.LogWindow import LogWindow
from apex_yolov5.auxiliary import on_click, get_lock_mode, on_move, on_press, start
from apex_yolov5.grabscreen import grab_screen
from apex_yolov5.mouse_lock import lock
from apex_yolov5.socket.config import global_config
from apex_yolov5.socket.yolov5_handler import model
from utils.augmentations import letterbox
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh

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


# threading.Thread(target=loop_screen, args=((left_top_x, left_top_y, right_bottom_x, right_bottom_y),
#                                            shot_Width,
#                                            shot_Height)).start()

def main():
    while True:
        t0 = time.time()
        img0 = grab_screen(region=global_config.region)
        img0 = cv2.resize(img0, (global_config.shot_width, global_config.shot_height))
        # img0 = get_img()
        # if img0 is None:
        #     continue
        stride = model.stride
        img = letterbox(img0, global_config.imgsz, stride=stride, auto=model.pt)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(model.device)
        img = img.half() if model.fp16 else img.float()
        img /= 255

        if len(img.shape) == 3:
            img = img[None]  # img = img.unsqueeze(0)

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, global_config.conf_thres, global_config.iou_thres, agnostic=False, max_det=1)

        aims = []
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
                    # print("aim:",aim)
                    aims.append(aim)
            if len(aims):
                if get_lock_mode():
                    lock(aims, global_config.mouse, global_config.screen_width, global_config.screen_height,
                         shot_width=global_config.shot_width,
                         shot_height=global_config.shot_height)  # x y 是分辨率
                for i, det in enumerate(aims):
                    tag, x_center, y_center, width, height = det
                    x_center, width = global_config.shot_width * float(x_center), global_config.shot_width * float(
                        width)
                    y_center, height = global_config.shot_height * float(y_center), global_config.shot_height * float(
                        height)
                    top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                    bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                    color = (0, 0, 255)  # BGR
                    if global_config.is_show_debug_window:
                        cv2.rectangle(img0, top_left, bottom_right, color, thickness=3)
        if global_config.is_show_debug_window:
            cv2.namedWindow(global_config.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(global_config.window_name, global_config.shot_width // 2, global_config.shot_height // 2)
            # global t0
            cv2.putText(img0, "FPS:{:.1f}".format(1.0 / (time.time() - t0)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 255, 0), 4)
            cv2.imshow(global_config.window_name, img0)

            hwnd = win32gui.FindWindow(None, global_config.window_name)
            CVRECT = cv2.getWindowImageRect(global_config.window_name)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


# main()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()
    threading.Thread(target=main).start()
    sys.exit(app.exec_())
