import json
import os.path

from apex_yolov5.log.LogWindow import LogWindow
from apex_yolov5.log.Logger import Logger

current_logger: Logger = None


def init_logger():
    global current_logger
    current_logger = LogWindow()


def logger():
    return current_logger


def getLogger(cls):
    """
        获取打印日志实峛
    """
    return MultipleLogger(cls)


log_map = {}
log_json = "config/log.json"
if os.path.exists(log_json):
    with open(log_json, encoding='utf-8') as file:
        log_map = json.load(file)


def prefix_search(full_path):
    """
        前缀匹配
    """
    longest_prefix = (0, "")
    for (key, value) in log_map.items():
        if full_path.startswith(key):
            max_length, log_type = longest_prefix
            length = len(key.split("."))
            if length > max_length:
                longest_prefix = (length, value)
    return longest_prefix


class MultipleLogger(Logger):
    def __init__(self, cls):
        self.cls = cls
        self.full_path = f"{cls.__module__}.{cls.__name__}"

    def print_log(self, text, log_type="default"):
        if current_logger is None:
            init_logger()

        length, search_log_type = prefix_search(self.full_path)
        if length != 0:
            current_logger.print_log(text, search_log_type)
        else:
            current_logger.print_log(text, log_type)
