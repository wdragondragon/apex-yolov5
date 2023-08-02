import torch

# sys.path.append(dir+"\\utils")

# from models.experimental import attempt_load
from utils.general import check_img_size
from utils.torch_utils import select_device
from models.common import DetectMultiBackend

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# #device = 'cpu'
# half = device != 'cpu'
#
# weights = r'apexSt1.pt'
# weights = "yolov5s.pt"
# weights = 'best.pt' #这个模型最好

# weights = 'apex-yolov5/apex.pt'
weights = 'apex_yolov5/apex2.pt'
# imgsz = 640
device = '0'  # cuda,cpu
dnn = False
data = 'models/mydata.yaml'
half = False
imgsz1 = (640, 640)
device = select_device(device)


def load_model():
    print("cuda is ok?", torch.cuda.is_available())
    model = DetectMultiBackend(weights=weights, device=device, dnn=dnn, data=data, fp16=half)

    bs = 1  # batch_size
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz=imgsz1, s=stride)  # check image size
    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup

    return model
