from apex_yolov5.log.Logger import Logger

current_logger = None


def init_logger():
    global current_logger
    current_logger = Logger()


def logger():
    return current_logger
