from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QSlider

from apex_yolov5.socket import yolov5_handler


class ModelConfigLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        model_config_layout = QVBoxLayout()
        model_config_layout.setObjectName("model_config_layout")
        self.label = QLabel("模型设置")
        self.label.setAlignment(Qt.AlignCenter)

        model_combo_box_layout = QHBoxLayout()
        label = QLabel("选择模型:")
        self.model_combo_box = QComboBox()

        for key in self.config.available_models.keys():
            self.model_combo_box.addItem(key)
        self.model_combo_box.setCurrentText(self.config.current_model)
        self.model_combo_box.currentIndexChanged.connect(self.selection_changed)

        model_combo_box_layout.addWidget(label)
        model_combo_box_layout.addWidget(self.model_combo_box)

        conf_thres_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.conf_thres_label = QLabel("置信度阈值:" + str(self.config.conf_thres), self.main_window)
        self.conf_thres_slider = QSlider(Qt.Horizontal, self.main_window)
        self.conf_thres_slider.setMinimum(1)  # 最小值
        self.conf_thres_slider.setMaximum(100)  # 最大值
        self.conf_thres_slider.setValue(int(self.config.conf_thres * 100))  # 初始化值
        self.conf_thres_slider.valueChanged.connect(self.update_slieder_value)
        conf_thres_layout.addWidget(self.conf_thres_label)
        conf_thres_layout.addWidget(self.conf_thres_slider)

        iou_thres_layout = QHBoxLayout()
        # 创建标签和滑动条
        self.iou_thres_label = QLabel("交并比阈值:" + str(self.config.iou_thres), self.main_window)
        self.iou_thres_slider = QSlider(Qt.Horizontal, self.main_window)
        self.iou_thres_slider.setMinimum(1)  # 最小值
        self.iou_thres_slider.setMaximum(100)  # 最大值
        self.iou_thres_slider.setValue(int(self.config.iou_thres * 100))  # 初始化值
        self.iou_thres_slider.valueChanged.connect(self.update_iou_thres_value)
        iou_thres_layout.addWidget(self.iou_thres_label)
        iou_thres_layout.addWidget(self.iou_thres_slider)

        model_config_layout.addWidget(self.label)
        model_config_layout.addLayout(model_combo_box_layout)
        model_config_layout.addLayout(conf_thres_layout)
        model_config_layout.addLayout(iou_thres_layout)

        self.parent_layout.addLayout(model_config_layout)

    def selection_changed(self, index):
        selected_key = self.model_combo_box.currentText()
        self.model_combo_box.setEnabled(False)
        self.config.set_config("current_model", selected_key)
        self.config.current_model = selected_key
        yolov5_handler.reload_model()
        self.model_combo_box.setEnabled(True)

    def update_slieder_value(self, value):
        self.conf_thres_label.setText("置信度阈值:" + str(value / 100))
        self.conf_thres_label.adjustSize()
        self.config.set_config("conf_thres", value / 100)

    def update_iou_thres_value(self, value):
        self.iou_thres_label.setText("交并比阈值:" + str(value / 100))
        self.iou_thres_label.adjustSize()
        self.config.set_config("iou_thres", value / 100)
