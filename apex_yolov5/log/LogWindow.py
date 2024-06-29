import os
import time
import traceback

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QApplication, QPushButton, QTabWidget

from apex_yolov5.Tools import Tools
from apex_yolov5.log.Logger import Logger


class LogWindow(QMainWindow, Logger):
    """
        日志窗口
    """
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'log_text'):
            self.tab_widget = None
            self.log_texts = {}
            self.log_queue = Tools.GetBlockQueue(name='log_queue', maxsize=1000)
            self.init_ui()
            # 实例化对象
            self.print_log_thread = PrintLogThread(self.log_queue)
            # 信号连接到界面显示槽函数
            self.print_log_thread.log_signal.connect(self.real_print)
            # 多线程开始
            self.print_log_thread.start()
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def init_ui(self):
        """
            初始化UI
        """
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 600, 300)
        # 创建 QTextEdit 组件用于显示日志
        self.tab_widget = QTabWidget()

        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def print_log(self, log, log_type="default"):
        """
            打印日志
        :param log:
        :param log_type:
        """
        self.log_queue.put((log, log_type))

    def closeEvent(self, event):
        """
            关闭事件
        :param event:
        """
        QApplication.quit()
        os._exit(0)

    def real_print(self, log_data):
        """
            真实打印函数
        :param log_data:
        """
        log, log_type = log_data
        if log_type not in self.log_texts:
            self.add_log_tab(log_type)
        log_text = self.log_texts[log_type]
        log_text.append(log)
        log_text.moveCursor(log_text.textCursor().End)
        super().print_log(text=log)

    def add_log_tab(self, log_type):
        """
            添加日志类型标签页
        :param log_type:
        """
        log_text = QTextEdit()
        log_text.document().setMaximumBlockCount(1000)
        log_text.setReadOnly(True)
        self.tab_widget.addTab(log_text, log_type)
        self.log_texts[log_type] = log_text


class PrintLogThread(QThread):
    """
        使用信号槽来多线程更新ui
    """
    log_signal = pyqtSignal(tuple)

    def __init__(self, log_queue: Tools.GetBlockQueue):
        super().__init__()
        self.log_queue = log_queue

    def run(self):
        """
            避免多线程影响ui，在一个线程中启动队列消费打印
        """
        self.log_signal.emit(("打印日志线程启动", "default"))
        while True:
            try:
                log_data = self.log_queue.get()
                self.log_signal.emit(log_data)
            except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(0.1)
