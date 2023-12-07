from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QMainWindow

from apex_yolov5.KeyAndMouseListener import KMCallBack
from apex_yolov5.socket.config import global_config


class CircleWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.desktop_width = self.config.desktop_width
        self.desktop_height = self.config.desktop_height
        self.center = QPoint(self.config.desktop_width // 2, self.config.desktop_height // 2)
        self.radius = self.config.mouse_moving_radius
        self.setGeometry(0, 0, self.desktop_width, self.desktop_height)
        self.setWindowTitle('')
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        KMCallBack.connect(
            KMCallBack("m", "right", self.update_circle, False))
        KMCallBack.connect(
            KMCallBack("m", "right", self.update_circle))

    def update_circle(self, pressed=False, toggle=False):
        if pressed:
            self.radius = self.config.aim_mouse_moving_radius
        else:
            self.radius = self.config.mouse_moving_radius
        self.update()

    def init_form_config(self):
        self.desktop_width = self.config.desktop_width
        self.desktop_height = self.config.desktop_height
        self.center = QPoint(self.config.desktop_width // 2, self.config.desktop_height // 2)
        self.radius = self.config.mouse_moving_radius
        self.setGeometry(0, 0, self.desktop_width, self.desktop_height)
        if self.config.show_circle:
            self.show()
        else:
            self.hide()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.drawEllipse(self.center, self.radius, self.radius)


circle_window = CircleWindow(global_config)

# def main():
#     app = QApplication(sys.argv)
#     widget = CircleWindow(QPoint(QApplication.desktop().width() // 2, QApplication.desktop().height() // 2), 50)
#     widget.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
