import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QCheckBox


class DisclaimerWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.check_box = QCheckBox('我已阅读并同意免责声明', self)

        self.setWindowTitle('免责声明')
        self.setGeometry(100, 100, 1000, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.set_disclaimer_text()

        self.show_disclaimer_message()

    def set_disclaimer_text(self):
        disclaimer = '''1. Apex Gun（下称“本软件”）完全出于个人兴趣爱好，由本人在业余时间开发，是一款安全、绿色、可靠的辅助性工具软件。
2. 辅助工具的定义：以辅助玩家为目的的，实现更加便捷方便的玩游戏，主要因为现在的游戏瞄准方式过于复杂，过于单调，使用玩家们都想需要这么一款辅助软件来帮助游戏。
3. 本软件属于辅助工具，严格遵守中华人民共和国《计算机软件保护条例》，该类工具不具有修改游戏内存数据，损坏游戏文件功能，只有这类辅助工具是合法的。
4. 一旦用户安装、使用本软件起，即表示愿意接受以下条约：
　4.1 您同意尽您最大的努力来防止和保护未经授权的发表和使用本程式及其文件内容，我们将保留所有无明确说明的权利。
　4.2 您应该对使用本软件的结果自行承担风险，若运行本软件后出现不良后果时，本人对其概不负责，亦不承担任何法律责任。
　4.3 您通过使用本软件进行游戏辅助获得的游戏积分（包括但不限于角色等级、游戏金钱、装备等），本人对其合法性概不负责，亦不承担任何法律责任。
　4.4 本软件所有功能之保证，已提供于软件内，没有任何其他额外保证。其他任何本软件未提供之功能、品质或损及您其他之权益均非本人之保证范围；若有价值、瑕疵等问题，均非本软件作者之责任。
　4.5 该软件只用于单机靶场用途，请用户知情。如发现超出本声明范围外的使用用途，将立即收回使用权限。若隐瞒造成后果，本人对其概不负责，亦不承担任何法律责任。
　4.6 本软件著作权为软件作者所有，软件、免责声明最终解释权归本软件作者所有。
5. 本软件仅供学习交流之用，不可私自传播。若无意伤害你的权益，请联系我们将立刻配合处理！
6. 为了强调，每次打开本软件时都会出现该声明
'''
        self.disclaimer_text = disclaimer

    def show_disclaimer_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle('免责声明')

        message_box.setText(self.disclaimer_text)
        message_box.setCheckBox(self.check_box)

        confirm_button = message_box.addButton('确认', QMessageBox.AcceptRole)
        confirm_button.clicked.connect(self.check_and_accept)

        message_box.exec_()

    def check_and_accept(self):
        if self.check_box.isChecked():
            self.close()
        else:
            QMessageBox.warning(self, '警告', '请先勾选同意免责声明', QMessageBox.Ok)
            self.show_disclaimer_message()
