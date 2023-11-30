import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction


class SystemTrayApp:
    def __init__(self, main_window, config):
        self.main_window = main_window
        self.config = config
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("系统托盘不可用")
            return

        icon = QIcon("images/ag.ico")
        if icon.isNull():
            print("无效的图标")
            return

        self.show_action = QAction("显示应用", self.main_window)
        self.hide_action = QAction("隐藏应用", self.main_window)
        self.exit_action = QAction("退出", self.main_window)

        self.init_ui()

    def init_ui(self):
        self.tray_menu = QMenu(self.main_window)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.exit_action)

        self.show_action.triggered.connect(self.show_app)
        self.hide_action.triggered.connect(self.hide_app)
        self.exit_action.triggered.connect(self.exit_app)

        self.tray_icon = QSystemTrayIcon(self.main_window)
        self.change_icon(self.config.ai_toggle)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def show_app(self):
        self.main_window.show()

    def hide_app(self):
        self.main_window.hide()

    def change_icon(self, open_status):
        # 在这里更改图标，例如，切换到另一个图标
        if open_status:
            self.tray_icon.setIcon(QIcon("images/ag.ico"))  # 切换到第二个图标
        else:
            self.tray_icon.setIcon(QIcon("images/close.ico"))  # 切换回第一个图标

    def exit_app(self):
        self.tray_icon.hide()
        os._exit(0)
