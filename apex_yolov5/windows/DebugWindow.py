from PyQt5.QtCore import QPoint, QRect, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from apex_yolov5.socket.config import global_config


class DebugWindow(QMainWindow):
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'image_label'):
            self.image_label = None
            self.init_ui()
        # self.installEventFilter(self)

    def init_ui(self):
        self.setWindowTitle("实时锁定人物展示")
        self.setGeometry(100, 100, 400, 300)
        # self.create_menus()

        self.image_label = QLabel(self)
        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_image(self, img_data, bboxes):
        if not global_config.is_show_debug_window:
            return
        # 将 OpenCV 图像转换为 QImage
        height, width, channel = img_data.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        # 创建 QPainter 对象并设置画笔
        painter = QPainter(pixmap)
        for bbox in bboxes:
            tag, top_left, bottom_right = bbox
            color = global_config.aim_type[tag]
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

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.setWindowOpacity(0.1)  # Set window opacity to 90% when focus is lost
        elif event.type() == QEvent.WindowActivate:
            self.setWindowOpacity(1.0)  # Set window opacity to fully opaque when focus is regained
        return super().eventFilter(obj, event)
