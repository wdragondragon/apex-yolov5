import time

import cv2
import numpy as np
from apex_yolov5.apex_model import load_model
from apex_yolov5.socket.config import *
from utils.augmentations import letterbox
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh

model = load_model()
names = model.module.names if hasattr(model, 'module') else model.names

def get_aims(img0):
    img0 = cv2.resize(img0, (shot_width, shot_height))
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
    pred = non_max_suppression(pred, conf_thres, iou_thres, agnostic=False, max_det=1)
    # print(pred)

    aims = []
    t1 = time.time()
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
    return aims
