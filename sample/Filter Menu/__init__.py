#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class Button01(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self): #ウインドウの設定
        btn1 = QPushButton("Button01", self)
        btn1.clicked.connect(self.button01Clicked)

        self.statusBar()

        self.setWindowTitle('Filter Menu')
        self.show()

    def filterBar(self): # フィルタメニューの設計
        bar1 = QPushButton(nameOfFilter, self) #あとで指定した配列の個数を指定して対応
        bar1.clicked.connect(self.bar01Clicked)



    def button01Clicked(self): # ボタンが押されたときの挙動
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' Push Button01')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Button01()
    sys.exit(app.exec_())
