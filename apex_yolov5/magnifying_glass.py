import cv2
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout

from apex_yolov5.Tools import Tools


class MagnifyingGlassWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MagnifyingGlassWindows")
        (self.x, self.y) = Tools.get_resolution()
        self.setGeometry(int(self.x // 2), int(self.y // 2), 640, 640)

        self.image_label = QLabel(self)
        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_image(self, img_data):
        # 将 OpenCV 图像转换为 QImage
        height, width, channel = img_data.shape
        img_data = cv2.resize(img_data, (width * 2, height * 2))

        height, width, channel = img_data.shape
        bytes_per_line = 3 * width
        q_img = QImage(img_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        # 创建 QPainter 对象并设置画笔
        painter = QPainter(pixmap)
        # 设置字体
        painter.end()
        self.image_label.setPixmap(pixmap)
        self.image_label.update()
