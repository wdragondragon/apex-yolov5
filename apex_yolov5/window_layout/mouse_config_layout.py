from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget, QCheckBox, QComboBox

from apex_yolov5.mouse_mover import MoverFactory


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

        mouse_model_layout.addWidget(mouse_model_label)
        mouse_model_layout.addWidget(self.mouse_model_combo_box)

        aim_model_layout = QHBoxLayout()
        aim_model_label = QLabel("选择开镜瞄准模式")
        self.aim_model_combo_box = QComboBox()

        aim_model_layout.addWidget(aim_model_label)
        aim_model_layout.addWidget(self.aim_model_combo_box)

        self.dynamic_mouse_move = QCheckBox("动态移速")
        self.dynamic_mouse_move.setObjectName("dynamic_mouse_move")

        self.joy_move = QCheckBox("手柄模式")
        self.joy_move.setObjectName("joy_move")
        self.joy_move.toggled.connect(self.joy_move_toggled)

        self.mouse_smoothing_switch = QCheckBox("鼠标平滑（勾选后单词移动像素才生效）")
        self.mouse_smoothing_switch.setObjectName("mouse_smoothing_switch")
        self.mouse_smoothing_switch.toggled.connect(self.disable_silder_toggled)

        self.aim_button_layout = QHBoxLayout()
        self.aim_button_label = QLabel("自动标准触发按键:")
        self.left_aim = QCheckBox("左键")
        self.left_aim.setObjectName("left")
        self.left_aim.toggled.connect(self.handle_toggled)

        self.right_aim = QCheckBox("右键")
        self.right_aim.setObjectName("right")

        self.right_aim.toggled.connect(self.handle_toggled)

        self.x2_aim = QCheckBox("前侧键")
        self.x2_aim.setObjectName("x2")

        self.x2_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.left_aim)
        self.aim_button_layout.addWidget(self.right_aim)
        self.aim_button_layout.addWidget(self.x2_aim)

        self.x1_aim = QCheckBox("后侧键")
        self.x1_aim.setObjectName("x1")
        self.x1_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.x1_aim)

        self.x1_no_x2_aim = QCheckBox("右键除左键")
        self.x1_no_x2_aim.setObjectName("x1&!x2")
        self.x1_no_x2_aim.toggled.connect(self.handle_toggled)
        self.aim_button_layout.addWidget(self.x1_no_x2_aim)

        move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_label = QLabel("单次水平移动像素:", self.main_window)
        self.move_step_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_slider.setMinimum(1)  # 最小值
        self.move_step_slider.setMaximum(100)  # 最大值
        self.move_step_slider.valueChanged.connect(self.update_move_step_label)

        self.move_step_max_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_max_slider.setMinimum(1)  # 最小值
        self.move_step_max_slider.setMaximum(100)  # 最大值
        self.move_step_max_slider.valueChanged.connect(self.update_move_step_label)

        move_step_layout.addWidget(self.move_step_label)
        move_step_layout.addWidget(self.move_step_slider)
        move_step_layout.addWidget(self.move_step_max_slider)

        move_step_y_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_y_label = QLabel("单次垂直移动像素:", self.main_window)
        self.move_step_y_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_y_slider.setMinimum(1)  # 最小值
        self.move_step_y_slider.setMaximum(100)  # 最大值
        self.move_step_y_slider.valueChanged.connect(self.update_move_step_y_label)

        self.move_step_y_max_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_step_y_max_slider.setMinimum(1)  # 最小值
        self.move_step_y_max_slider.setMaximum(100)  # 最大值
        self.move_step_y_max_slider.valueChanged.connect(self.update_move_step_y_label)
        move_step_y_layout.addWidget(self.move_step_y_label)
        move_step_y_layout.addWidget(self.move_step_y_slider)
        move_step_y_layout.addWidget(self.move_step_y_max_slider)

        move_path_nx_layout = QHBoxLayout()
        self.move_path_nx_label = QLabel("移动水平路径倍率:", self.main_window)
        self.move_path_nx_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_path_nx_slider.setObjectName("move_path_nx")
        self.move_path_nx_slider.setMinimum(1)  # 最小值
        self.move_path_nx_slider.setMaximum(300)  # 最大值
        self.move_path_nx_slider.valueChanged.connect(self.update_move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_slider)

        move_path_ny_layout = QHBoxLayout()
        self.move_path_ny_label = QLabel("移动垂直路径倍率:", self.main_window)
        self.move_path_ny_slider = QSlider(Qt.Horizontal, self.main_window)
        self.move_path_ny_slider.setObjectName("move_path_ny")
        self.move_path_ny_slider.setMinimum(1)  # 最小值
        self.move_path_ny_slider.setMaximum(300)  # 最大值
        self.move_path_ny_slider.valueChanged.connect(self.update_move_path_ny_label)
        move_path_ny_layout.addWidget(self.move_path_ny_label)
        move_path_ny_layout.addWidget(self.move_path_ny_slider)

        aim_move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.aim_move_step_label = QLabel("瞄准时水平移动像素:", self.main_window)
        self.aim_move_step_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_slider.setMinimum(1)  # 最小值
        self.aim_move_step_slider.setMaximum(100)  # 最大值
        self.aim_move_step_slider.valueChanged.connect(self.update_aim_move_step_label)

        self.aim_move_step_max_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_max_slider.setMinimum(1)  # 最小值
        self.aim_move_step_max_slider.setMaximum(100)  # 最大值
        self.aim_move_step_max_slider.valueChanged.connect(self.update_aim_move_step_label)
        aim_move_step_layout.addWidget(self.aim_move_step_label)
        aim_move_step_layout.addWidget(self.aim_move_step_slider)
        aim_move_step_layout.addWidget(self.aim_move_step_max_slider)

        aim_move_step_y_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.aim_move_step_y_label = QLabel("瞄准时垂直移动像素:", self.main_window)
        self.aim_move_step_y_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_y_slider.setMinimum(1)  # 最小值
        self.aim_move_step_y_slider.setMaximum(100)  # 最大值
        self.aim_move_step_y_slider.valueChanged.connect(self.update_aim_move_step_y_label)

        self.aim_move_step_y_max_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_step_y_max_slider.setMinimum(1)  # 最小值
        self.aim_move_step_y_max_slider.setMaximum(100)  # 最大值
        self.aim_move_step_y_max_slider.valueChanged.connect(self.update_aim_move_step_y_label)

        aim_move_step_y_layout.addWidget(self.aim_move_step_y_label)
        aim_move_step_y_layout.addWidget(self.aim_move_step_y_slider)
        aim_move_step_y_layout.addWidget(self.aim_move_step_y_max_slider)

        aim_move_path_nx_layout = QHBoxLayout()
        self.aim_move_path_nx_label = QLabel("瞄准时移动水平路径倍率:", self.main_window)
        self.aim_move_path_nx_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_path_nx_slider.setObjectName("aim_move_path_nx")
        self.aim_move_path_nx_slider.setMinimum(0)  # 最小值
        self.aim_move_path_nx_slider.setMaximum(300)  # 最大值
        self.aim_move_path_nx_slider.valueChanged.connect(self.update_aim_move_path_nx_label)
        aim_move_path_nx_layout.addWidget(self.aim_move_path_nx_label)
        aim_move_path_nx_layout.addWidget(self.aim_move_path_nx_slider)

        aim_move_path_ny_layout = QHBoxLayout()
        self.aim_move_path_ny_label = QLabel("瞄准时移动垂直路径倍率:", self.main_window)
        self.aim_move_path_ny_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_move_path_ny_slider.setObjectName("aim_move_path_ny")
        self.aim_move_path_ny_slider.setMinimum(0)  # 最小值
        self.aim_move_path_ny_slider.setMaximum(300)  # 最大值
        self.aim_move_path_ny_slider.valueChanged.connect(self.update_aim_move_path_ny_label)
        aim_move_path_ny_layout.addWidget(self.aim_move_path_ny_label)
        aim_move_path_ny_layout.addWidget(self.aim_move_path_ny_slider)

        self.mouse_move_frequency_switch = QCheckBox("鼠标移动频率自适应（勾选后移动频率不生效）")
        self.mouse_move_frequency_switch.setObjectName("mouse_move_frequency_switch")
        self.mouse_move_frequency_switch.toggled.connect(self.disable_silder_toggled)

        mouse_move_frequency_layout = QHBoxLayout()
        self.mouse_move_frequency_label = QLabel("鼠标移动频率:", self.main_window)
        self.mouse_move_frequency_slider = QSlider(Qt.Horizontal, self.main_window)
        self.mouse_move_frequency_slider.setObjectName("mouse_move_frequency")
        self.mouse_move_frequency_slider.setMinimum(125)  # 最小值
        self.mouse_move_frequency_slider.setMaximum(4000)  # 最大值

        self.mouse_move_frequency_slider.valueChanged.connect(self.update_mouse_move_frequency_label)
        mouse_move_frequency_layout.addWidget(self.mouse_move_frequency_label)
        mouse_move_frequency_layout.addWidget(self.mouse_move_frequency_slider)

        aim_delay_layout = QHBoxLayout()
        self.aim_delay_label = QLabel("瞄准延迟范围:", self.main_window)
        self.aim_delay_min_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_delay_min_slider.setObjectName("aim_delay_min")
        self.aim_delay_min_slider.setMinimum(0)  # 最小值
        self.aim_delay_min_slider.setMaximum(1000)  # 最大值

        self.aim_delay_max_slider = QSlider(Qt.Horizontal, self.main_window)
        self.aim_delay_max_slider.setObjectName("aim_delay_max")
        self.aim_delay_max_slider.setMinimum(0)  # 最小值
        self.aim_delay_max_slider.setMaximum(1000)  # 最大值
        self.aim_delay_max_slider.setMinimum(self.aim_delay_min_slider.value())

        self.aim_delay_min_slider.valueChanged.connect(self.update_aim_delay_slider)  # 最大值
        self.aim_delay_max_slider.valueChanged.connect(self.update_aim_delay_slider)  # 最大值
        aim_delay_layout.addWidget(self.aim_delay_label)
        aim_delay_layout.addWidget(self.aim_delay_min_slider)
        aim_delay_layout.addWidget(self.aim_delay_max_slider)

        re_cut_size_layout = QHBoxLayout()
        self.re_cut_size_label = QLabel("单次移动最大像素:", self.main_window)
        self.re_cut_size_slider = QSlider(Qt.Horizontal, self.main_window)
        self.re_cut_size_slider.setObjectName("re_cut_size")
        self.re_cut_size_slider.setMinimum(0)  # 最小值
        self.re_cut_size_slider.setMaximum(100)  # 最大值
        self.re_cut_size_slider.valueChanged.connect(self.update_re_cut_size_label)  # 最大值
        re_cut_size_layout.addWidget(self.re_cut_size_label)
        re_cut_size_layout.addWidget(self.re_cut_size_slider)

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
        self.parent_layout.addWidget(self.joy_move)
        self.parent_layout.addWidget(self.dynamic_mouse_move)
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
        self.parent_layout.addLayout(aim_delay_layout)
        self.parent_layout.addLayout(re_cut_size_layout)

        self.parent_layout.addLayout(cross_layout)
        self.init_form_config()

    def init_form_config(self):
        self.mouse_model_combo_box.blockSignals(True)
        self.mouse_model_combo_box.clear()
        self.mouse_model_combo_box.blockSignals(False)
        for key in self.config.available_mouse_models.keys():
            self.mouse_model_combo_box.addItem(key)
        self.mouse_model_combo_box.setCurrentText(self.config.mouse_model)
        self.mouse_model_combo_box.currentIndexChanged.connect(self.selection_changed)

        self.aim_model_combo_box.blockSignals(True)
        self.aim_model_combo_box.clear()
        self.aim_model_combo_box.blockSignals(False)
        for key in self.config.aim_models:
            self.aim_model_combo_box.addItem(key)
        self.aim_model_combo_box.setCurrentText(self.config.aim_model)
        self.aim_model_combo_box.currentIndexChanged.connect(self.selection_aim_model_changed)

        self.joy_move.setChecked(self.config.joy_move)  # 初始化开关的值
        self.dynamic_mouse_move.setChecked(self.config.dynamic_mouse_move)  # 初始化开关的值

        self.mouse_smoothing_switch.setChecked(self.config.mouse_smoothing_switch)  # 初始化开关的值

        self.left_aim.setChecked("left" in self.config.aim_button)  # 初始化开关的值

        self.right_aim.setChecked("right" in self.config.aim_button)  # 初始化开关的值

        self.x2_aim.setChecked("x2" in self.config.aim_button)  # 初始化开关的值

        self.x1_aim.setChecked("x1" in self.config.aim_button)  # 初始化开关的值

        self.x1_no_x2_aim.setChecked("x1&!x2" in self.config.aim_button)  # 初始化开关的值

        self.move_step_label.setText(
            f"单次水平移动像素:{self.move_step_slider.value()}-{self.move_step_max_slider.value()}")
        self.move_step_slider.setValue(self.config.move_step)  # 初始化值
        self.move_step_max_slider.setValue(self.config.move_step_max)  # 初始化值
        self.move_step_slider.setEnabled(self.config.mouse_smoothing_switch)
        self.move_step_max_slider.setEnabled(self.config.mouse_smoothing_switch)

        self.move_step_y_label.setText(
            f"单次垂直移动像素:{self.move_step_y_slider.value()}-{self.move_step_y_max_slider.value()}")
        self.move_step_y_slider.setValue(self.config.move_step_y)  # 初始化值
        self.move_step_y_max_slider.setValue(self.config.move_step_y_max)  # 初始化值
        self.move_step_y_slider.setEnabled(self.config.mouse_smoothing_switch)
        self.move_step_y_max_slider.setEnabled(self.config.mouse_smoothing_switch)

        self.move_path_nx_label.setText("移动水平路径倍率:" + str(self.config.move_path_nx))
        self.move_path_nx_slider.setValue(int(self.config.move_path_nx * 10))  # 初始化值

        self.move_path_ny_label.setText("移动垂直路径倍率:" + str(self.config.move_path_ny))
        self.move_path_ny_slider.setValue(int(self.config.move_path_ny * 10))  # 初始化值

        self.move_step_label.setText(
            f"单次水平移动像素:{self.move_step_slider.value()}-{self.move_step_max_slider.value()}")
        self.aim_move_step_slider.setValue(self.config.aim_move_step)  # 初始化值
        self.aim_move_step_max_slider.setValue(self.config.aim_move_step_max)  # 初始化值
        self.aim_move_step_slider.setEnabled(self.config.mouse_smoothing_switch)
        self.aim_move_step_max_slider.setEnabled(self.config.mouse_smoothing_switch)

        self.aim_move_step_y_label.setText(
            f"瞄准时垂直移动像素:{self.aim_move_step_y_slider.value()}-{self.aim_move_step_y_max_slider.value()}")
        self.aim_move_step_y_slider.setValue(self.config.aim_move_step_y)  # 初始化值
        self.aim_move_step_y_max_slider.setValue(self.config.aim_move_step_y_max)  # 初始化值
        self.aim_move_step_y_slider.setEnabled(self.config.mouse_smoothing_switch)
        self.aim_move_step_y_max_slider.setEnabled(self.config.mouse_smoothing_switch)

        self.aim_move_path_nx_label.setText("瞄准时移动水平路径倍率:" + str(self.config.aim_move_path_nx))
        self.aim_move_path_nx_slider.setValue(int(self.config.aim_move_path_nx * 10))  # 初始化值

        self.aim_move_path_ny_label.setText("瞄准时移动垂直路径倍率:" + str(self.config.aim_move_path_ny))
        self.aim_move_path_ny_slider.setValue(int(self.config.aim_move_path_ny * 10))  # 初始化值

        self.mouse_move_frequency_switch.setChecked(self.config.mouse_move_frequency_switch)  # 初始化开关的值

        self.mouse_move_frequency_label.setText("鼠标移动频率:" + str(int(1 / self.config.mouse_move_frequency)))
        self.mouse_move_frequency_slider.setValue(int(1 / self.config.mouse_move_frequency))  # 初始化值

        self.re_cut_size_label.setText("单次移动最大像素:" + str(self.config.re_cut_size))
        self.re_cut_size_slider.setValue(int(self.config.re_cut_size))

        self.aim_delay_label.setText(
            f"瞄准延迟范围: {self.aim_delay_min_slider.value()}-{self.aim_delay_max_slider.value()}")

        self.mouse_move_frequency_slider.setEnabled(
            self.config.mouse_smoothing_switch and not self.config.mouse_move_frequency_switch)

        human_pix_map_height = self.human_pixmap.size().height()
        cross_position_height = int(
            (human_pix_map_height // 2) * (1 - self.config.cross_hair))

        self.crosshair_position = QPoint(
            self.human_pixmap.size().width() // 2 - self.crosshair_pixmap.size().width() // 2,
            cross_position_height - self.crosshair_pixmap.size().height() // 2)

        self.image_widget.update()

    def update_aim_delay_slider(self, value):
        # 如果第一个滑块的值大于等于第二个滑块的值，将第二个滑块的最小值设置为第一个滑块的值加1
        self.aim_delay_max_slider.setMinimum(self.aim_delay_min_slider.value())
        self.aim_delay_label.setText(
            f"瞄准延迟范围: {self.aim_delay_min_slider.value()}-{self.aim_delay_max_slider.value()}")

    def selection_changed(self, index):
        selected_key = self.mouse_model_combo_box.currentText()
        self.mouse_model_combo_box.setEnabled(False)
        self.config.set_config("mouse_model", selected_key)
        self.config.mouse_model = selected_key
        MoverFactory.reload_mover(self.config.mouse_model, self.config.available_mouse_models)
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

    def joy_move_toggled(self, checked):
        self.main_window.handle_toggled(checked)
        self.config.joy_move = checked
        if checked:
            from apex_yolov5.job_listener.JoyListener import get_joy_listener
            get_joy_listener().start(self.main_window)

    def update_move_step_label(self, value):
        self.move_step_max_slider.setMinimum(self.move_step_slider.value())
        self.move_step_label.setText(
            f"单次水平移动像素:{self.move_step_slider.value()}-{self.move_step_max_slider.value()}")
        self.move_step_label.adjustSize()

    def update_move_step_y_label(self, value):
        self.move_step_y_max_slider.setMinimum(self.move_step_y_slider.value())
        self.move_step_y_label.setText(
            f"单次垂直移动像素:{self.move_step_y_slider.value()}-{self.move_step_y_max_slider.value()}")
        self.move_step_y_label.adjustSize()

    def update_move_path_nx_label(self, value):
        self.move_path_nx_label.setText("移动水平路径倍率:" + str((1.0 * value) / 10))
        self.move_path_nx_label.adjustSize()

    def update_move_path_ny_label(self, value):
        self.move_path_ny_label.setText("移动垂直路径倍率:" + str((1.0 * value) / 10))
        self.move_path_ny_label.adjustSize()

    def update_aim_move_step_label(self, value):
        self.aim_move_step_max_slider.setMinimum(self.aim_move_step_slider.value())
        self.aim_move_step_label.setText(
            f"瞄准时水平移动像素:{self.aim_move_step_slider.value()}-{self.aim_move_step_max_slider.value()}")
        self.aim_move_step_label.adjustSize()

    def update_aim_move_step_y_label(self, value):
        self.aim_move_step_y_max_slider.setMinimum(self.aim_move_step_y_slider.value())
        self.aim_move_step_y_label.setText(
            f"瞄准时垂直移动像素:{self.aim_move_step_y_slider.value()}-{self.aim_move_step_y_max_slider.value()}")
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

    def update_re_cut_size_label(self, value):
        self.re_cut_size_label.setText("单次移动最大像素:" + str(value))
        self.re_cut_size_label.adjustSize()

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
        self.config.set_config("move_step_max", self.move_step_max_slider.value())
        self.config.set_config("move_step_y", self.move_step_y_slider.value())
        self.config.set_config("move_step_y_max", self.move_step_y_max_slider.value())
        self.config.set_config("move_path_nx", self.move_path_nx_slider.value() / 10.0)
        self.config.set_config("move_path_ny", self.move_path_ny_slider.value() / 10.0)
        self.config.set_config("aim_move_step", self.aim_move_step_slider.value())
        self.config.set_config("aim_move_step_max", self.aim_move_step_max_slider.value())
        self.config.set_config("aim_move_step_y", self.aim_move_step_y_slider.value())
        self.config.set_config("aim_move_step_y_max", self.aim_move_step_y_max_slider.value())
        self.config.set_config("aim_move_path_nx", self.aim_move_path_nx_slider.value() / 10.0)
        self.config.set_config("aim_move_path_ny", self.aim_move_path_ny_slider.value() / 10.0)
        self.config.set_config("mouse_move_frequency", 1.0 / self.mouse_move_frequency_slider.value())
        self.config.set_config("re_cut_size", int(self.re_cut_size_slider.value()))

        self.config.set_config("cross_hair", (self.slider.value() / (
                self.slider.maximum() // 2)) - 1)

        self.config.set_config("dynamic_mouse_move", self.dynamic_mouse_move.isChecked())
        self.config.set_config("aiming_delay_min", self.aim_delay_min_slider.value())
        self.config.set_config("aiming_delay_max", self.aim_delay_max_slider.value())
