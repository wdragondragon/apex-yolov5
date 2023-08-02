import pynput.mouse

import torch

from aiming.apex_model import load_model
from aiming.mouse_lock import lock
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh, clip_boxes, xywh2xyxy
from utils.augmentations import letterbox
import cv2, time
import numpy as np

from aiming.grabscreen import grab_screen

device = 'cuda' if torch.cuda.is_available() else 'cpu'
half = device != 'cpu'
imgsz = 640
conf_thres = 0.4
iou_thres = 0.05
# screen_width, screren_ = (1920, 1080)  # 1280 * 1024
screen_width, screen_height = (2560, 1440)
# 截屏区域
offet_Shot_Screen = 20  # 屏幕截图偏移量,
# 默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
left_top_x = screen_width // 2 - offet_Shot_Screen * 16
left_top_y = screen_height // 2 - offet_Shot_Screen * 9
right_bottom_x = screen_width // 2 + offet_Shot_Screen * 16
right_bottom_y = screen_height // 2 + offet_Shot_Screen * 9
shot_Width = 2 * offet_Shot_Screen * 16  # 截屏区域的实际大小需要乘以2，因为是计算的中心点
shot_Height = 2 * offet_Shot_Screen * 9

window_Name = "apex-tang"
auto = True
model = load_model()
lock_mode = False  # don's edit this
mouse = pynput.mouse.Controller()  # 鼠标对象
lock_button = "left"  # 无用，apex为按住鼠标左或者右其中一个为就为lock模式，建议在游戏设置按住开镜
isShowDebugWindow = False  # 可修改为True，会出现调试窗口
isRightKeyDown = False
isLeftKeyDown = False
mouseFlag = 0  # 0, 1 2 3


def on_click(x, y, button, pressed):
    # print("鼠标按住")
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


listener = pynput.mouse.Listener(
    on_click=on_click)
listener.start()
names = model.module.names if hasattr(model, 'module') else model.names


def main():
    while True:
        t0 = time.time()
        monitor = {'top': left_top_x, 'left': left_top_y, 'width': shot_Width, 'height': shot_Height}
        # monitor = {'top': left_top_x, 'left': left_top_y, 'width': left_top_x - right_bottom_x,
        #            'height': left_top_y - right_bottom_y}
        # img0 = grab_screen(region=(left_top_x, left_top_y, right_bottom_x, right_bottom_y))
        img0 = grab_screen(monitor=monitor)
        img0 = cv2.resize(img0, (shot_Width, shot_Height))
        stride = model.stride
        img = letterbox(img0, imgsz, stride=stride, auto=model.pt)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(model.device)
        img = img.half() if model.fp16 else img.float()
        img /= 255

        if len(img.shape) == 3:
            img = img[None]  # img = img.unsqueeze(0)

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres, agnostic=False)
        # print(pred)

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
                    xyxy = torch.tensor(xyxy).view(-1, 4)
                    b = xyxy2xywh(xyxy)  # boxes
                    b[:, 2:] = b[:, 2:] * 1.02 + 10  # box wh * gain + pad
                    xyxy = xywh2xyxy(b).long()
                    clip_boxes(xyxy, img.shape)
                    crop = img[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(1 if True else -1)]
                    print("(" + str(int(xyxy[0, 0])) + "," + str(int(xyxy[0, 1])) + ")->(" + str(int(xyxy[0, 2])) + "," + str(int(xyxy[0, 3])) + ")")
                    aim = {"x1":int(xyxy[0, 0]),"y1":int(xyxy[0, 1]),"x2":int(xyxy[0, 2]),"y2":int(xyxy[0, 3])}
                    # print("aim:",aim)
                    aims.append(aim)

            if len(aims):
                if lock_mode:
                    print("todo...")
                    lock(aims, mouse, screen_width, screen_height, shot_width=shot_Width,
                         shot_height=shot_Height)  # x y 是分辨率
                # lock(aims, mouse, screen_width, screen_height, shot_width=shot_Width,shot_height=shot_Height) #x y 是分辨率
                # for i, det in enumerate(aims):
                #     tag, x_center, y_center, width, height = det
                #     x_center, width = shot_Width * float(x_center), shot_Width * float(width)
                #     y_center, height = shot_Height * float(y_center), shot_Height * float(height)
                #     top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
                #     bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
                #     color = (0, 0, 255)  # BGR


main()
