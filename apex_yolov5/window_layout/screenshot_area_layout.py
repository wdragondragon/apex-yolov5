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
        self.width_input.setText(str(int(self.config.shot_width)))
        self.height_input.setText(str(int(self.config.shot_height)))
        # 连接信号和槽
        self.width_input.textChanged.connect(self.update_inner_rect_size)
        self.height_input.textChanged.connect(self.update_inner_rect_size)

        self.width_input.setValidator(QIntValidator(0, self.config.screen_width))
        self.height_input.setValidator(QIntValidator(0, self.config.screen_height))
        resolution_layout.addWidget(self.screenshot_area_label)
        resolution_layout.addWidget(self.width_input)
        resolution_layout.addWidget(self.screenshot_area_x_label)
        resolution_layout.addWidget(self.height_input)

        self.view = RectView(self.main_window,
                             outer_rect_size=(
                                 int(self.config.screen_width / 10), int(self.config.screen_height / 10)),
                             inner_rect_size=(
                                 int(self.config.shot_width / 10), int(self.config.shot_height / 10)))
        screenshot_area_layout.addWidget(self.screenshot_area_title_label)
        screenshot_area_layout.addLayout(resolution_layout)
        screenshot_area_layout.addWidget(self.view)
        self.parent_layout.addLayout(screenshot_area_layout)

    def update_inner_rect_size(self):
        # 当输入框的内容改变时，更新内部框的大小
        width = int(self.width_input.text()) if self.width_input.text() else 0
        height = int(self.height_input.text()) if self.height_input.text() else 0
        self.view.resize_inner_rect(width, height)

    def save_config(self):
        self.config.set_config("shot_width", int(self.view.inner_rect.rect().width() * 10))
        self.config.set_config("shot_height", int(self.view.inner_rect.rect().height() * 10))


class RectView(QGraphicsView):
    def __init__(self, parent=None, outer_rect_size=(192, 108), inner_rect_size=(64, 64)):
        super(RectView, self).__init__(parent)
        self.setMinimumSize(*outer_rect_size)
        self.setScene(QGraphicsScene(self))

        self.outer_rect = self.scene().addRect(QRectF(0, 0, *outer_rect_size))  # 外部框
        self.outer_rect.setBrush(QColor(255, 0, 0))

        self.inner_rect = self.scene().addRect(QRectF(0, 0, *inner_rect_size))  # 内部框
        self.inner_rect.setBrush(QColor(0, 255, 0))

        self.center_inner_rect()

    def center_inner_rect(self):
        # 将内部框居中
        self.inner_rect.setPos((self.outer_rect.rect().width() - self.inner_rect.rect().width()) / 2,
                               (self.outer_rect.rect().height() - self.inner_rect.rect().height()) / 2)

    def resize_inner_rect(self, width, height):
        # 改变内部框的大小
        self.inner_rect.setRect(0, 0, width / 10, height / 10)
        self.center_inner_rect()
