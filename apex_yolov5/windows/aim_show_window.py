from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPoint, QRect

from apex_yolov5.socket.config import global_config


class AimShowWindows(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.left_top_x, self.left_top_y = self.config.left_top_x, self.config.left_top_y
        self.setGeometry(self.left_top_x, self.left_top_y, self.config.shot_width, self.config.shot_width)
        self.setWindowTitle('')
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.bbox = None
        self.left_top_xy = None
        self.icon = QPixmap("images/aim3.ico")

    def update_box(self, left_top_xy, bbox):
        self.left_top_x, self.left_top_y = left_top_xy
        self.bbox = bbox
        self.update()

    def clear_box(self):
        self.bbox = None
        self.left_top_xy = None
        self.update()

    def paintEvent(self, event):
        if self.bbox is None:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        tag, x_center, y_center, width, height = self.bbox
        x_center, width = self.config.shot_width * float(
            x_center), self.config.shot_width * float(
            width)
        y_center, height = self.config.shot_height * float(
            y_center), self.config.shot_height * float(
            height)

        # 计算图标的位置
        icon_width, icon_height = self.icon.width(), self.icon.height()
        icon_position = QPoint(int(x_center - icon_width / 2.0), int(y_center - height / 2.0 - icon_height))

        # 绘制图标
        self.setGeometry(self.left_top_x, self.left_top_y, self.config.shot_width, self.config.shot_width)
        painter.drawPixmap(icon_position, self.icon)

        # top_left = (int(x_center - width / 2.0), int(y_center - height / 2.0))
        # bottom_right = (int(x_center + width / 2.0), int(y_center + height / 2.0))
        # color = self.config.aim_type[tag]
        # pen = QPen(QColor(color[0], color[1], color[2]), 3)
        # painter.setPen(pen)
        # # 在图像上绘制矩形
        # top_left = QPoint(*top_left)  # 你的左上角点
        # bottom_right = QPoint(*bottom_right)  # 你的右下角点
        # painter.drawRect(QRect(top_left, bottom_right))


aim_show_window: AimShowWindows = None


def get_aim_show_window():
    global aim_show_window
    if aim_show_window is None:
        aim_show_window = AimShowWindows(global_config)
    return aim_show_window


def destory_aim_show_window():
    global aim_show_window
    if aim_show_window is not None:
        aim_show_window.close()
        aim_show_window = None
