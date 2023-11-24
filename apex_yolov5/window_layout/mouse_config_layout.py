from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget, QCheckBox, QComboBox

import km_test


class MouseConfigLayout:

    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        self.label = QLabel("瞄准设置")
        self.label.setAlignment(Qt.AlignCenter)

        mouse_model_layout = QHBoxLayout()
        mouse_model_layout.setObjectName("add_layout")
        mouse_model_label = QLabel("选择自瞄鼠标模式:")
        self.mouse_model_combo_box = QComboBox()

        for key in self.config.available_mouse_models.keys():
            self.mouse_model_combo_box.addItem(key)
        self.mouse_model_combo_box.setCurrentText(self.config.mouse_model)
        self.mouse_model_combo_box.currentIndexChanged.connect(self.selection_changed)
        mouse_model_layout.addWidget(mouse_model_label)
        mouse_model_layout.addWidget(self.mouse_model_combo_box)

        aim_model_layout = QHBoxLayout()
        aim_model_label = QLabel("选择开镜瞄准模式")
        self.aim_model_combo_box = QComboBox()
        for key in self.config.aim_models:
            self.aim_model_combo_box.addItem(key)
            self.aim_model_combo_box.setCurrentText(self.config.aim_model)
            self.aim_model_combo_box.currentIndexChanged.connect(self.selection_aim_model_changed)
        aim_model_layout.addWidget(aim_model_label)
        aim_model_layout.addWidget(self.aim_model_combo_box)

        self.mouse_smoothing_switch = QCheckBox("鼠标平滑（勾选后单词移动像素才生效）")
        self.mouse_smoothing_switch.setObjectName("mouse_smoothing_switch")
        self.mouse_smoothing_switch.setChecked(self.config.mouse_smoothing_switch)  # 初始化开关的值
        self.mouse_smoothing_switch.toggled.connect(self.disable_silder_toggled)

        self.aim_button_layout = QHBoxLayout()
        self.aim_button_label = QLabel("自动标准触发按键:")
        self.left_aim = QCheckBox("左键")
        self.left_aim.setObjectName("left")
        self.left_aim.setChecked("left" in self.config.aim_button)  # 初始化开关的值
        self.left_aim.toggled.connect(self.handle_toggled)

        self.right_aim = QCheckBox("右键")
        self.right_aim.setObjectName("right")
        self.right_aim.setChecked("right" in self.config.aim_button)  # 初始化开关的值
        self.right_aim.toggled.connect(self.handle_toggled)

        self.x2_aim = QCheckBox("前侧键")
        self.x2_aim.setObjectName("x2")
        self.x2_aim.setChecked("x2" in self.config.aim_button)  # 初始化开关的值
        self.x2_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.left_aim)
        self.aim_button_layout.addWidget(self.right_aim)
        self.aim_button_layout.addWidget(self.x2_aim)

        self.x1_aim = QCheckBox("后侧键")
        self.x1_aim.setObjectName("x1")
        self.x1_aim.setChecked("x1" in self.config.aim_button)  # 初始化开关的值
        self.x1_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.x1_aim)

        self.x1_no_x2_aim = QCheckBox("右键除左键")
        self.x1_no_x2_aim.setObjectName("x1&!x2")
        self.x1_no_x2_aim.setChecked("x1&!x2" in self.config.aim_button)  # 初始化开关的值
        self.x1_no_x2_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.x1_no_x2_aim)

        move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_label = QLabel("单次水平移动像素:" + str(self.config.move_step), self.main_window)
        self.move_step_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_slider.setMinimum(1)  # 最小值
        self.move_step_slider.setMaximum(100)  # 最大值
        self.move_step_slider.setValue(self.config.move_step)  # 初始化值
        self.move_step_slider.valueChanged.connect(self.update_move_step_label)
        self.move_step_slider.setEnabled(self.config.mouse_smoothing_switch)
        move_step_layout.addWidget(self.move_step_label)
        move_step_layout.addWidget(self.move_step_slider)

        move_step_y_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_y_label = QLabel("单次垂直移动像素:" + str(self.config.move_step_y), self.main_window)
        self.move_step_y_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_y_slider.setMinimum(1)  # 最小值
        self.move_step_y_slider.setMaximum(100)  # 最大值
        self.move_step_y_slider.setValue(self.config.move_step_y)  # 初始化值
        self.move_step_y_slider.valueChanged.connect(self.update_move_step_y_label)
        self.move_step_y_slider.setEnabled(self.config.mouse_smoothing_switch)
        move_step_y_layout.addWidget(self.move_step_y_label)
        move_step_y_layout.addWidget(self.move_step_y_slider)

        move_path_nx_layout = QHBoxLayout()
        self.move_path_nx_label = QLabel("移动水平路径倍率:" + str(self.config.move_path_nx), self.main_window)
        self.move_path_nx_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_path_nx_slider.setObjectName("move_path_nx")
        self.move_path_nx_slider.setMinimum(1)  # 最小值
        self.move_path_nx_slider.setMaximum(300)  # 最大值
        self.move_path_nx_slider.setValue(int(self.config.move_path_nx * 10))  # 初始化值
        self.move_path_nx_slider.valueChanged.connect(self.update_move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_slider)

        move_path_ny_layout = QHBoxLayout()
        self.move_path_ny_label = QLabel("移动垂直路径倍率:" + str(self.config.move_path_ny), self.main_window)
        self.move_path_ny_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_path_ny_slider.setObjectName("move_path_ny")
        self.move_path_ny_slider.setMinimum(1)  # 最小值
        self.move_path_ny_slider.setMaximum(300)  # 最大值
        self.move_path_ny_slider.setValue(int(self.config.move_path_ny * 10))  # 初始化值
        self.move_path_ny_slider.valueChanged.connect(self.update_move_path_ny_label)
        move_path_ny_layout.addWidget(self.move_path_ny_label)
        move_path_ny_layout.addWidget(self.move_path_ny_slider)

        aim_move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.aim_move_step_label = QLabel("瞄准时水平移动像素:" + str(self.config.aim_move_step), self.main_window)
        self.aim_move_step_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_slider.setMinimum(1)  # 最小值
        self.aim_move_step_slider.setMaximum(100)  # 最大值
        self.aim_move_step_slider.setValue(self.config.aim_move_step)  # 初始化值
        self.aim_move_step_slider.valueChanged.connect(self.update_aim_move_step_label)
        self.aim_move_step_slider.setEnabled(self.config.mouse_smoothing_switch)
        aim_move_step_layout.addWidget(self.aim_move_step_label)
        aim_move_step_layout.addWidget(self.aim_move_step_slider)

        aim_move_step_y_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.aim_move_step_y_label = QLabel("瞄准时垂直移动像素:" + str(self.config.aim_move_step_y), self.main_window)
        self.aim_move_step_y_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_y_slider.setMinimum(1)  # 最小值
        self.aim_move_step_y_slider.setMaximum(100)  # 最大值
        self.aim_move_step_y_slider.setValue(self.config.aim_move_step_y)  # 初始化值
        self.aim_move_step_y_slider.valueChanged.connect(self.update_aim_move_step_y_label)
        self.aim_move_step_y_slider.setEnabled(self.config.mouse_smoothing_switch)
        aim_move_step_y_layout.addWidget(self.aim_move_step_y_label)
        aim_move_step_y_layout.addWidget(self.aim_move_step_y_slider)

        aim_move_path_nx_layout = QHBoxLayout()
        self.aim_move_path_nx_label = QLabel("瞄准时移动水平路径倍率:" + str(self.config.aim_move_path_nx),
                                             self.main_window)
        self.aim_move_path_nx_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_path_nx_slider.setObjectName("aim_move_path_nx")
        self.aim_move_path_nx_slider.setMinimum(1)  # 最小值
        self.aim_move_path_nx_slider.setMaximum(300)  # 最大值
        self.aim_move_path_nx_slider.setValue(int(self.config.aim_move_path_nx * 10))  # 初始化值
        self.aim_move_path_nx_slider.valueChanged.connect(self.update_aim_move_path_nx_label)
        aim_move_path_nx_layout.addWidget(self.aim_move_path_nx_label)
        aim_move_path_nx_layout.addWidget(self.aim_move_path_nx_slider)

        aim_move_path_ny_layout = QHBoxLayout()
        self.aim_move_path_ny_label = QLabel("瞄准时移动垂直路径倍率:" + str(self.config.aim_move_path_ny),
                                             self.main_window)
        self.aim_move_path_ny_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_path_ny_slider.setObjectName("aim_move_path_ny")
        self.aim_move_path_ny_slider.setMinimum(1)  # 最小值
        self.aim_move_path_ny_slider.setMaximum(300)  # 最大值
        self.aim_move_path_ny_slider.setValue(int(self.config.aim_move_path_ny * 10))  # 初始化值
        self.aim_move_path_ny_slider.valueChanged.connect(self.update_aim_move_path_ny_label)
        aim_move_path_ny_layout.addWidget(self.aim_move_path_ny_label)
        aim_move_path_ny_layout.addWidget(self.aim_move_path_ny_slider)

        self.mouse_move_frequency_switch = QCheckBox("鼠标移动频率自适应（勾选后移动频率不生效）")
        self.mouse_move_frequency_switch.setObjectName("mouse_move_frequency_switch")
        self.mouse_move_frequency_switch.setChecked(self.config.mouse_move_frequency_switch)  # 初始化开关的值
        self.mouse_move_frequency_switch.toggled.connect(self.disable_silder_toggled)

        mouse_move_frequency_layout = QHBoxLayout()
        self.mouse_move_frequency_label = QLabel("鼠标移动频率:" + str(int(1 / self.config.mouse_move_frequency)),
                                                 self.main_window)
        self.mouse_move_frequency_slider = QSlider(Qt.Horizontal, self.main_window)
        self.mouse_move_frequency_slider.setObjectName("mouse_move_frequency")
        self.mouse_move_frequency_slider.setMinimum(100)  # 最小值
        self.mouse_move_frequency_slider.setMaximum(1000)  # 最大值
        self.mouse_move_frequency_slider.setValue(int(1 / self.config.mouse_move_frequency))  # 初始化值
        self.mouse_move_frequency_slider.valueChanged.connect(self.update_mouse_move_frequency_label)
        self.mouse_move_frequency_slider.setEnabled(
            self.config.mouse_smoothing_switch and not self.config.mouse_move_frequency_switch)
        mouse_move_frequency_layout.addWidget(self.mouse_move_frequency_label)
        mouse_move_frequency_layout.addWidget(self.mouse_move_frequency_slider)

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
        self.parent_layout.addLayout(self.aim_button_layout)
        self.parent_layout.addLayout(aim_model_layout)
        self.parent_layout.addLayout(mouse_model_layout)
        self.parent_layout.addWidget(self.mouse_smoothing_switch)
        self.parent_layout.addLayout(move_step_layout)
        self.parent_layout.addLayout(move_step_y_layout)
        self.parent_layout.addLayout(move_path_nx_layout)
        self.parent_layout.addLayout(move_path_ny_layout)

        self.parent_layout.addLayout(aim_move_step_layout)
        self.parent_layout.addLayout(aim_move_step_y_layout)
        self.parent_layout.addLayout(aim_move_path_nx_layout)
        self.parent_layout.addLayout(aim_move_path_ny_layout)

        self.parent_layout.addWidget(self.mouse_move_frequency_switch)
        self.parent_layout.addLayout(mouse_move_frequency_layout)

        self.parent_layout.addLayout(cross_layout)

    def selection_changed(self, index):
        selected_key = self.mouse_model_combo_box.currentText()
        self.mouse_model_combo_box.setEnabled(False)
        self.config.set_config("mouse_model", selected_key)
        if selected_key == "kmbox":
            km_test.load()
        self.mouse_model_combo_box.setEnabled(True)

    def selection_aim_model_changed(self, index):
        self.config.set_config("aim_model", self.aim_model_combo_box.currentText())

    def handle_toggled(self, checked):
        if checked and not self.main_window.sender().objectName() in self.config.aim_button:
            self.config.aim_button.append(self.main_window.sender().objectName())
        elif not checked and self.main_window.sender().objectName() in self.config.aim_button:
            self.config.aim_button.remove(self.main_window.sender().objectName())

    def disable_silder_toggled(self, checked):
        self.main_window.handle_toggled(checked)
        if self.main_window.sender().objectName() == 'mouse_smoothing_switch':
            self.move_step_slider.setEnabled(checked)
            self.move_step_y_slider.setEnabled(checked)
            self.aim_move_step_slider.setEnabled(checked)
            self.aim_move_step_y_slider.setEnabled(checked)
            self.mouse_move_frequency_slider.setEnabled(checked and not self.mouse_move_frequency_switch.isChecked())
        elif self.main_window.sender().objectName() == 'mouse_move_frequency_switch':
            self.mouse_move_frequency_slider.setEnabled(not checked and self.mouse_smoothing_switch.isChecked())

    def update_move_step_label(self, value):
        self.move_step_label.setText("单次水平移动像素:" + str(value))
        self.move_step_label.adjustSize()

    def update_move_step_y_label(self, value):
        self.move_step_y_label.setText("单次垂直移动像素:" + str(value))
        self.move_step_y_label.adjustSize()

    def update_move_path_nx_label(self, value):
        self.move_path_nx_label.setText("移动水平路径倍率:" + str((1.0 * value) / 10))
        self.move_path_nx_label.adjustSize()

    def update_move_path_ny_label(self, value):
        self.move_path_ny_label.setText("移动垂直路径倍率:" + str((1.0 * value) / 10))
        self.move_path_ny_label.adjustSize()

    def update_aim_move_step_label(self, value):
        self.aim_move_step_label.setText("瞄准时水平移动像素:" + str(value))
        self.aim_move_step_label.adjustSize()

    def update_aim_move_step_y_label(self, value):
        self.aim_move_step_y_label.setText("瞄准时垂直移动像素:" + str(value))
        self.aim_move_step_y_label.adjustSize()

    def update_aim_move_path_nx_label(self, value):
        self.aim_move_path_nx_label.setText("瞄准时移动水平路径倍率:" + str((1.0 * value) / 10))
        self.aim_move_path_nx_label.adjustSize()

    def update_aim_move_path_ny_label(self, value):
        self.aim_move_path_ny_label.setText("瞄准时移动垂直路径倍率:" + str((1.0 * value) / 10))
        self.aim_move_path_ny_label.adjustSize()

    def update_mouse_move_frequency_label(self, value):
        self.mouse_move_frequency_label.setText("鼠标移动频率:" + str(value))
        self.mouse_move_frequency_label.adjustSize()

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
        self.config.set_config("move_step_y", self.move_step_y_slider.value())
        self.config.set_config("move_path_nx", self.move_path_nx_slider.value() / 10.0)
        self.config.set_config("move_path_ny", self.move_path_ny_slider.value() / 10.0)
        self.config.set_config("aim_move_step", self.aim_move_step_slider.value())
        self.config.set_config("aim_move_step_y", self.aim_move_step_y_slider.value())
        self.config.set_config("aim_move_path_nx", self.aim_move_path_nx_slider.value() / 10.0)
        self.config.set_config("aim_move_path_ny", self.aim_move_path_ny_slider.value() / 10.0)
        self.config.set_config("mouse_move_frequency", 1.0 / self.mouse_move_frequency_slider.value())

        self.config.set_config("cross_hair", (self.slider.value() / (
                self.slider.maximum() // 2)) - 1)
