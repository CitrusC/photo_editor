# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import numpy as np
from PIL import Image


import os

# テキストフォーム中心の画面のためQMainWindowを継承する
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.array=np.array(Image.open("gazou3.jpg"))

        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # メニューバーのアイコン設定
        openFile = QAction(QIcon('imoyokan.jpg'), 'Save', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.save_image)

        # メニューバー作成
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


        # 第二引数はダイアログのタイトル、第三引数は表示するパス
    def save_image(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop",filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        print(fname)
        if fname[0]:
            pil_img = Image.fromarray(self.array)
            pil_img.save(fname[0])

        # fnameにパス名が入る


        # fname[0]は選択したファイルのパス（ファイル名を含む）
        # if fname[0]:
        #     # ファイル読み込み
        #     #f = open(fname[0], 'r')
        #
        #     # テキストエディタにファイル内容書き込み
        #     with f:
        #         data = f.read()
        #         self.textEdit.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
