import sys
from PyQt5.QtWidgets import *

class ComboTest01(QWidget):
    def __init__(self, parent=None):
        super(ComboTest01, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.label = QLabel("東京",self)
        combo = QComboBox(self)
        combo.addItem("東京")
        combo.addItem("足立区")
        combo.addItem("台東区")
        combo.addItem("千代田区")
        combo.addItem("品川区")
        combo.addItem("隅田区")
        combo.move(50,50)
        self.label.move(50,150)
        combo.activated[str].connect(self.onActivated)
        self.setGeometry(300,300,300,200)
        self.setWindowTitle("QComboBox")

    def onActivated(self,text):
        self.label.setText(text)
        self.label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ComboTest01()
    win.show()
    sys.exit(app.exec_())