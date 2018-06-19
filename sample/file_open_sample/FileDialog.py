#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)

import numpy as np
from PIL import Image

# テキストフォーム中心の画面のためQMainWindowを継承する
class MainWindow(QMainWindow):

    # ひな形
    def __init__(self):
        super().__init__()

        self.initUI()
    # ここまで

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # メニューバーのアイコン設定
        openFile = QAction(QIcon('imoyokan.jpg'), 'Open', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.fileOpen)

        # メニューバー作成
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def fileOpen(self):
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop", filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        # fnameにパス名が入る

        # fname[0]は選択したファイルのパス（ファイル名を含む）
        if fname[0]:
            self.array = np.array(Image.open(fname[0]).convert("RGBA"), np.float32)

            # ファイル読み込み

            # f = open(fname[0], 'r')
            #
            # # テキストエディタにファイル内容書き込み
            # with f:
            #     data = f.read()
            #     self.textEdit.setText(data)
                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
