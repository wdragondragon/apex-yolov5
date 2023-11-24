from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QLabel


class AutoSaveConfigLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        toggle_layout = QVBoxLayout()
        toggle_layout.setObjectName("toggle_layout")
        self.label = QLabel("自动保存设置")
        self.label.setAlignment(Qt.AlignCenter)
        toggle_layout.addWidget(self.label)
        self.is_show_debug_window_switch = QCheckBox("主页人物实时图像")
        self.is_show_debug_window_switch.setObjectName("is_show_debug_window")
        self.is_show_debug_window_switch.setChecked(self.config.is_show_debug_window)  # 初始化开关的值
        self.is_show_debug_window_switch.toggled.connect(self.main_window.handle_toggled)
        toggle_layout.addWidget(self.is_show_debug_window_switch)

        self.auto_save_switch = QCheckBox("自动保存标注文件")
        self.auto_save_switch.setObjectName("auto_save")
        self.auto_save_switch.setChecked(self.config.auto_save)  # 初始化开关的值
        self.auto_save_switch.toggled.connect(self.main_window.handle_toggled)
        toggle_layout.addWidget(self.auto_save_switch)

        self.only_save_switch = QCheckBox("仅保存标注文件（不开启自瞄）")
        self.only_save_switch.setObjectName("only_save")
        self.only_save_switch.setChecked(self.config.only_save)  # 初始化开关的值
        self.only_save_switch.toggled.connect(self.main_window.handle_toggled)
        toggle_layout.addWidget(self.only_save_switch)

        self.parent_layout.addLayout(toggle_layout)
