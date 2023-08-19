from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget


class MouseConfigLayout:

    def __init__(self, config, main_window, parent_layout):
        self.move_step_label = None
        self.move_step_slider = None
        self.move_step_layout = None

        self.move_path_nx_layout = None
        self.move_path_nx_label = None
        self.move_path_nx_slider = None

        self.cross_layout = None
        self.cross_label = None
        self.human_pixmap = None
        self.crosshair_pixmap = None
        self.crosshair_position = None
        self.image_widget = None
        self.slider = None
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        self.label = QLabel("瞄准设置")
        self.label.setAlignment(Qt.AlignCenter)

        move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_label = QLabel("单次移动像素:" + str(self.config.move_step), self.main_window)
        self.move_step_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_slider.setMinimum(1)  # 最小值
        self.move_step_slider.setMaximum(30)  # 最大值
        self.move_step_slider.setValue(self.config.move_step)  # 初始化值
        self.move_step_slider.valueChanged.connect(self.update_move_step_label)
        move_step_layout.addWidget(self.move_step_label)
        move_step_layout.addWidget(self.move_step_slider)

        move_path_nx_layout = QHBoxLayout()
        self.move_path_nx_label = QLabel("移动路径倍率:" + str(self.config.move_path_nx), self.main_window)
        self.move_path_nx_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_path_nx_slider.setMinimum(1)  # 最小值
        self.move_path_nx_slider.setMaximum(300)  # 最大值
        self.move_path_nx_slider.setValue(int(self.config.move_path_nx * 10))  # 初始化值
        self.move_path_nx_slider.valueChanged.connect(self.update_move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_slider)

        cross_layout = QHBoxLayout()
        self.cross_label = QLabel("瞄准高度：", self.main_window)
        self.human_pixmap = QPixmap("images/human.jpg").scaled(100, 200, Qt.KeepAspectRatio)
        self.crosshair_pixmap = QPixmap("images/crosshair.jpg").scaled(50, 50, Qt.KeepAspectRatio)
        human_pix_map_height = self.human_pixmap.size().height()
        cross_position_height = int(
            (human_pix_map_height // 2) * (1 - self.config.cross_hair))

        self.crosshair_position = QPoint(
            self.human_pixmap.size().width() // 2 - self.crosshair_pixmap.size().width() // 2,
            cross_position_height - self.crosshair_pixmap.size().height() // 2)
        self.image_widget = QWidget(self.main_window)
        self.image_widget.setFixedSize(self.human_pixmap.size())
        self.image_widget.paintEvent = self.paintEvent
        self.slider = QSlider(Qt.Vertical, self.main_window)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.human_pixmap.height())
        self.slider.setValue(self.slider.maximum() - cross_position_height)  # 反转滑动条的值
        self.slider.valueChanged.connect(self.move_crosshair)
        cross_layout.addWidget(self.cross_label)
        cross_layout.addWidget(self.slider)
        cross_layout.addWidget(self.image_widget)

        self.parent_layout.addWidget(self.label)
        self.parent_layout.addLayout(move_step_layout)
        self.parent_layout.addLayout(move_path_nx_layout)
        self.parent_layout.addLayout(cross_layout)

    def update_move_step_label(self, value):
        self.move_step_label.setText("单次移动像素:" + str(value))
        self.move_step_label.adjustSize()

    def update_move_path_nx_label(self, value):
        self.move_path_nx_label.setText("移动路径倍率:" + str((1.0 * value) / 10))
        self.move_path_nx_label.adjustSize()

    def move_crosshair(self, value):
        self.crosshair_position = QPoint(
            self.human_pixmap.size().width() // 2 - self.crosshair_pixmap.size().width() // 2,
            self.slider.maximum() - value - self.crosshair_pixmap.size().height() // 2)  # 反转滑动条的值
        self.image_widget.update()  # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self.image_widget)
        painter.drawPixmap(0, 0, self.human_pixmap)
        painter.drawPixmap(self.crosshair_position, self.crosshair_pixmap)

    def save_config(self):
        self.config.set_config("move_step", self.move_step_slider.value())
        self.config.set_config("move_path_nx", self.move_path_nx_slider.value() / 10.0)
        self.config.set_config("cross_hair", (self.slider.value() / (
                self.slider.maximum() // 2)) - 1)
