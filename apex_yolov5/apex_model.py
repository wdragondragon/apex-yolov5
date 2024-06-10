from torch.cuda import is_available

from apex_yolov5.socket.config import global_config
from models.common import DetectMultiBackend
from utils.general import check_img_size
from utils.torch_utils import select_device

current_model_name = ''


def load_model():
    global current_model_name
    device = global_config.device if global_config.device == 'cpu' or global_config.device == 'dml' else '0'  # cuda,cpu
    dnn = False
    device = select_device(device)
    print("cuda is ok?", is_available())
    current_model_info = global_config.available_models.get(global_config.current_model)
    print("加载模型:" + global_config.current_model + ":" + current_model_info["data"])
    model = DetectMultiBackend(weights=current_model_info["weights"], device=device, dnn=dnn,
                               data=current_model_info["data"],
                               fp16=global_config.half)

    bs = 1  # batch_size
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz=(global_config.imgsz, global_config.imgszy), s=stride)  # check image size
    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup

    current_model_name = global_config.current_model

    return model
