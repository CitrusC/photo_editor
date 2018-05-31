# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600,400)
        self.move(300, 300)
        self.setWindowTitle('Simple')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win=MainWindow()
    sys.exit(app.exec_())

// 以下追記
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win=MainWindow()
    sys.exit(app.exec_())


