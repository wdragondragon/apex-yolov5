import queue
import sys
import time
from datetime import datetime

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLabel

from apex_yolov5.socket.config import global_config

message_queue = queue.Queue()


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
        self.log_text.document().setMaximumBlockCount(200)
        self.log_text.setReadOnly(True)

        self.image_label = QLabel(self)
        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.log_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @staticmethod
    def set_image(img_data, bboxes):
        message_queue.put({'msg_type': 'image', 'param': (img_data, bboxes)})

    @staticmethod
    def print_log(log):
        message_queue.put({'msg_type': 'log', 'param': (log)})

    def show(self):
        while True:
            if not message_queue.empty():
                msg = message_queue.get()
                msg_type = msg['msg_type']
                param = msg['param']
                if msg_type == 'image':
                    self.show_image(*param)
                elif msg_type == 'log':
                    self.show_log(*param)
            QApplication.processEvents()
            time.sleep(0.01)

    def show_log(self, log):
        # 获取当前日期和时间
        now = datetime.now()
        # 格式化日期为字符串
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        msg = "[{}]{}".format(formatted_date, log)
        if global_config.is_show_debug_window:
            self.log_text.append(msg)
            self.log_text.moveCursor(self.log_text.textCursor().End)
        print(msg)

    def show_image(self, img_data, bboxes):
        # 将 OpenCV 图像转换为 QImage
        height, width, channel = img_data.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        # 创建 QPainter 对象并设置画笔
        painter = QPainter(pixmap)
        for bbox in bboxes:
            tag, top_left, bottom_right = bbox
            color = global_config.lock_index[tag]
            pen = QPen(QColor(color[0], color[1], color[2]), 5)  # 设置颜色和线宽
            painter.setPen(pen)
            # 在图像上绘制矩形
            top_left = QPoint(*top_left)  # 你的左上角点
            bottom_right = QPoint(*bottom_right)  # 你的右下角点
            painter.drawRect(QRect(top_left, bottom_right))
            # 结束绘制
        # 设置字体
        painter.end()
        self.image_label.setPixmap(pixmap)
        self.image_label.update()
