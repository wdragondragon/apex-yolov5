import sys
import time
import traceback

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

from apex_yolov5.Tools import Tools
from apex_yolov5.log import LogFactory


class FrameRateMonitor(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

    def initUI(self):
        self.setWindowTitle('帧率监控')
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        import matplotlib
        # 指定中文字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用宋体或其他支持中文的字体

        matplotlib.rcParams['font.family'] = 'SimHei'  # 字体

        matplotlib.rcParams['font.size'] = 11  # 调整字体大小

        layout = QVBoxLayout()

        # 创建Matplotlib图形和帧率数据
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_major_locator(MultipleLocator(1))
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_facecolor('#f0f0f0')  # 浅灰色背景颜色
        self.frame_rate_data = []
        self.frame_rate_data_2 = []

        layout.setContentsMargins(5, 5, 5, 5)  # 设置布局内容的边距
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.queue = Tools.GetBlockQueue(name='frame_rate_queue', maxsize=1000)
        self.frame_rate_monitor_thread = FrameRateMonitorThread(self.queue)
        self.frame_rate_monitor_thread.signal.connect(self.update_frame_rate_plot)
        self.frame_rate_monitor_thread.start()

    def add_frame_rate_plot(self, frame_rate):
        self.queue.put(frame_rate)

    def update_frame_rate_plot(self, frame_rate):
        reasoning, screenshot = frame_rate

        self.frame_rate_data.append(reasoning)
        if len(self.frame_rate_data) > 60:
            self.frame_rate_data.pop(0)

        self.frame_rate_data_2.append(screenshot)
        if len(self.frame_rate_data_2) > 60:
            self.frame_rate_data_2.pop(0)

        if self.config.frame_rate_monitor:
            # 清除图表并绘制新数据
            self.ax.clear()
            self.ax.plot(self.frame_rate_data, marker='o', linestyle='-', label='识别', markersize=3)
            self.ax.plot(self.frame_rate_data_2, marker='o', linestyle='-', label='截图', markersize=3)
            # self.ax.set_title('帧率监控')
            # self.ax.set_xlabel('经过时间（秒）', fontsize=12)
            # self.ax.set_ylabel('帧率', fontsize=12)

            self.ax.legend(loc='lower right')

            # 刷新图表
            self.canvas.draw()
        else:
            LogFactory.logger().print_log(f"截图频率：[{screenshot}]，推理频率：[{reasoning}]")


class FrameRateMonitorThread(QThread):
    """
        使用信号槽来多线程更新ui
    """
    signal = pyqtSignal(object)

    def __init__(self, queue: Tools.GetBlockQueue):
        super().__init__()
        self.queue = queue

    def run(self):
        """
            避免多线程影响ui，在一个线程中启动队列消费打印
        """
        while True:
            try:
                data = self.queue.get()
                self.signal.emit(data)
            except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(0.1)


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
