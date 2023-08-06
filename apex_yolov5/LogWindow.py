import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget


class LogWindow(QMainWindow):
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'log_text'):
            # self.app = QApplication(sys.argv)
            self.log_text = None
            self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 400, 300)

        # 创建 QTextEdit 组件用于显示日志
        self.log_text = QTextEdit()
        self.log_text.document().setMaximumBlockCount(1000)
        self.log_text.setReadOnly(True)

        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 日志打印函数

    def print_log(self, log):
        # 获取当前日期和时间
        now = datetime.now()
        # 格式化日期为字符串
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        msg = "[{}]{}".format(formatted_date, log)
        self.log_text.append(msg)
        self.log_text.moveCursor(self.log_text.textCursor().End)
        print(msg)

    # def exit(self):
    #     sys.exit(self.app.exec_())
