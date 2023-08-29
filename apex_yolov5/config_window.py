from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout

from apex_yolov5.window_layout.auto_charged_energy_layout import AutoChargedEnergyLayout
from apex_yolov5.window_layout.auto_gun_config_layout import AutoGunConfigLayout
from apex_yolov5.window_layout.auto_save_config_layout import AutoSaveConfigLayout
from apex_yolov5.window_layout.mouse_config_layout import MouseConfigLayout
from apex_yolov5.window_layout.screenshot_area_layout import ScreenshotAreaLayout


class ConfigWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.config_layout_main = QVBoxLayout()
        self.config_layout = QHBoxLayout()
        self.config_layout_1 = QVBoxLayout()
        self.config_layout_2 = QVBoxLayout()
        self.mouse_config_layout = MouseConfigLayout(self.config, self, self.config_layout_1)
        self.auto_gun_config_layout = AutoGunConfigLayout(self.config, self, self.config_layout_1)
        self.auto_save_config_layout = AutoSaveConfigLayout(self.config, self, self.config_layout_2)
        self.auto_charge_energy_layout = AutoChargedEnergyLayout(self.config, self, self.config_layout_2)
        self.screenshot_layout = ScreenshotAreaLayout(self.config, self, self.config_layout_2)
        self.initUI()
        # self.setWindowFlags(Qt.FramelessWindowHint)

    def initUI(self):
        self.setWindowTitle("Config Window")
        self.setGeometry(100, 100, 250, 200)
        self.mouse_config_layout.add_layout()
        self.auto_gun_config_layout.add_layout()
        self.auto_save_config_layout.add_layout()
        self.auto_charge_energy_layout.add_layout()
        self.screenshot_layout.add_layout()

        # 创建保存按钮
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.saveConfig)


        self.config_layout.addLayout(self.config_layout_1)
        self.config_layout.addLayout(self.config_layout_2)

        self.config_layout_main.addLayout(self.config_layout)
        self.config_layout_main.addWidget(self.save_button)
        container = QWidget()
        container.setLayout(self.config_layout_main)
        self.setCentralWidget(container)

    def handle_toggled(self, checked):
        self.config.set_config(self.sender().objectName(), checked)

    def saveConfig(self):
        # 更新配置对象的属性
        self.mouse_config_layout.save_config()
        self.screenshot_layout.save_config()
        self.auto_charge_energy_layout.save_config()
        self.config.save_config()
        self.destroy()
