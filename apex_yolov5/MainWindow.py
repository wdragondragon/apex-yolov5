import os

from PyQt5.QtCore import QPoint, QRect, Qt, QRectF, QPointF
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QPainterPath, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QAction, QApplication, QSlider, QHBoxLayout, \
    QListWidget, QCheckBox, QGraphicsRectItem, QGraphicsItem, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from apex_yolov5.socket.config import global_config


class MainWindow(QMainWindow):
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.config_window = None
        if not hasattr(self, 'image_label'):
            self.image_label = None
            self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 400, 300)
        self.create_menus()

        self.image_label = QLabel(self)
        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_menus(self):
        config_action = QAction("Config", self)
        config_action.triggered.connect(self.open_config_window)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(config_action)

    def open_config_window(self):
        if self.config_window is None:
            self.config_window = ConfigWindow(global_config)
        self.config_window.show()

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

    def closeEvent(self, event):
        QApplication.quit()
        os._exit(0)

    # def print_log(self, log):
    #     # 获取当前日期和时间
    #     now = datetime.now()
    #     # 格式化日期为字符串
    #     formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    #     msg = "[{}]{}".format(formatted_date, log)
    #     if global_config.is_show_debug_window:
    #         self.log_text.append(msg)
    #         self.log_text.moveCursor(self.log_text.textCursor().End)
    #     print(msg)


class ConfigWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def initUI(self):
        self.setWindowTitle("Config Window")
        self.setGeometry(100, 100, 250, 200)
        config_layout = QVBoxLayout()
        move_step_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.move_step_label = QLabel("单次移动像素:" + str(self.config.move_step), self)
        self.move_step_slider = QSlider(Qt.Horizontal, self)
        self.move_step_slider.setMinimum(1)  # 最小值
        self.move_step_slider.setMaximum(30)  # 最大值
        self.move_step_slider.setValue(self.config.move_step)  # 初始化值
        self.move_step_slider.valueChanged.connect(self.update_move_step_label)
        move_step_layout.addWidget(self.move_step_label)
        move_step_layout.addWidget(self.move_step_slider)

        move_path_nx_layout = QHBoxLayout()
        self.move_path_nx_label = QLabel("移动路径倍率:" + str(self.config.move_path_nx), self)
        self.move_path_nx_slider = QSlider(Qt.Horizontal, self)
        self.move_path_nx_slider.setMinimum(1)  # 最小值
        self.move_path_nx_slider.setMaximum(300)  # 最大值
        self.move_path_nx_slider.setValue(int(self.config.move_path_nx * 10))  # 初始化值
        self.move_path_nx_slider.valueChanged.connect(self.update_move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_label)
        move_path_nx_layout.addWidget(self.move_path_nx_slider)

        cross_layout = QHBoxLayout()
        self.cross_label = QLabel("瞄准高度：", self)
        self.human_pixmap = QPixmap("images/human.jpg").scaled(100, 200, Qt.KeepAspectRatio)
        self.crosshair_pixmap = QPixmap("images/crosshair.jpg").scaled(50, 50, Qt.KeepAspectRatio)
        human_pix_map_height = self.human_pixmap.size().height()
        cross_position_height = int(
            (human_pix_map_height // 2) * (1 - self.config.cross_hair))

        self.crosshair_position = QPoint(
            self.human_pixmap.size().width() // 2 - self.crosshair_pixmap.size().width() // 2,
            cross_position_height - self.crosshair_pixmap.size().height() // 2)
        self.image_widget = QWidget(self)
        self.image_widget.setFixedSize(self.human_pixmap.size())
        self.image_widget.paintEvent = self.paintEvent
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.human_pixmap.height())
        self.slider.setValue(self.slider.maximum() - cross_position_height)  # 反转滑动条的值
        self.slider.valueChanged.connect(self.move_crosshair)
        cross_layout.addWidget(self.cross_label)
        cross_layout.addWidget(self.slider)
        cross_layout.addWidget(self.image_widget)

        add_refresh_button_title_layout = QVBoxLayout()
        add_refresh_button_layout = QHBoxLayout()
        add_refresh_button_input_layout = QVBoxLayout()
        self.refresh_button_title = QLabel("触发枪械识别按键列表", self)
        self.refresh_button_title.setAlignment(Qt.AlignCenter)
        self.fresh_button_list = QListWidget(self)
        self.refresh_button_input = QLineEdit()
        self.fresh_button_list.addItems(self.config.refresh_button)
        self.add_refresh_button = QPushButton("Add")
        self.add_refresh_button.clicked.connect(self.add_refresh_button_item)
        self.remove_refresh_button = QPushButton("Remove", self)
        self.remove_refresh_button.clicked.connect(self.delete_refresh_button_item)

        add_refresh_button_input_layout.addWidget(self.refresh_button_input)
        add_refresh_button_input_layout.addWidget(self.add_refresh_button)
        add_refresh_button_input_layout.addWidget(self.remove_refresh_button)
        add_refresh_button_layout.addWidget(self.fresh_button_list)
        add_refresh_button_layout.addLayout(add_refresh_button_input_layout)
        add_refresh_button_title_layout.addWidget(self.refresh_button_title)
        add_refresh_button_title_layout.addLayout(add_refresh_button_layout)

        list_layout = QHBoxLayout()
        list_layout_label = QLabel("自动开枪枪械识别列表", self)
        list_layout_label.setAlignment(Qt.AlignCenter)
        available_layout = QVBoxLayout()
        self.available_guns_label = QLabel("可用枪支", self)
        self.available_guns = [item for item in self.config.available_guns if item not in self.config.click_gun]
        self.available_guns_list = QListWidget(self)
        self.available_guns_list.addItems(self.available_guns)  # 假设config.available_guns是一个包含所有可用枪支的列表
        self.available_guns_list.setMinimumSize(150, 200)
        available_layout.addWidget(self.available_guns_label)
        available_layout.addWidget(self.available_guns_list)
        list_layout.addLayout(available_layout)

        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Add >>", self)
        self.add_button.clicked.connect(self.addGun)
        button_layout.addWidget(self.add_button)
        self.remove_button = QPushButton("<< Remove", self)
        self.remove_button.clicked.connect(self.removeGun)
        button_layout.addWidget(self.remove_button)
        list_layout.addLayout(button_layout)

        add_guns_layout = QVBoxLayout()
        self.add_guns_label = QLabel("已选择枪支", self)
        self.selected_guns_list = QListWidget(self)
        self.selected_guns_list.addItems(self.config.click_gun)  # 假设config.click_gun是一个包含已选择枪支的列表
        self.selected_guns_list.setMinimumSize(150, 200)
        add_guns_layout.addWidget(self.add_guns_label)
        add_guns_layout.addWidget(self.selected_guns_list)
        list_layout.addLayout(add_guns_layout)

        toggle_layout = QVBoxLayout(self)

        self.is_show_debug_window_switch = QCheckBox("主页人物实时图像")
        self.is_show_debug_window_switch.setObjectName("is_show_debug_window")
        self.is_show_debug_window_switch.setChecked(self.config.is_show_debug_window)  # 初始化开关的值
        self.is_show_debug_window_switch.toggled.connect(self.handle_toggled)
        toggle_layout.addWidget(self.is_show_debug_window_switch)

        self.auto_save_switch = QCheckBox("自动保存标注文件")
        self.auto_save_switch.setObjectName("auto_save")
        self.auto_save_switch.setChecked(self.config.auto_save)  # 初始化开关的值
        self.auto_save_switch.toggled.connect(self.handle_toggled)
        toggle_layout.addWidget(self.auto_save_switch)

        self.only_save_switch = QCheckBox("仅保存标注文件（不开启自瞄）")
        self.only_save_switch.setObjectName("only_save")
        self.only_save_switch.setChecked(self.config.only_save)  # 初始化开关的值
        self.only_save_switch.toggled.connect(self.handle_toggled)
        toggle_layout.addWidget(self.only_save_switch)

        screenshot_area_layout = QVBoxLayout(self)
        resolution_layout = QHBoxLayout(self)
        self.screenshot_area_label = QLabel("截图区域：", self)
        self.screenshot_area_x_label = QLabel("x", self)

        self.width_input = QLineEdit(self)
        self.height_input = QLineEdit(self)
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

        self.view = RectView(self,
                             outer_rect_size=(
                                 int(self.config.screen_width / 10), int(self.config.screen_height / 10)),
                             inner_rect_size=(
                                 int(self.config.shot_height / 10), int(self.config.shot_width / 10)))
        screenshot_area_layout.addLayout(resolution_layout)
        screenshot_area_layout.addWidget(self.view)

        config_layout.addLayout(move_step_layout)
        config_layout.addLayout(move_path_nx_layout)
        config_layout.addLayout(cross_layout)
        config_layout.addLayout(add_refresh_button_title_layout)
        config_layout.addWidget(list_layout_label)
        config_layout.addLayout(list_layout)
        config_layout.addLayout(toggle_layout)
        config_layout.addLayout(screenshot_area_layout)
        # 创建保存按钮
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.saveConfig)

        config_layout.addWidget(self.save_button)
        container = QWidget()
        container.setLayout(config_layout)
        self.setCentralWidget(container)

    def update_move_step_label(self, value):
        self.move_step_label.setText("单次移动像素:" + str(value))
        self.move_step_label.adjustSize()

    def update_move_path_nx_label(self, value):
        self.move_path_nx_label.setText("移动路径倍率:" + str(value))
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

    def add_refresh_button_item(self):
        new_item = self.refresh_button_input.text()
        if new_item:
            self.fresh_button_list.addItem(new_item)
            self.config.refresh_button.append(new_item)

    def delete_refresh_button_item(self):
        selected_items = self.fresh_button_list.selectedItems()
        for item in selected_items:
            self.fresh_button_list.takeItem(self.fresh_button_list.row(item))
            self.config.refresh_button.remove(item.text())

    def addGun(self):
        selected_guns = self.available_guns_list.selectedItems()
        for gun in selected_guns:
            self.available_guns_list.takeItem(self.available_guns_list.row(gun))
            self.selected_guns_list.addItem(gun)
            self.config.click_gun.append(gun.text())
            self.available_guns.remove(gun.text())

    def removeGun(self):
        selected_guns = self.selected_guns_list.selectedItems()
        for gun in selected_guns:
            self.selected_guns_list.takeItem(self.selected_guns_list.row(gun))
            self.available_guns_list.addItem(gun)
            self.config.click_gun.remove(gun.text())
            self.available_guns.append(gun.text())

    def handle_toggled(self, checked):
        self.config.set_config(self.sender().objectName(), checked)

    def update_inner_rect_size(self):
        # 当输入框的内容改变时，更新内部框的大小
        width = int(self.width_input.text()) if self.width_input.text() else 0
        height = int(self.height_input.text()) if self.height_input.text() else 0
        self.view.resize_inner_rect(width, height)

    def saveConfig(self):
        # 从界面获取新值
        new_move_step = self.move_step_slider.value()
        new_move_path_nx = self.move_path_nx_slider.value() / 10.0
        new_cross_hair = (self.slider.value() / (self.slider.maximum() // 2)) - 1

        # 更新配置对象的属性
        self.config.set_config("move_step", new_move_step)
        self.config.set_config("move_path_nx", new_move_path_nx)
        self.config.set_config("cross_hair", new_cross_hair)
        self.config.set_config("shot_width", int(self.view.inner_rect.rect().width() * 10))
        self.config.set_config("shot_height", int(self.view.inner_rect.rect().height() * 10))

        self.config.save_config()
        self.destroy()


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
