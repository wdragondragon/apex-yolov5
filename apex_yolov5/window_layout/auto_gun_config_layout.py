from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton


class AutoGunConfigLayout:
    def __init__(self, config, main_window, parent_layout):
        self.config = config
        self.main_window = main_window
        self.parent_layout = parent_layout

    def add_layout(self):
        add_refresh_button_title_layout = QVBoxLayout()
        add_refresh_button_layout = QHBoxLayout()
        add_refresh_button_input_layout = QVBoxLayout()
        self.refresh_button_title = QLabel("触发枪械识别按键列表", self.main_window)
        self.refresh_button_title.setAlignment(Qt.AlignCenter)
        self.fresh_button_list = QListWidget(self.main_window)
        self.refresh_button_input = QLineEdit()
        self.fresh_button_list.addItems(self.config.refresh_button)
        self.add_refresh_button = QPushButton("Add")
        self.add_refresh_button.clicked.connect(self.add_refresh_button_item)
        self.remove_refresh_button = QPushButton("Remove")
        self.remove_refresh_button.clicked.connect(self.delete_refresh_button_item)

        add_refresh_button_input_layout.addWidget(self.refresh_button_input)
        add_refresh_button_input_layout.addWidget(self.add_refresh_button)
        add_refresh_button_input_layout.addWidget(self.remove_refresh_button)
        add_refresh_button_layout.addWidget(self.fresh_button_list)
        add_refresh_button_layout.addLayout(add_refresh_button_input_layout)
        add_refresh_button_title_layout.addWidget(self.refresh_button_title)
        add_refresh_button_title_layout.addLayout(add_refresh_button_layout)

        list_layout = QHBoxLayout()
        list_layout_label = QLabel("自动开枪枪械识别列表", self.main_window)
        list_layout_label.setAlignment(Qt.AlignCenter)
        available_layout = QVBoxLayout()
        self.available_guns_label = QLabel("可用枪支", self.main_window)
        self.available_guns = [item for item in self.config.available_guns if item not in self.config.click_gun]
        self.available_guns_list = QListWidget(self.main_window)
        self.available_guns_list.addItems(self.available_guns)  # 假设config.available_guns是一个包含所有可用枪支的列表
        self.available_guns_list.setMinimumSize(100, 150)
        available_layout.addWidget(self.available_guns_label)
        available_layout.addWidget(self.available_guns_list)
        list_layout.addLayout(available_layout)

        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Add >>")
        self.add_button.clicked.connect(self.addGun)
        button_layout.addWidget(self.add_button)
        self.remove_button = QPushButton("<< Remove")
        self.remove_button.clicked.connect(self.removeGun)
        button_layout.addWidget(self.remove_button)
        list_layout.addLayout(button_layout)

        add_guns_layout = QVBoxLayout()
        self.add_guns_label = QLabel("已选择枪支", self.main_window)
        self.selected_guns_list = QListWidget(self.main_window)
        self.selected_guns_list.addItems(self.config.click_gun)  # 假设config.click_gun是一个包含已选择枪支的列表
        self.selected_guns_list.setMinimumSize(100, 150)
        add_guns_layout.addWidget(self.add_guns_label)
        add_guns_layout.addWidget(self.selected_guns_list)
        list_layout.addLayout(add_guns_layout)
        self.parent_layout.addLayout(add_refresh_button_title_layout)
        self.parent_layout.addWidget(list_layout_label)
        self.parent_layout.addLayout(list_layout)

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
