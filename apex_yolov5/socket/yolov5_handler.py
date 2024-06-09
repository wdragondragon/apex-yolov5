import time
import numpy as np
from torch import from_numpy, tensor

from apex_yolov5 import apex_model
from apex_yolov5.apex_model import load_model
from apex_yolov5.socket.config import global_config
from utils.augmentations import letterbox
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh

model = load_model()
names = model.module.names if hasattr(model, 'module') else model.names

def reload_model():
    global model, names
    if not apex_model.current_model_name == global_config.current_model:
        model = load_model()
        names = model.module.names if hasattr(model, 'module') else model.names


def get_aims(img0):
    # img0 = cv2.resize(img0, (global_config.shot_width, global_config.shot_height))
    stride = model.stride
    img = letterbox(img0, (global_config.imgsz, global_config.imgszy), stride=stride, auto=model.pt)[0]
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW and BGR to RGB
    img = np.ascontiguousarray(img)

    img = from_numpy(img).to(model.device)
    img = img.half() if model.fp16 else img.float()
    img /= 255.0

    if len(img.shape) == 3:
        img = img[None]  # Add batch dimension
    pred = model(img, augment=False, visualize=False)

    # Ensure pred is a tensor, not a list
    if isinstance(pred, (list, tuple)):
        pred = pred[0]

    pred = non_max_suppression(pred,
                               conf_thres=global_config.conf_thres,
                               iou_thres=global_config.iou_thres,
                               classes=None,
                               agnostic=False,
                               multi_label=False,
                               labels=(),
                               max_det=10)
    aims = []
    t1 = time.time()
    for i, det in enumerate(pred):
        gn = tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in reversed(det):
                # bbox:(tag, x_center, y_center, x_width, y_width)
                """
                0 ct_head  1 ct_body  2 t_head  3 t_body
                """
                xywh = (xyxy2xywh(tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = (cls, *xywh)  # label format
                aim = ('%g ' * len(line)).rstrip() % line
                aim = aim.split(' ')
                if all(item != 'nan' for item in aim):
                    aims.append(aim)

    return aims
