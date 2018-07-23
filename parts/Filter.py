"""
*** File Name           : Filter.py
*** Designer            : 稲垣 大輔
*** Date                : 2018.07.入力
*** Function            : 画像処理用のフィルタ処理を管理する。
"""

from abc import ABCMeta, abstractmethod
from fractions import Fraction

import numpy as np
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSlider, QGridLayout, QLineEdit, QPushButton, QTextEdit, QSpinBox, \
    QVBoxLayout, QTableWidget, QMessageBox
from PyQt5.QtCore import Qt
from PIL import Image
import numba


class Filter(metaclass=ABCMeta):
    def __init__(self):
        self.before_image_id = None
        self.after_image_id = None
        self.id = None
        self.isUpdate = False
        self.parent = None

    def set_id(self, id):
        self.id = id

    def set_parent(self, parent):
        self.parent = parent

    @abstractmethod
    def apply(self, array):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_layout(self):
        pass


class Nega(Filter):
    def __init__(self):
        super().__init__()

    def apply(self, array):
        array[:, :, 0] = 255 - array[:, :, 0]
        array[:, :, 1] = 255 - array[:, :, 1]
        array[:, :, 2] = 255 - array[:, :, 2]
        return array

    def get_name(self):
        # return 'Nega filter {} {}'.format(self.before_image_id, self.after_image_id)
        return 'Nega filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Brightness(Filter):
    def __init__(self):
        super().__init__()
        self.brightness = 0

    def set_parameter(self, brightness):
        self.brightness = brightness
        self.parent.parent_list.update_filter(self)

    def apply(self, array):
        array[:, :, 0] = array[:, :, 0] + self.brightness
        array[:, :, 1] = array[:, :, 1] + self.brightness
        array[:, :, 2] = array[:, :, 2] + self.brightness
        array = np.clip(array, 0, 255)
        return array

    def get_layout(self):
        label = QLabel(self.get_name())
        self.slider = QSlider(Qt.Horizontal, self.parent)
        self.slider.setRange(-255, 255)
        self.slider.setValue(self.brightness)
        self.slider.sliderReleased.connect(self.release_mouse)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.slider)
        return layout

    def release_mouse(self):
        self.set_parameter(self.slider.value())

    def get_name(self):
        # return 'Brightness filter{} {}'.format(self.before_image_id, self.after_image_id)
        return 'Brightness filter {}->{}'.format(self.before_image_id, self.after_image_id)


class Median(Filter):
    def __init__(self):
        super().__init__()
        self.size = 1  # 奇数のみ有効
        self.before_value = 1

    def set_parameter(self, size):
        if size % 2 == 0:
            self.size = max(1, size - 1)
            self.spinbox.setValue(self.size)
        else:
            self.size = size
        self.parent.parent_list.update_filter(self)

    @numba.jit
    def apply(self, array):
        height, width = array.shape[0], array.shape[1]
        d = int(self.size / 2)
        array_c = array.copy()
        if (d != 0):
            for y in range(d, height - d):
                for x in range(d, width - d):
                    array_c[y, x, 0] = np.median(array[y - d: y + d, x - d: x + d, 0])
                    array_c[y, x, 1] = np.median(array[y - d: y + d, x - d: x + d, 1])
                    array_c[y, x, 2] = np.median(array[y - d: y + d, x - d: x + d, 2])
        return array_c

    def get_name(self):
        return 'Median filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def clicked(self):
        self.set_parameter(self.spinbox.value())

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        self.spinbox = QSpinBox()
        self.spinbox.setValue(self.size)
        self.spinbox.setSingleStep(2)
        self.spinbox.setRange(1, 99)
        button = QPushButton(self.parent)
        button.setText("apply")
        button.clicked.connect(self.clicked)
        layout.addWidget(label)
        layout.addWidget(self.spinbox)
        layout.addWidget(button)
        return layout


class Linear(Filter):
    def __init__(self, ):
        super().__init__()
        self.size = 1
        self.mask = "1"

    def set_parameter(self, size, mask):
        if size % 2 == 0:
            self.size = max(1, size - 1)
            self.spinbox.setValue(self.size)
        else:
            self.size = size
        self.mask = mask
        self.parent.parent_list.update_filter(self)

    @numba.jit
    def apply(self, array):
        line = self.mask.strip().split('\n')
        mask = []
        for l in line:
            data = l.split(',')
            out2 = []
            for d in data:
                out2.append(float(Fraction(d)))
            mask.append(out2)

        height, width = array.shape[0], array.shape[1]
        if height != self.size or width != self.size:
            QMessageBox.critical(self.parent.parent_list.parent_, 'Error', "Mask size error.", QMessageBox.Ok)
            return array
        d = int(self.size / 2)
        array_c = np.zeros_like(array)
        array_c[:, :, 3] = array[:, :, 3]
        if self.size == 1:
            array_c = array * mask[0][0]
            array_c[:, :, 3] = array[:, :, 3]
            array_c = np.clip(array_c, 0, 255)
            return array_c

        for j in range(-d, d + 1):
            for i in range(-d, d + 1):
                array_c[d:height - d, d:width - d, 0] += array[d + j:height - d + j, d + i:width - d + i, 0] * \
                                                         mask[j][i]
                array_c[d:height - d, d:width - d, 1] += array[d + j:height - d + j, d + i:width - d + i, 1] * \
                                                         mask[j][i]
                array_c[d:height - d, d:width - d, 2] += array[d + j:height - d + j, d + i:width - d + i, 2] * \
                                                         mask[j][i]
        array_c = np.clip(array_c, 0, 255)

        return array_c

    def get_name(self):
        return 'Linear filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def clicked(self):
        self.set_parameter(self.spinbox.value(), self.maskEdit.toPlainText())

    def get_layout(self):
        label = QLabel(self.get_name())

        size = QLabel('size')
        mask = QLabel('mask')
        self.spinbox = QSpinBox()
        self.spinbox.setValue(self.size)
        self.spinbox.setSingleStep(2)
        self.spinbox.setRange(1, 99)
        self.maskEdit = QTextEdit()
        self.maskEdit.setPlainText(self.mask)
        self.maskEdit.setMaximumHeight(label.sizeHint().width())
        self.maskEdit.setMaximumWidth(label.sizeHint().width())

        # 格子状の配置を作り、各ウィジェットのスペースを空ける
        grid = QGridLayout()

        grid.addWidget(size, 0, 0)
        # 入力欄の位置設定
        grid.addWidget(self.spinbox, 0, 1)
        grid.setSpacing(5)
        grid.addWidget(mask, 1, 0)
        grid.addWidget(self.maskEdit, 1, 1)

        layout = QHBoxLayout()

        self.button = QPushButton(self.parent)
        grid.addWidget(self.button, 2, 1)
        self.button.setText("apply")
        self.button.clicked.connect(self.clicked)
        layout.addWidget(label)
        layout.addLayout(grid)
        layout.addWidget(self.button)
        return layout


class FFT2D(Filter):
    def __init__(self, ):
        super().__init__()
        self.a = 0.1
        self.type = 0

    def set_parameter(self, a, type):
        self.a = a
        self.type = type

    def apply(self, array):
        # 高速フーリエ変換(2次元)
        gray = np.array(Image.fromarray(array.astype(np.uint8)).convert('L'))
        src = np.fft.fft2(gray)

        # 第1象限と第3象限、第1象限と第4象限を入れ替え
        fsrc = np.fft.fftshift(src)

        fsrc_abs = np.absolute(fsrc)

        fsrc_abs[fsrc < 1] = 1

        p = np.log10(fsrc)

        p_norm = p / np.amax(p)

        y = np.uint8(np.around(p_norm.real * 255))

        himg = Image.fromarray(y)

        array_c = np.array(Image.fromarray(y).convert("RGBA"), np.float32)
        return array_c

    def get_name(self):
        return 'FFT2D filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Thiza(Filter):
    def __init__(self, ):
        super().__init__()
        self.mask = np.array([[0, 8, 2, 10],
                              [12, 4, 14, 6],
                              [3, 11, 1, 9],
                              [15, 7, 13, 5]])

    def apply(self, array):
        a = array[:, :, 0] * 0.298912 + array[:, :, 1] * 0.586611 + array[:, :, 2] * 0.114478
        array[:, :, 0], array[:, :, 1], array[:, :, 2] = a, a, a
        h = array.shape[0]
        w = array.shape[1]
        for y in range(h):
            for x in range(w):
                if (array[y, x, 0] * 16 / 255 >= self.mask[y % self.mask.shape[0], x % self.mask.shape[1]]):
                    array[y, x, 0] = 255
                    array[y, x, 1] = 255
                    array[y, x, 2] = 255
                else:
                    array[y, x, 0] = 0
                    array[y, x, 1] = 0
                    array[y, x, 2] = 0
        return array

    def get_name(self):
        return 'Thiza filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Grayscale(Filter):
    def __init__(self, ):
        super().__init__()

    def apply(self, array):
        a = array[:, :, 0] * 0.298912 + array[:, :, 1] * 0.586611 + array[:, :, 2] * 0.114478
        array[:, :, 0], array[:, :, 1], array[:, :, 2] = a, a, a
        return array

    def get_name(self):
        return 'Grayscale filter {}->{}'.format(self.before_image_id, self.after_image_id)

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Error_diffusion(Filter):
    def __init__(self, ):
        super().__init__()

    @numba.jit
    def apply(self, array):
        gray = np.array(Image.fromarray(array.astype(np.uint8)).convert('L'))
        H = gray.shape[0]
        W = gray.shape[1]
        for y in range(H):
            for x in range(W):
                # 二値化
                if (gray[y, x] > 127):
                    gray[y, x] = 255
                    e = gray[y, x] - 255
                else:
                    gray[y, x] = 0
                    e = gray[y, x] - 0

                if x < W - 1:
                    gray[y, x + 1] += e * 5 / 16

                if y < H - 1:
                    gray[y + 1, x - 1] += e * 3 / 16
                    gray[y + 1, x] += e * 5 / 16

                if x < W - 1 and y < H - 1:
                    gray[y + 1, x + 1] += e * 3 / 16

        array_c = np.array(Image.fromarray(gray).convert("RGBA"), np.float32)
        return array_c

    def get_name(self):
        return 'Error_diffusion filter'

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Contrast(Filter):
    def __init__(self):
        super().__init__()
        self.contrast = 100

    def set_parameter(self, contrast):
        self.contrast = contrast
        self.parent.parent_list.update_filter(self)

    def apply(self, array):
        array[:, :, 0] = (array[:, :, 0] - 128) * self.contrast / 100 + 128
        array[:, :, 1] = (array[:, :, 1] - 128) * self.contrast / 100 + 128
        array[:, :, 2] = (array[:, :, 2] - 128) * self.contrast / 100 + 128

        array = np.clip(array, 0, 255)
        return array

    def get_layout(self):
        label = QLabel(self.get_name())
        self.slider = QSlider(Qt.Horizontal, self.parent)
        self.slider.setRange(0, 200)
        self.slider.setValue(self.contrast)
        self.slider.sliderReleased.connect(self.release_mouse)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.slider)
        return layout

    def release_mouse(self):
        self.set_parameter(self.slider.value())

    def get_name(self):
        # return 'Contrast filter{} {}'.format(self.before_image_id, self.after_image_id)
        return 'Contrast filter'
