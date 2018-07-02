# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QLCDNumber, QSlider
from PyQt5.QtGui import QPixmap
import Filter
import numpy as np
from PIL import Image
import PyQt5.QtGui as QtGui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.nega = Filter.Nega()
        self.br = Filter.Brightness()
        self.med = Filter.Median()
        self.med.set_parameter(9)
        self.show()

    def initUI(self):
        self.resize(600, 500)
        self.setWindowTitle('filter_sample')
        # 画像を読み込んで、arrayにセット
        self.array = np.array(Image.open("sample.jpg").convert("RGBA"), np.float32)
        print(self.array.dtype)
        # 画像を読み込んで、ラベルに貼り付け
        pixmap = QPixmap("sample.jpg")
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        # フィルタ適用用のボタンを作って、関数にリンク
        btn1 = QPushButton("Nega", self)
        btn1.move(400, 50)
        btn1.clicked.connect(self.button_clicked1)
        btn2 = QPushButton("Brightness", self)
        btn2.move(400, 100)
        btn2.clicked.connect(self.button_clicked2)
        btn3 = QPushButton("Median", self)
        btn3.move(400, 150)
        btn3.clicked.connect(self.button_clicked3)

        # 数字のウィジェットを作成
        lcd = QLCDNumber(self)
        lcd.resize(150, 100)
        lcd.move(400, 200)
        # スライダーウィジェット作成
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.resize(150, 30)
        self.sld.move(400, 300)

        # スライダーを変更すると、数字も切り替わる
        self.sld.valueChanged.connect(lcd.display)
        self.sld.sliderReleased.connect(self.release_mouse)

    def ndarray_to_qpixmap(self, image):
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4,
                              QtGui.QImage.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def update_image(self, array):
        self.lbl.setPixmap(self.ndarray_to_qpixmap(array))
        self.update()

    def button_clicked1(self):
        # フィルタを適用する
        self.array = self.nega.apply(self.array)
        # 画面更新
        self.update_image(self.array.astype(np.uint8))

    def button_clicked2(self):
        # フィルタを適用する
        self.array = self.br.apply(self.array)
        # 画面更新
        self.update_image(self.array.astype(np.uint8))

    def button_clicked3(self):
        # フィルタを適用する
        self.array = self.med.apply(self.array)
        # 画面更新
        self.update_image(self.array.astype(np.uint8))

    def release_mouse(self):
        self.br.set_parameter(self.sld.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
