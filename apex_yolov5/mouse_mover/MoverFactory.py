from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.KmBoxMover import KmBoxMover
from apex_yolov5.mouse_mover.MouseMover import MouseMover
from apex_yolov5.mouse_mover.Win32ApiMover import Win32ApiMover
from apex_yolov5.mouse_mover.WuYaMover import WuYaMover

current_mover: MouseMover = None


def init_mover(mouse_model, mouse_mover_params):
    global current_mover
    mouse_mover_param = mouse_mover_params[mouse_model]
    logger = LogFactory.logger()
    if mouse_mover_param is None:
        logger.print_log(f"鼠标模式:[{mouse_model}]不可用")
    else:
        logger.print_log(f"初始化鼠标模式：[{mouse_model}]")
    if mouse_model == 'win32api':
        current_mover = Win32ApiMover(logger, mouse_mover_param)
    elif mouse_model == "km_box":
        current_mover = KmBoxMover(logger, mouse_mover_param)
    elif mouse_model == "wu_ya":
        current_mover = WuYaMover(logger, mouse_mover_param)


def reload_mover(mouse_model, mouse_mover_params):
    if current_mover is not None:
        current_mover.destroy()
        init_mover(mouse_model, mouse_mover_params)


def mouse_mover():
    return current_mover
