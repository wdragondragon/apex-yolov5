from torch.cuda import is_available

from apex_yolov5.socket.config import global_config
from models.common import DetectMultiBackend
from utils.general import check_img_size
from utils.torch_utils import select_device

# sys.path.append(dir+"\\utils")

# from models.experimental import attempt_load
# import utils.general as utils_general
# import utils.torch_utils as utils_torch
# import models.common as models_common

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# #device = 'cpu'
# half = device != 'cpu'
#
# weights = r'apexSt1.pt'
# weights = "yolov5s.pt"
# weights = 'best.pt' #这个模型最好

# weights = 'apex-yolov5/apex.pt'
weights = global_config.weights
data = global_config.data

# weights = 'C:/Users/Administrator/PycharmProjects/apex-yolov5/apex_yolov5/apex-1050.engine'
# data = 'C:/Users/Administrator/PycharmProjects/apex-yolov5/models/mydata.yaml'
# imgsz = 640
device = global_config.device if global_config.device == 'cpu' else '0'  # cuda,cpu
dnn = False
half = global_config.half
imgsz1 = (global_config.imgsz, global_config.imgszy)
device = select_device(device)


def load_model():
    print("cuda is ok?", is_available())
    model = DetectMultiBackend(weights=weights, device=device, dnn=dnn, data=data, fp16=half)

    bs = 1  # batch_size
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz=imgsz1, s=stride)  # check image size
    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup

    return model
