import inspect
import os

max_length = 0


class Logger:
    """
        日志抽象
    """

    def print_log(self, text, log_type="default"):
        """
            打印日志
        :param text:
        :param log_type:
        """
        global max_length
        # 获取被调用函数所在模块文件名
        file_path = inspect.stack()[1][1]

        (filepath, file_name) = os.path.split(file_path)
        (file_name, extension) = os.path.splitext(file_name)
        func_name = inspect.stack()[1][3]
        line_num = inspect.stack()[1][2]
        text_split = text.split("\n")
        log_text = f'[{file_name}:{func_name}][{line_num}]'
        max_length = max(max_length, len(log_text))
        for content in text_split:
            print(str.ljust(log_text, max_length) + content)