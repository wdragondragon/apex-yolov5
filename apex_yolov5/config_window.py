import os

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QAction, QApplication

from apex_yolov5.FrameRateMonitor import FrameRateMonitor
from apex_yolov5.DebugWindow import DebugWindow
from apex_yolov5.magnifying_glass import MagnifyingGlassWindows
from apex_yolov5.window_layout.ai_toggle_layout import AiToggleLayout
from apex_yolov5.window_layout.auto_charged_energy_layout import AutoChargedEnergyLayout
from apex_yolov5.window_layout.auto_gun_config_layout import AutoGunConfigLayout
from apex_yolov5.window_layout.auto_save_config_layout import AutoSaveConfigLayout
from apex_yolov5.window_layout.model_config_layout import ModelConfigLayout
from apex_yolov5.window_layout.mouse_config_layout import MouseConfigLayout
from apex_yolov5.window_layout.screenshot_area_layout import ScreenshotAreaLayout


class ConfigWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.main_window = DebugWindow()
        self.magnifying_glass_window = MagnifyingGlassWindows()
        self.open_frame_rate_monitor_window = FrameRateMonitor()
        self.config = config
        self.config_layout_main = QVBoxLayout()
        self.config_layout = QHBoxLayout()
        self.config_layout_1 = QVBoxLayout()
        self.config_layout_2 = QVBoxLayout()
        self.ai_toggle_layout = AiToggleLayout(self.config, self, self.config_layout_1)
        self.mouse_config_layout = MouseConfigLayout(self.config, self, self.config_layout_1)
        self.screenshot_layout = ScreenshotAreaLayout(self.config, self, self.config_layout_1)
        self.model_config_layout = ModelConfigLayout(self.config, self, self.config_layout_2)
        self.auto_gun_config_layout = AutoGunConfigLayout(self.config, self, self.config_layout_2)
        self.auto_save_config_layout = AutoSaveConfigLayout(self.config, self, self.config_layout_2)
        self.auto_charge_energy_layout = AutoChargedEnergyLayout(self.config, self, self.config_layout_2)

        self.initUI()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.installEventFilter(self)

    def create_menus(self):
        config_action = QAction("实时锁定人物展示", self)
        config_action.triggered.connect(self.open_config_window)

        magnifying_glass_action = QAction("magnifying_glass", self)
        magnifying_glass_action.triggered.connect(self.open_magnifying_glass_window)

        magnifying_glass_action = QAction("识别频率监控", self)
        magnifying_glass_action.triggered.connect(self.open_frame_rate_monitor)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("功能")
        file_menu.addAction(config_action)
        file_menu.addAction(magnifying_glass_action)

    def open_config_window(self):
        if self.main_window is None:
            self.main_window = DebugWindow()
        self.main_window.show()

    def open_magnifying_glass_window(self):
        if self.magnifying_glass_window is None:
            self.magnifying_glass_window = MagnifyingGlassWindows()
        self.magnifying_glass_window.show()

    def open_frame_rate_monitor(self):
        if self.open_frame_rate_monitor_window is None:
            self.open_frame_rate_monitor_window = FrameRateMonitor()
        self.open_frame_rate_monitor_window.show()

    def update_frame_rate_plot(self, frame_rate):
        if self.open_frame_rate_monitor_window is not None:
            self.open_frame_rate_monitor_window.update_frame_rate_plot(frame_rate)

    def initUI(self):
        self.setWindowTitle("Apex gun")
        self.setGeometry(0, 0, 250, 200)
        self.create_menus()
        self.ai_toggle_layout.add_layout()
        self.mouse_config_layout.add_layout()
        self.screenshot_layout.add_layout()
        self.model_config_layout.add_layout()
        self.auto_gun_config_layout.add_layout()
        self.auto_save_config_layout.add_layout()
        self.auto_charge_energy_layout.add_layout()

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

    def set_image(self, img_data, bboxes):
        self.main_window.set_image(img_data, bboxes)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.setWindowOpacity(0.1)  # Set window opacity to 90% when focus is lost
        elif event.type() == QEvent.WindowActivate:
            self.setWindowOpacity(1.0)  # Set window opacity to fully opaque when focus is regained
        return super().eventFilter(obj, event)

    def saveConfig(self):
        # 更新配置对象的属性
        self.mouse_config_layout.save_config()
        self.screenshot_layout.save_config()
        self.auto_charge_energy_layout.save_config()
        self.ai_toggle_layout.save_config()
        self.config.save_config()

    def closeEvent(self, event):
        QApplication.quit()
        os._exit(0)
