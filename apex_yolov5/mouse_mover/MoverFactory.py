import threading

from apex_recoils.core.kmnet_listener.ToggleKeyListener import ToggleKeyListener
from apex_yolov5.KmBoxNetListener import KmBoxNetListener
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover.FeiMover import FeiMover
from apex_yolov5.mouse_mover.GHubMover import GHubMover
from apex_yolov5.mouse_mover.KmBoxMover import KmBoxMover
from apex_yolov5.mouse_mover.KmBoxNetMover import KmBoxNetMover
from apex_yolov5.mouse_mover.MouseMover import MouseMover
from apex_yolov5.mouse_mover.PanNiMover import PanNiMover
from apex_yolov5.mouse_mover.Win32ApiMover import Win32ApiMover
from apex_yolov5.mouse_mover.WuYaMover import WuYaMover
from apex_yolov5.socket.config import global_config

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
        current_mover = Win32ApiMover(mouse_mover_param)
    elif mouse_model == "km_box":
        current_mover = KmBoxMover(mouse_mover_param)
    elif mouse_model == "fei_yi_lai" or mouse_model == 'fei_yi_lai_single':
        current_mover = FeiMover(mouse_mover_param)
    elif mouse_model == "wu_ya":
        current_mover = WuYaMover(mouse_mover_param)
    elif mouse_model == 'logitech':
        current_mover = GHubMover(mouse_mover_param)
    elif mouse_model == "pan_ni":
        current_mover = PanNiMover(mouse_mover_param)
    elif mouse_model == "km_box_net":
        current_mover = KmBoxNetMover(mouse_mover_param)
        current_mover.listener = KmBoxNetListener(current_mover)
        threading.Thread(target=current_mover.listener.km_box_net_start).start()
        if global_config.rea_snow_gun_config_name != "":
            current_mover.toggle_key_listener = ToggleKeyListener(km_box_net_listener=current_mover.listener,
                                                                  delayed_activation_key_list=global_config.delayed_activation_key_list,
                                                                  toggle_hold_key=global_config.toggle_hold_key)


def reload_mover(mouse_model, mouse_mover_params):
    if current_mover is not None:
        current_mover.destroy()
        init_mover(mouse_model, mouse_mover_params)


def mouse_mover():
    return current_mover
