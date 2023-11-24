from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QSlider, QLineEdit


class AutoChargedEnergyLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        auto_charged_energy_layout = QVBoxLayout()
        auto_charged_energy_layout.setObjectName("auto_charged_energy_layout")
        self.auto_charged_energy_label = QLabel("充能枪自动寸止设置", self.main_window)
        self.auto_charged_energy_label.setAlignment(Qt.AlignCenter)
        self.auto_charged_energy_switch = QCheckBox("充能枪自动寸止")
        self.auto_charged_energy_switch.setObjectName("auto_charged_energy")
        self.auto_charged_energy_switch.setChecked(self.config.auto_charged_energy)  # 初始化开关的值
        self.auto_charged_energy_switch.toggled.connect(self.main_window.handle_toggled)
        auto_charged_energy_layout.addWidget(self.auto_charged_energy_label)
        auto_charged_energy_layout.addWidget(self.auto_charged_energy_switch)

        storage_interval_layout = QHBoxLayout()
        self.storage_interval_label = QLabel("寸止间隔:" + str(self.config.storage_interval * 1000) + "毫秒",
                                             self.main_window)
        self.storage_interval_slider = QSlider(Qt.Horizontal, self.main_window)
        self.storage_interval_slider.setMinimum(1)
        self.storage_interval_slider.setMaximum(300)
        self.storage_interval_slider.setValue(int(self.config.storage_interval * 1000))  # 初始化值
        self.storage_interval_slider.valueChanged.connect(self.update_storage_interval_label)
        storage_interval_layout.addWidget(self.storage_interval_label)
        storage_interval_layout.addWidget(self.storage_interval_slider)
        auto_charged_energy_layout.addLayout(storage_interval_layout)

        auto_charged_energy_toggle_layout = QHBoxLayout()
        self.auto_charged_energy_toggle_label = QLabel("寸止开关:", self.main_window)
        self.auto_charged_energy_toggle = QLineEdit(self.main_window)
        self.auto_charged_energy_toggle.setText(str(self.config.auto_charged_energy_toggle))
        auto_charged_energy_toggle_layout.addWidget(self.auto_charged_energy_toggle_label)
        auto_charged_energy_toggle_layout.addWidget(self.auto_charged_energy_toggle)
        auto_charged_energy_layout.addLayout(auto_charged_energy_toggle_layout)

        self.parent_layout.addLayout(auto_charged_energy_layout)

    def update_storage_interval_label(self, value):
        self.storage_interval_label.setText("寸止间隔:" + str(int(value)) + "毫秒")
        self.storage_interval_label.adjustSize()

    def save_config(self):
        self.config.set_config("storage_interval",
                               self.storage_interval_slider.value() / 1000)
        self.config.set_config("auto_charged_energy",
                               self.auto_charged_energy_switch.isChecked())
        self.config.set_config("auto_charged_energy_toggle",
                               self.auto_charged_energy_toggle.text())
