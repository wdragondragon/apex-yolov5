import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FrameRateMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('帧率监控')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        import matplotlib
        # 指定中文字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用宋体或其他支持中文的字体

        matplotlib.rcParams['font.family'] = 'SimHei'  # 字体

        matplotlib.rcParams['font.size'] = 11  # 调整字体大小
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 创建Matplotlib图形和帧率数据
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.frame_rate_data = []

        # 创建一个定时器以定期更新折线图
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame_rate_plot)
        # self.timer.start(1000)  # 更新频率：每1秒更新一次

    def update_frame_rate_plot(self, frame_rate):
        # 模拟获取帧率值，这里使用随机数代替
        # frame_rate = random.uniform(50, 60)
        self.frame_rate_data.append(frame_rate)

        # 只保留最近的20个数据点，以保持图表的长度有限
        if len(self.frame_rate_data) > 200:
            self.frame_rate_data.pop(0)

        # 清除图表并绘制新数据
        self.ax.clear()
        self.ax.plot(self.frame_rate_data, marker='o', linestyle='-')
        self.ax.set_xlabel('过去时间（秒）')
        self.ax.set_ylabel('帧率')

        # 刷新图表
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import matplotlib

    # 指定中文字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用宋体或其他支持中文的字体

    matplotlib.rcParams['font.family'] = 'SimHei'  # 字体

    matplotlib.rcParams['font.size'] = 11  # 调整字体大小

    frame_rate_app = FrameRateMonitor()
    frame_rate_app.show()
    sys.exit(app.exec_())
