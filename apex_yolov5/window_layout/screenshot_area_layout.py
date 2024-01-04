from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QIntValidator, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QCheckBox, \
    QMessageBox

from apex_yolov5.windows.aim_show_window import get_aim_show_window, destory_aim_show_window
from apex_yolov5.windows.circle_window import get_circle_window, destory_circle_window


class ScreenshotAreaLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        screenshot_area_layout = QVBoxLayout()
        screenshot_area_layout.setObjectName("screenshot_area_layout")
        self.screenshot_area_title_label = QLabel("识别范围设置")
        self.screenshot_area_title_label.setAlignment(Qt.AlignCenter)

        show_circle_layout = QHBoxLayout()
        self.show_circle_toggle_switch = QCheckBox("展示瞄准范围")
        self.show_circle_toggle_switch.setObjectName("show_circle_toggle_switch")
        self.show_circle_toggle_switch.toggled.connect(self.show_circle_toggle)

        self.show_aim_toggle_switch = QCheckBox("标记瞄准目标")
        self.show_aim_toggle_switch.setObjectName("show_aim_toggle_switch")
        self.show_aim_toggle_switch.toggled.connect(self.show_aim_toggle)
        show_circle_layout.addWidget(self.show_circle_toggle_switch)
        show_circle_layout.addWidget(self.show_aim_toggle_switch)

        resolution_layout = QHBoxLayout()
        self.screenshot_area_label = QLabel("识别区域：", self.main_window)
        self.screenshot_area_x_label = QLabel("x", self.main_window)

        self.width_input = QLineEdit(self.main_window)
        self.height_input = QLineEdit(self.main_window)
        self.width_input.setText(str(int(self.config.shot_width)))
        self.height_input.setText(str(int(self.config.shot_height)))
        # 连接信号和槽
        self.width_input.textChanged.connect(self.update_inner_rect_size)
        self.height_input.textChanged.connect(self.update_inner_rect_size)
        self.width_input.setValidator(QIntValidator(0, self.config.desktop_width))
        self.height_input.setValidator(QIntValidator(0, self.config.desktop_height))
        resolution_layout.addWidget(self.screenshot_area_label)
        resolution_layout.addWidget(self.width_input)
        resolution_layout.addWidget(self.screenshot_area_x_label)
        resolution_layout.addWidget(self.height_input)

        dynamic_screenshot_layout = QVBoxLayout()
        self.dynamic_screenshot_area_toggle = QCheckBox("开启动态识别区域")
        self.dynamic_screenshot_area_toggle.toggled.connect(self.dynamic_screenshot_toggle)
        dynamic_screenshot_upper_layout = QHBoxLayout()
        self.dynamic_screenshot_upper_label = QLabel("最大区域：")
        self.dynamic_screenshot_upper_x_label = QLabel("x", self.main_window)
        self.dynamic_upper_width_input = QLineEdit()
        self.dynamic_upper_height_input = QLineEdit()
        dynamic_screenshot_upper_layout.addWidget(self.dynamic_screenshot_upper_label)
        dynamic_screenshot_upper_layout.addWidget(self.dynamic_upper_width_input)
        dynamic_screenshot_upper_layout.addWidget(self.dynamic_screenshot_upper_x_label)
        dynamic_screenshot_upper_layout.addWidget(self.dynamic_upper_height_input)

        dynamic_screenshot_lower_layout = QHBoxLayout()
        self.dynamic_screenshot_lower_label = QLabel("最小区域：")
        self.dynamic_screenshot_lower_x_label = QLabel("x", self.main_window)
        self.dynamic_lower_width_input = QLineEdit()
        self.dynamic_lower_height_input = QLineEdit()
        dynamic_screenshot_lower_layout.addWidget(self.dynamic_screenshot_lower_label)
        dynamic_screenshot_lower_layout.addWidget(self.dynamic_lower_width_input)
        dynamic_screenshot_lower_layout.addWidget(self.dynamic_screenshot_lower_x_label)
        dynamic_screenshot_lower_layout.addWidget(self.dynamic_lower_height_input)

        dynamic_screenshot_param_layout = QVBoxLayout()
        dynamic_screenshot_windows_layout = QHBoxLayout()
        self.dynamic_screenshot_collection_window_label = QLabel("采样窗口：")
        self.dynamic_screenshot_collection_window_input = QLineEdit()
        self.dynamic_screenshot_step_label = QLabel("动态步长：")
        self.dynamic_screenshot_step_input = QLineEdit()
        dynamic_screenshot_windows_layout.addWidget(self.dynamic_screenshot_step_label)
        dynamic_screenshot_windows_layout.addWidget(self.dynamic_screenshot_step_input)
        dynamic_screenshot_windows_layout.addWidget(self.dynamic_screenshot_collection_window_label)
        dynamic_screenshot_windows_layout.addWidget(self.dynamic_screenshot_collection_window_input)

        dynamic_screenshot_threshold_layout = QHBoxLayout()
        self.dynamic_screenshot_reduce_threshold_label = QLabel("缩小阈值：")
        self.dynamic_screenshot_reduce_threshold_input = QLineEdit()
        self.dynamic_screenshot_increase_threshold_label = QLabel("放大阈值：")
        self.dynamic_screenshot_increase_threshold_input = QLineEdit()
        dynamic_screenshot_threshold_layout.addWidget(self.dynamic_screenshot_reduce_threshold_label)
        dynamic_screenshot_threshold_layout.addWidget(self.dynamic_screenshot_reduce_threshold_input)
        dynamic_screenshot_threshold_layout.addWidget(self.dynamic_screenshot_increase_threshold_label)
        dynamic_screenshot_threshold_layout.addWidget(self.dynamic_screenshot_increase_threshold_input)
        dynamic_screenshot_param_layout.addLayout(dynamic_screenshot_windows_layout)
        dynamic_screenshot_param_layout.addLayout(dynamic_screenshot_threshold_layout)

        dynamic_screenshot_layout.addWidget(self.dynamic_screenshot_area_toggle)
        dynamic_screenshot_layout.addLayout(dynamic_screenshot_lower_layout)
        dynamic_screenshot_layout.addLayout(dynamic_screenshot_upper_layout)
        dynamic_screenshot_layout.addLayout(dynamic_screenshot_param_layout)

        aim_radius_layout = QHBoxLayout()
        self.mouse_moving_radius_label = QLabel("腰射自瞄半径：")
        self.mouse_moving_radius_input = QLineEdit(self.main_window)
        self.mouse_moving_radius_input.setObjectName("mouse_moving_radius")
        self.mouse_moving_radius_input.setText(str(int(self.config.mouse_moving_radius)))
        self.mouse_moving_radius_input.textChanged.connect(self.update_inner_circle_size)

        self.aim_mouse_moving_radius_label = QLabel("瞄准自瞄半径：")
        self.aim_mouse_moving_radius_input = QLineEdit(self.main_window)
        self.aim_mouse_moving_radius_input.setObjectName("aim_mouse_moving_radius")
        self.aim_mouse_moving_radius_input.setText(str(int(self.config.aim_mouse_moving_radius)))
        # 连接信号和槽
        self.aim_mouse_moving_radius_input.textChanged.connect(self.update_inner_circle_size)

        aim_radius_layout.addWidget(self.mouse_moving_radius_label)
        aim_radius_layout.addWidget(self.mouse_moving_radius_input)
        aim_radius_layout.addWidget(self.aim_mouse_moving_radius_label)
        aim_radius_layout.addWidget(self.aim_mouse_moving_radius_input)

        stage_aiming_speed_toggle_layout = QHBoxLayout()
        self.multi_stage_aiming_speed_toggle = QCheckBox("开启多级瞄速")
        self.multi_stage_aiming_speed_toggle.setObjectName("multi_stage_aiming_speed_toggle")

        self.based_on_character_box = QCheckBox("基于人物框倍率的多级瞄速")
        self.based_on_character_box.setObjectName("based_on_character_box")

        stage_aiming_speed_toggle_layout.addWidget(self.multi_stage_aiming_speed_toggle)
        stage_aiming_speed_toggle_layout.addWidget(self.based_on_character_box)

        multi_stage_aiming_speed_layout = QHBoxLayout()
        self.multi_stage_aiming_speed_label = QLabel("腰射多级瞄速：")
        self.multi_stage_aiming_speed_input = QLineEdit(self.main_window)
        self.multi_stage_aiming_speed_input.setObjectName("multi_stage_aiming_speed")

        # 连接信号和槽
        multi_stage_aiming_speed_layout.addWidget(self.multi_stage_aiming_speed_label)
        multi_stage_aiming_speed_layout.addWidget(self.multi_stage_aiming_speed_input)

        aim_multi_stage_aiming_speed_layout = QHBoxLayout()
        self.aim_multi_stage_aiming_speed_label = QLabel("瞄准多级瞄速：")
        self.aim_multi_stage_aiming_speed_input = QLineEdit(self.main_window)
        self.aim_multi_stage_aiming_speed_input.setObjectName("aim_multi_stage_aiming_speed")

        # 连接信号和槽
        aim_multi_stage_aiming_speed_layout.addWidget(self.aim_multi_stage_aiming_speed_label)
        aim_multi_stage_aiming_speed_layout.addWidget(self.aim_multi_stage_aiming_speed_input)

        self.view = RectView(self.main_window,
                             outer_rect_size=(
                                 int(self.config.desktop_width / 10), int(self.config.desktop_height / 10)),
                             inner_rect_size=(
                                 int(self.config.shot_width / 10), int(self.config.shot_height / 10)),
                             radius=int(self.config.mouse_moving_radius / 10),
                             aim_radius=int(self.config.aim_mouse_moving_radius / 10))
        screenshot_area_layout.addWidget(self.screenshot_area_title_label)
        screenshot_area_layout.addLayout(show_circle_layout)
        screenshot_area_layout.addLayout(resolution_layout)
        screenshot_area_layout.addLayout(aim_radius_layout)
        screenshot_area_layout.addLayout(stage_aiming_speed_toggle_layout)
        screenshot_area_layout.addLayout(multi_stage_aiming_speed_layout)
        screenshot_area_layout.addLayout(aim_multi_stage_aiming_speed_layout)
        screenshot_area_layout.addWidget(self.view)
        screenshot_area_layout.addLayout(dynamic_screenshot_layout)

        self.parent_layout.addLayout(screenshot_area_layout)

        self.init_form_config()

    def init_form_config(self):
        self.width_input.setText(str(int(self.config.shot_width)))
        self.height_input.setText(str(int(self.config.shot_height)))
        self.width_input.setValidator(QIntValidator(0, self.config.desktop_width))
        self.height_input.setValidator(QIntValidator(0, self.config.desktop_height))
        self.mouse_moving_radius_input.setText(str(int(self.config.mouse_moving_radius)))
        self.aim_mouse_moving_radius_input.setText(str(int(self.config.aim_mouse_moving_radius)))
        self.multi_stage_aiming_speed_input.setText(
            " ".join([f"{self.delete_extra_zero(start)}-{self.delete_extra_zero(end)}" for start, end in
                      self.config.multi_stage_aiming_speed]))
        self.aim_multi_stage_aiming_speed_input.setText(
            " ".join([f"{self.delete_extra_zero(start)}-{self.delete_extra_zero(end)}" for start, end in
                      self.config.aim_multi_stage_aiming_speed]))

        self.multi_stage_aiming_speed_toggle.setChecked(self.config.multi_stage_aiming_speed_toggle)
        self.based_on_character_box.setChecked(self.config.based_on_character_box)
        self.show_circle_toggle_switch.setChecked(self.config.show_circle)
        self.show_aim_toggle_switch.setChecked(self.config.show_aim)
        self.dynamic_screenshot_area_toggle.setDisabled(self.config.screenshot_frequency_mode == "asyn")
        self.dynamic_screenshot_area_toggle.setChecked(self.config.dynamic_screenshot)
        self.dynamic_upper_width_input.setText(str(self.config.dynamic_upper_width))
        self.dynamic_upper_height_input.setText(str(self.config.dynamic_upper_height))
        self.dynamic_lower_width_input.setText(str(self.config.dynamic_lower_width))
        self.dynamic_lower_height_input.setText(str(self.config.dynamic_lower_height))
        self.dynamic_screenshot_step_input.setText(str(self.config.dynamic_screenshot_step))
        self.dynamic_screenshot_collection_window_input.setText(str(self.config.dynamic_screenshot_collection_window))
        self.dynamic_screenshot_reduce_threshold_input.setText(str(self.config.dynamic_screenshot_reduce_threshold))
        self.dynamic_screenshot_increase_threshold_input.setText(str(self.config.dynamic_screenshot_increase_threshold))
        self.dynamic_screenshot_toggle(self.config.dynamic_screenshot)

    def delete_extra_zero(self, n):
        """删除小数点后多余的0"""
        n = '{:g}'.format(n)
        n = float(n) if '.' in n else int(n)  # 含小数点转float否则int
        return n

    def dynamic_screenshot_toggle(self, checked):
        self.dynamic_screenshot_upper_label.setVisible(checked)
        self.dynamic_screenshot_upper_x_label.setVisible(checked)
        self.dynamic_upper_width_input.setVisible(checked)
        self.dynamic_upper_height_input.setVisible(checked)
        self.dynamic_screenshot_lower_label.setVisible(checked)
        self.dynamic_screenshot_lower_x_label.setVisible(checked)
        self.dynamic_lower_width_input.setVisible(checked)
        self.dynamic_lower_height_input.setVisible(checked)
        self.dynamic_screenshot_step_label.setVisible(checked)
        self.dynamic_screenshot_step_input.setVisible(checked)
        self.dynamic_screenshot_collection_window_label.setVisible(checked)
        self.dynamic_screenshot_collection_window_input.setVisible(checked)
        self.dynamic_screenshot_reduce_threshold_label.setVisible(checked)
        self.dynamic_screenshot_reduce_threshold_input.setVisible(checked)
        self.dynamic_screenshot_increase_threshold_label.setVisible(checked)
        self.dynamic_screenshot_increase_threshold_input.setVisible(checked)

    def show_circle_toggle(self, checked):
        self.config.set_config("show_circle", checked)
        self.config.show_circle = checked
        if self.config.show_circle:
            get_circle_window().show()
        else:
            destory_circle_window()

    def show_aim_toggle(self, checked):
        self.config.set_config("show_aim", checked)
        self.config.show_aim = checked
        if self.config.show_aim:
            get_aim_show_window().show()
        else:
            destory_aim_show_window()

    def update_inner_rect_size(self):
        # 当输入框的内容改变时，更新内部框的大小
        width = int(self.width_input.text()) if self.width_input.text() else 0
        height = int(self.height_input.text()) if self.height_input.text() else 0
        self.view.resize_inner_rect(width, height)

    def update_inner_circle_size(self):
        object_name = self.main_window.sender().objectName()
        if object_name == "mouse_moving_radius":
            radius = int(self.mouse_moving_radius_input.text()) if self.mouse_moving_radius_input.text() else 0
            self.view.resize_inner_circle(radius)
        elif object_name == "aim_mouse_moving_radius":
            radius = int(self.aim_mouse_moving_radius_input.text()) if self.aim_mouse_moving_radius_input.text() else 0
            self.view.resize_inner_circle_aim(radius)

    def check_multi_stage_aiming_speed(self, speed_up, multi_stage_aiming_speed_str):
        if multi_stage_aiming_speed_str is None or multi_stage_aiming_speed_str == "":
            return []
        multi_stage_aiming_speed_arr = multi_stage_aiming_speed_str.split(" ")
        number_array = []
        for num_str in multi_stage_aiming_speed_arr:
            try:
                num_str_arr = num_str.split("-")
                num_one = float(num_str_arr[0])
                num_two = float(num_str_arr[1])
                if not (len(num_str_arr) == 2 and num_two >= num_one):
                    QMessageBox.warning(self.main_window, "不符合条件",
                                        f"{num_str_arr} 格式错误，格式为 数字-数字，且前一位大于后一位")

                if not 0 <= num_two <= speed_up:
                    QMessageBox.warning(self.main_window, "不符合条件", f"{num_two} 数字不允许比瞄准范围大")
                    return []
                else:
                    number_array.append((num_one, num_two))
            except ValueError:
                QMessageBox.critical(self.main_window, "错误", f"{num_str} 格式错误")
                return []
        return number_array

    def save_config(self):
        self.config.set_config("shot_width", int(self.view.inner_rect.rect().width() * 10))
        self.config.set_config("shot_height", int(self.view.inner_rect.rect().height() * 10))
        self.config.set_config("mouse_moving_radius", int(self.mouse_moving_radius_input.text()))
        self.config.set_config("aim_mouse_moving_radius", int(self.aim_mouse_moving_radius_input.text()))

        multi_stage_aiming_speed_arr = self.check_multi_stage_aiming_speed(self.config.mouse_moving_radius,
                                                                           self.multi_stage_aiming_speed_input.text())
        self.config.set_config("multi_stage_aiming_speed", multi_stage_aiming_speed_arr)

        aim_multi_stage_aiming_speed_arr = self.check_multi_stage_aiming_speed(self.config.aim_mouse_moving_radius,
                                                                               self.aim_multi_stage_aiming_speed_input
                                                                               .text())
        self.config.set_config("aim_multi_stage_aiming_speed", aim_multi_stage_aiming_speed_arr)

        self.config.set_config("multi_stage_aiming_speed_toggle", self.multi_stage_aiming_speed_toggle.isChecked())
        self.config.set_config("based_on_character_box", self.based_on_character_box.isChecked())

        self.config.set_config("dynamic_screenshot", self.dynamic_screenshot_area_toggle.isChecked())
        self.config.set_config("dynamic_upper_width", int(self.dynamic_upper_width_input.text()))
        self.config.set_config("dynamic_upper_height", int(self.dynamic_upper_height_input.text()))
        self.config.set_config("dynamic_lower_width", int(self.dynamic_lower_width_input.text()))
        self.config.set_config("dynamic_lower_height", int(self.dynamic_lower_height_input.text()))
        self.config.set_config("dynamic_screenshot_step", int(self.dynamic_screenshot_step_input.text()))
        self.config.set_config("dynamic_screenshot_collection_window",
                               int(self.dynamic_screenshot_collection_window_input.text()))
        self.config.set_config("dynamic_screenshot_reduce_threshold",
                               float(self.dynamic_screenshot_reduce_threshold_input.text()))
        self.config.set_config("dynamic_screenshot_increase_threshold",
                               float(self.dynamic_screenshot_increase_threshold_input.text()))


class RectView(QGraphicsView):
    def __init__(self, parent=None, outer_rect_size=(192, 108), inner_rect_size=(64, 64), radius=32, aim_radius=32):
        super(RectView, self).__init__(parent)
        self.setMinimumSize(*outer_rect_size)
        self.setScene(QGraphicsScene(self))

        self.outer_rect = self.scene().addRect(QRectF(0, 0, *outer_rect_size))  # 外部框
        self.outer_rect.setBrush(QColor(255, 0, 0))

        self.inner_rect = self.scene().addRect(QRectF(0, 0, *inner_rect_size))  # 内部框
        self.inner_rect.setBrush(QColor(0, 255, 0))
        self.center_inner_rect()

        self.inner_circle = self.scene().addEllipse(QRectF(0, 0, radius * 2, radius * 2))
        self.inner_circle.setBrush(QColor(0, 0, 255))
        self.center_inner_circle()

        self.inner_circle_aim = self.scene().addEllipse(QRectF(0, 0, aim_radius * 2, aim_radius * 2))
        self.inner_circle_aim.setBrush(QColor(0, 255, 255))
        self.center_inner_circle_aim()

    def center_inner_rect(self):
        # 将内部框居中
        self.inner_rect.setPos((self.outer_rect.rect().width() - self.inner_rect.rect().width()) / 2,
                               (self.outer_rect.rect().height() - self.inner_rect.rect().height()) / 2)

    def center_inner_circle(self):
        self.inner_circle.setPos((self.outer_rect.rect().width() - self.inner_circle.rect().width()) / 2,
                                 (self.outer_rect.rect().height() - self.inner_circle.rect().height()) / 2)

    def center_inner_circle_aim(self):
        self.inner_circle_aim.setPos((self.outer_rect.rect().width() - self.inner_circle_aim.rect().width()) / 2,
                                     (self.outer_rect.rect().height() - self.inner_circle_aim.rect().height()) / 2)

    def resize_inner_rect(self, width, height):
        # 改变内部框的大小
        self.inner_rect.setRect(0, 0, width / 10, height / 10)
        self.center_inner_rect()

    def resize_inner_circle(self, radius):
        self.inner_circle.setRect(0, 0, radius * 2 / 10, radius * 2 / 10)
        self.center_inner_circle()

    def resize_inner_circle_aim(self, radius):
        self.inner_circle_aim.setRect(0, 0, radius * 2 / 10, radius * 2 / 10)
        self.center_inner_circle_aim()
