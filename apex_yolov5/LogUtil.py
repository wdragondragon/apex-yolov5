from apex_yolov5.LogWindow import LogWindow


class LogUtil:

    def __init__(self):
        self.use_time_dict = dict()

    def set_time(self, use_time_type, use_time):
        self.use_time_dict[use_time_type] = self.use_time_dict.get(use_time_type, 0) + use_time

    def print_time(self, print_count):
        for k, v in self.use_time_dict.items():
            LogWindow().print_log("步骤[{}]使用平均时间:{}ms".format(k, v * 1000 / print_count))
        self.use_time_dict.clear()


use_time_dict = dict()


def set_time(self, use_time_type, use_time):
    self.use_time_dict[use_time_type] = self.use_time_dict.get(use_time_type, 0) + use_time


def print_time(self, print_count):
    for k, v in self.use_time_dict.items():
        LogWindow().print_log("步骤[{}]使用平均时间:{}ms".format(k, v * 1000 / print_count))
    self.use_time_dict.clear()
