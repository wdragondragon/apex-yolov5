from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QIntValidator, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGraphicsView, QGraphicsScene


class ScreenshotAreaLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        screenshot_area_layout = QVBoxLayout(self.main_window)
        resolution_layout = QHBoxLayout(self.main_window)
        self.screenshot_area_title_label = QLabel("截图设置")
        self.screenshot_area_title_label.setAlignment(Qt.AlignCenter)
        self.screenshot_area_label = QLabel("截图区域：", self.main_window)
        self.screenshot_area_x_label = QLabel("x", self.main_window)

        self.width_input = QLineEdit(self.main_window)
        self.height_input = QLineEdit(self.main_window)
        self.mouse_moving_radius_input = QLineEdit(self.main_window)
        self.width_input.setText(str(int(self.config.shot_width)))
        self.height_input.setText(str(int(self.config.shot_height)))

        self.mouse_moving_radius_label = QLabel("移动直径：")
        self.mouse_moving_radius_input.setText(str(int(self.config.mouse_moving_radius)))
        # 连接信号和槽
        self.width_input.textChanged.connect(self.update_inner_rect_size)
        self.height_input.textChanged.connect(self.update_inner_rect_size)
        self.mouse_moving_radius_input.textChanged.connect(self.update_inner_circle_size)

        self.width_input.setValidator(QIntValidator(0, self.config.screen_width))
        self.height_input.setValidator(QIntValidator(0, self.config.screen_height))
        resolution_layout.addWidget(self.screenshot_area_label)
        resolution_layout.addWidget(self.width_input)
        resolution_layout.addWidget(self.screenshot_area_x_label)
        resolution_layout.addWidget(self.height_input)
        resolution_layout.addWidget(self.mouse_moving_radius_label)
        resolution_layout.addWidget(self.mouse_moving_radius_input)

        self.view = RectView(self.main_window,
                             outer_rect_size=(
                                 int(self.config.screen_width / 10), int(self.config.screen_height / 10)),
                             inner_rect_size=(
                                 int(self.config.shot_width / 10), int(self.config.shot_height / 10)),
                             radius=int(self.config.mouse_moving_radius / 10))
        screenshot_area_layout.addWidget(self.screenshot_area_title_label)
        screenshot_area_layout.addLayout(resolution_layout)
        screenshot_area_layout.addWidget(self.view)
        self.parent_layout.addLayout(screenshot_area_layout)

    def update_inner_rect_size(self):
        # 当输入框的内容改变时，更新内部框的大小
        width = int(self.width_input.text()) if self.width_input.text() else 0
        height = int(self.height_input.text()) if self.height_input.text() else 0
        self.view.resize_inner_rect(width, height)

    def update_inner_circle_size(self):
        radius = int(self.mouse_moving_radius_input.text()) if self.mouse_moving_radius_input.text() else 0
        self.view.resize_inner_circle(radius)

    def save_config(self):
        self.config.set_config("shot_width", int(self.view.inner_rect.rect().width() * 10))
        self.config.set_config("shot_height", int(self.view.inner_rect.rect().height() * 10))
        self.config.set_config("mouse_moving_radius", int(self.mouse_moving_radius_input.text()))


class RectView(QGraphicsView):
    def __init__(self, parent=None, outer_rect_size=(192, 108), inner_rect_size=(64, 64), radius=32):
        super(RectView, self).__init__(parent)
        self.setMinimumSize(*outer_rect_size)
        self.setScene(QGraphicsScene(self))

        self.outer_rect = self.scene().addRect(QRectF(0, 0, *outer_rect_size))  # 外部框
        self.outer_rect.setBrush(QColor(255, 0, 0))

        self.inner_rect = self.scene().addRect(QRectF(0, 0, *inner_rect_size))  # 内部框
        self.inner_rect.setBrush(QColor(0, 255, 0))
        self.center_inner_rect()

        self.inner_circle = self.scene().addEllipse(QRectF(0, 0, radius * 2, radius * 2))
        self.inner_circle.setBrush(QColor(0, 0, 255))  # 设置圆形的填充颜色为蓝色
        self.center_inner_circle()

    def center_inner_rect(self):
        # 将内部框居中
        self.inner_rect.setPos((self.outer_rect.rect().width() - self.inner_rect.rect().width()) / 2,
                               (self.outer_rect.rect().height() - self.inner_rect.rect().height()) / 2)

    def center_inner_circle(self):
        self.inner_circle.setPos((self.outer_rect.rect().width() - self.inner_circle.rect().width()) / 2,
                                 (self.outer_rect.rect().height() - self.inner_circle.rect().height()) / 2)

    def resize_inner_rect(self, width, height):
        # 改变内部框的大小
        self.inner_rect.setRect(0, 0, width / 10, height / 10)
        self.center_inner_rect()

    def resize_inner_circle(self, radius):
        self.inner_circle.setRect(0, 0, radius * 2 / 10, radius * 2 / 10)
        self.center_inner_circle()
