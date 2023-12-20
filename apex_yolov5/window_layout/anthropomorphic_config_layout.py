from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit


class AnthropomorphicConfigLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        self.label = QLabel("鼠标拟人化设置")
        self.label.setAlignment(Qt.AlignCenter)
        intention_deviation_layout = QVBoxLayout()
        intention_deviation_layout.setObjectName("intention_deviation_layout")
        self.intention_deviation_toggle = QCheckBox("是否启动漏枪（根据配置周期性停止瞄准）")
        self.intention_deviation_toggle.setObjectName("intention_deviation_toggle")

        intention_deviation_interval_layout = QHBoxLayout()
        self.intention_deviation_interval_label = QLabel("漏枪周期")
        self.intention_deviation_interval = QLineEdit(self.main_window)
        self.intention_deviation_interval.setValidator(QIntValidator())
        intention_deviation_interval_layout.addWidget(self.intention_deviation_interval_label)
        intention_deviation_interval_layout.addWidget(self.intention_deviation_interval)
        self.intention_deviation_duration_label = QLabel("持续次数")
        self.intention_deviation_duration = QLineEdit(self.main_window)
        self.intention_deviation_duration.setValidator(QIntValidator())
        intention_deviation_interval_layout.addWidget(self.intention_deviation_duration_label)
        intention_deviation_interval_layout.addWidget(self.intention_deviation_duration)

        self.intention_deviation_force = QCheckBox("强制漏枪（将停止瞄准改变为强制将移动到人物外）")
        self.intention_deviation_force.setObjectName("intention_deviation_force")
        intention_deviation_layout.addWidget(self.intention_deviation_toggle)
        intention_deviation_layout.addLayout(intention_deviation_interval_layout)
        intention_deviation_layout.addWidget(self.intention_deviation_force)

        random_aim_layout = QVBoxLayout()
        random_aim_layout.setObjectName("random_aim_layout")
        self.random_aim_toggle = QCheckBox("随机弹道（准星在人物一定范围内按频率更换瞄准点）")
        self.random_aim_toggle.setObjectName("random_aim_toggle")

        random_coefficient_layout = QHBoxLayout()
        self.random_coefficient_label = QLabel("随机范围（0到1的小数）")
        self.random_coefficient = QLineEdit(self.main_window)
        self.random_coefficient.setValidator(QDoubleValidator())

        self.random_change_frequency_label = QLabel("瞄准点更换周期")
        self.random_change_frequency = QLineEdit(self.main_window)
        self.random_change_frequency.setValidator(QDoubleValidator())
        random_coefficient_layout.addWidget(self.random_coefficient_label)
        random_coefficient_layout.addWidget(self.random_coefficient)
        random_coefficient_layout.addWidget(self.random_change_frequency_label)
        random_coefficient_layout.addWidget(self.random_change_frequency)

        random_aim_layout.addWidget(self.random_aim_toggle)
        random_aim_layout.addLayout(random_coefficient_layout)

        self.parent_layout.addWidget(self.label)
        self.parent_layout.addLayout(intention_deviation_layout)
        self.parent_layout.addLayout(random_aim_layout)

        self.init_form_config()

    def init_form_config(self):
        self.intention_deviation_toggle.setChecked(self.config.intention_deviation_toggle)
        self.intention_deviation_interval.setText(str(self.config.intention_deviation_interval))
        self.intention_deviation_duration.setText(str(self.config.intention_deviation_duration))
        self.intention_deviation_force.setChecked(self.config.intention_deviation_force)

        self.random_aim_toggle.setChecked(self.config.random_aim_toggle)
        self.random_coefficient.setText(str(self.config.random_coefficient))
        self.random_change_frequency.setText(str(self.config.random_change_frequency))

    def save_config(self):
        self.config.set_config("intention_deviation_toggle", self.intention_deviation_toggle.isChecked())
        self.config.set_config("intention_deviation_interval", int(self.intention_deviation_interval.text()))
        self.config.set_config("intention_deviation_duration", int(self.intention_deviation_duration.text()))
        self.config.set_config("intention_deviation_force", self.intention_deviation_force.isChecked())

        self.config.set_config("random_aim_toggle", self.random_aim_toggle.isChecked())
        self.config.set_config("random_coefficient", float(self.random_coefficient.text()))
        self.config.set_config("random_change_frequency", int(self.random_change_frequency.text()))
