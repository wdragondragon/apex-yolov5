import os
import threading
import time

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QAction, QApplication, QDialog, \
    QComboBox, QLineEdit, QFileDialog

import detect
from apex_yolov5 import check_run
from apex_yolov5.FrameRateMonitor import FrameRateMonitor
from apex_yolov5.SystemTrayApp import SystemTrayApp
from apex_yolov5.magnifying_glass import MagnifyingGlassWindows
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket import config
from apex_yolov5.window_layout.ai_toggle_layout import AiToggleLayout
from apex_yolov5.window_layout.anthropomorphic_config_layout import AnthropomorphicConfigLayout
from apex_yolov5.window_layout.auto_charged_energy_layout import AutoChargedEnergyLayout
from apex_yolov5.window_layout.auto_gun_config_layout import AutoGunConfigLayout
from apex_yolov5.window_layout.auto_save_config_layout import AutoSaveConfigLayout
from apex_yolov5.window_layout.model_config_layout import ModelConfigLayout
from apex_yolov5.window_layout.mouse_config_layout import MouseConfigLayout
from apex_yolov5.window_layout.screenshot_area_layout import ScreenshotAreaLayout
from apex_yolov5.windows.DebugWindow import DebugWindow
from apex_yolov5.windows.DisclaimerWindow import DisclaimerWindow


class ConfigWindow(QMainWindow):
    # 类变量用于保存单例实例
    _instance = None
    init_sign = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config, title=None):
        super().__init__()
        if not self.init_sign:
            self.config = config
            self.system_tray = SystemTrayApp(self, self.config)
            self.main_window = DebugWindow()
            self.magnifying_glass_window = MagnifyingGlassWindows()
            self.open_frame_rate_monitor_window = FrameRateMonitor(self.config)
            self.config_layout_main = QVBoxLayout()
            self.config_layout = QHBoxLayout()
            self.config_layout_1 = QVBoxLayout()
            self.config_layout_2 = QVBoxLayout()
            self.config_layout_3 = QVBoxLayout()
            self.ai_toggle_layout = AiToggleLayout(self.config, self, self.config_layout_1, self.system_tray)
            self.model_config_layout = ModelConfigLayout(self.config, self, self.config_layout_1)
            self.mouse_config_layout = MouseConfigLayout(self.config, self, self.config_layout_1)

            self.anthropomorphic_config_layout = AnthropomorphicConfigLayout(self.config, self, self.config_layout_2)
            self.screenshot_layout = ScreenshotAreaLayout(self.config, self, self.config_layout_2)

            self.auto_gun_config_layout = AutoGunConfigLayout(self.config, self, self.config_layout_3)
            self.auto_save_config_layout = AutoSaveConfigLayout(self.config, self, self.config_layout_3)
            self.auto_charge_energy_layout = AutoChargedEnergyLayout(self.config, self, self.config_layout_3)
            self.initUI()
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.init_sign = True
            if title is None:
                self.setWindowTitle("Apex Gun " + self.config.version)
            else:
                self.setWindowTitle(title)
            if check_run.expiration_time is None:
                self.setWindowTitle(self.windowTitle() + " 永久授权")
            else:
                self.setWindowTitle(
                    self.windowTitle() + " 授权过期时间：" + check_run.expiration_time)

    def create_menus(self):
        config_action = QAction("实时锁定人物展示", self)
        config_action.triggered.connect(self.open_config_window)

        magnifying_glass_action = QAction("magnifying_glass", self)
        magnifying_glass_action.triggered.connect(self.open_magnifying_glass_window)

        magnifying_glass_action = QAction("识别频率监控", self)
        magnifying_glass_action.triggered.connect(self.open_frame_rate_monitor)

        mouse_performance_action = QAction("测试鼠标性能", self)
        mouse_performance_action.triggered.connect(self.mouse_performance_test)

        detect_test = QAction("模拟标记", self)

        detect_test.triggered.connect(self.showFileDialog)

        read_ref_glass_action = QAction("读取配置", self)
        read_ref_glass_action.triggered.connect(self.open_read_ref_glass_window)

        writer_ref_glass_action = QAction("新建配置", self)
        writer_ref_glass_action.triggered.connect(self.open_new_ref_glass_window)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("其他功能")
        file_menu.addAction(config_action)
        file_menu.addAction(magnifying_glass_action)
        file_menu.addAction(detect_test)

        config_menu = menu_bar.addMenu("管理配置")
        config_menu.addAction(read_ref_glass_action)
        config_menu.addAction(writer_ref_glass_action)

        more_menu = menu_bar.addMenu("更多")
        disclaimer_action = QAction('免责声明', self)
        disclaimer_action.triggered.connect(self.open_disclaimer_window)
        more_menu.addAction(disclaimer_action)

    def mouse_performance_test(self):
        threading.Thread(target=self.mouse_performance_test_threading).start()

    def mouse_performance_test_threading(self):
        i = 0
        x = 1
        start = time.time()
        while int((time.time() - start) * 1000) < 1000:
            MoverFactory.mouse_mover().move_test(x, x)
            i += 1
            x = -x
        print(f"鼠标性能为{i}/s")

    def open_disclaimer_window(self):
        self.disclaimer_window = DisclaimerWindow(self)

    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, file_type = QFileDialog.getOpenFileName(self, "选取文件", "",
                                                           "All Files (*);;Python Files (*.py)", options=options)
        threading.Thread(target=self.detect_threading, args=(file_path,)).start()

    def detect_threading(self, file_path):
        current_model_info = self.config.available_models.get(self.config.current_model)
        print_path = os.path.expanduser('~') + "\\" + "apex_gun\\runs\\detect"
        start = time.time()
        detect.run(imgsz=(self.config.imgsz, self.config.imgszy),
                   conf_thres=self.config.conf_thres,
                   half=self.config.half,
                   iou_thres=self.config.iou_thres,
                   weights=current_model_info["weights"],
                   data=current_model_info["data"],
                   source=file_path,
                   project=print_path,
                   max_det=10,
                   hide_conf=True,
                   hide_labels=True,
                   subsz=(self.config.shot_width, self.config.shot_height))
        print(f"检测标记使用时间：{(int((time.time() - start) * 1000)) / 1000.0}s")
        os.system("explorer.exe %s" % print_path)

    def open_read_ref_glass_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("读取配置窗口")

        layout = QVBoxLayout(dialog)

        # 添加下拉框
        combo_box = QComboBox(dialog)

        combo_box.addItems(config.get_all_config_file_name())
        combo_box.setCurrentText(config.read_config_file_name())
        layout.addWidget(combo_box)

        # 添加确定按钮
        ok_button = QPushButton("确定", dialog)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        # 添加取消按钮
        cancel_button = QPushButton("取消", dialog)
        cancel_button.clicked.connect(dialog.reject)
        layout.addWidget(cancel_button)

        # 显示对话框
        result = dialog.exec_()
        if result == QDialog.Accepted:
            selected_option = combo_box.currentText()
            config.writer_config_file_name(content=selected_option)
            self.config.update()
            self.init_form_config()
            print(f"选中的选项是: {selected_option}")
        else:
            print("用户取消操作")

    def open_new_ref_glass_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("新建配置窗口")

        layout = QVBoxLayout(dialog)

        new_config_name = QLineEdit(dialog)
        layout.addWidget(new_config_name)

        # 添加确定按钮
        ok_button = QPushButton("确定", dialog)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        # 添加取消按钮
        cancel_button = QPushButton("取消", dialog)
        cancel_button.clicked.connect(dialog.reject)
        layout.addWidget(cancel_button)

        # 显示对话框
        result = dialog.exec_()
        if result == QDialog.Accepted:
            selected_option = new_config_name.text()
            config.copy_config(selected_option)
            config.writer_config_file_name(content=selected_option)
            self.config.update()
            self.init_form_config()
            print(f"选中的选项是: {selected_option}")
        else:
            print("用户取消操作")

    def init_form_config(self):
        self.ai_toggle_layout.init_form_config()
        self.mouse_config_layout.init_form_config()
        self.screenshot_layout.init_form_config()
        self.model_config_layout.init_form_config()
        self.auto_gun_config_layout.init_form_config()
        self.auto_save_config_layout.init_form_config()
        self.auto_charge_energy_layout.init_form_config()
        self.anthropomorphic_config_layout.init_form_config()

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
            self.open_frame_rate_monitor_window = FrameRateMonitor(self.config)
        self.open_frame_rate_monitor_window.show()

    def add_frame_rate_plot(self, frame_rate):
        if self.open_frame_rate_monitor_window is not None:
            self.open_frame_rate_monitor_window.add_frame_rate_plot(frame_rate)

    def initUI(self):
        self.setGeometry(0, 0, 250, 200)
        self.create_menus()
        self.ai_toggle_layout.add_layout()
        self.model_config_layout.add_layout()
        self.mouse_config_layout.add_layout()
        self.anthropomorphic_config_layout.add_layout()
        self.screenshot_layout.add_layout()
        self.auto_gun_config_layout.add_layout()
        self.auto_save_config_layout.add_layout()
        self.auto_charge_energy_layout.add_layout()

        # 创建保存按钮
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.saveConfig)

        self.config_layout.addLayout(self.config_layout_1)
        self.config_layout.addLayout(self.config_layout_2)
        self.config_layout.addLayout(self.config_layout_3)

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
        self.anthropomorphic_config_layout.save_config()
        self.config.save_config()

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange and self.windowState() == Qt.WindowMinimized:
            # 如果窗口状态变为最小化，则同时隐藏主窗口并显示系统托盘图标
            self.system_tray.hide_app()
            # 在这里添加代码以显示系统托盘图标，可能是调用 SystemTrayApp 的相关方法

    def closeEvent(self, event):
        QApplication.quit()
        os._exit(0)
