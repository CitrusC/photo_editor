# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QPixmap
import Filter
import numpy as np
from PIL import Image
import PyQt5.QtGui as QtGui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(600, 500)
        self.setWindowTitle('filter_sample')
        # 画像を読み込んで、arrayにセット
        self.array = np.array(Image.open("sample.jpg").convert("RGBA"))
        # 画像を読み込んで、ラベルに貼り付け
        pixmap = QPixmap("sample.jpg")
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        # フィルタ適用用のボタンを作って、関数にリンク
        btn1 = QPushButton("Button 1", self)
        btn1.move(400, 50)
        btn1.clicked.connect(self.button_clicked)

    def ndarray_to_qpixmap(self, image):
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4,
                              QtGui.QImage.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def update_image(self, array):
        self.lbl.setPixmap(self.ndarray_to_qpixmap(array))
        self.update()

    def button_clicked(self):
        # ネガフィルタを掛ける場合
        # オブジェクト生成
        nega = Filter.Nega()
        # フィルタを適用する
        nega.apply(self.array)
        # 画面更新
        self.update_image(self.array)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
