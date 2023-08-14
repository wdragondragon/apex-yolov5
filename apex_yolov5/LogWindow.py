import os

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QAction, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from apex_yolov5.socket.config import global_config


class LogWindow(QMainWindow):
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
            # self.app = QApplication(sys.argv)
            self.image_label = None
            self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 400, 300)
        self.create_menus()

        # 创建 QTextEdit 组件用于显示日志
        # self.log_text = QTextEdit()
        # self.log_text.document().setMaximumBlockCount(200)
        # self.log_text.setReadOnly(True)

        self.image_label = QLabel(self)
        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        # layout.addWidget(self.log_text)

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

    def initUI(self):
        self.setWindowTitle("Config Window")
        self.setGeometry(100, 100, 300, 200)

        # 创建标签和文本框
        self.move_step_label = QLabel("Move Step:", self)
        self.move_step_label.move(20, 20)
        self.move_step_textbox = QLineEdit(self)
        self.move_step_textbox.move(120, 20)

        self.move_path_nx_label = QLabel("Move Path NX:", self)
        self.move_path_nx_label.move(20, 60)
        self.move_path_nx_textbox = QLineEdit(self)
        self.move_path_nx_textbox.move(120, 60)

        # 创建保存按钮
        self.save_button = QPushButton("Save", self)
        self.save_button.move(120, 100)
        self.save_button.clicked.connect(self.saveConfig)

        # 初始化文本框的值
        self.move_step_textbox.setText(str(self.config.move_step))
        self.move_path_nx_textbox.setText(str(self.config.move_path_nx))

    def saveConfig(self):
        # 从界面获取新值
        new_move_step = int(self.move_step_textbox.text())
        new_move_path_nx = int(self.move_path_nx_textbox.text())
        # 更新配置对象的属性
        self.config.set_config("move_step", new_move_step)
        self.config.set_config("move_path_nx", new_move_path_nx)
        self.config.save_config()
        self.destroy()
