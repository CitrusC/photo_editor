from abc import ABCMeta, abstractmethod
import numpy as np
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSlider, \
    QGridLayout, QLineEdit, QTextEdit, QWidget, QApplication
from PyQt5.QtCore import Qt
from PIL import Image
import numba
import cv2


class Filter(metaclass=ABCMeta):
    def __init__(self):
        self.before_image_id = None
        self.after_image_id = None
        self.isUpdate = False
        self.parent = None

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
        return 'Nega filter {} {}'.format(self.before_image_id, self.after_image_id)

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
        self.isUpdate = True
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
        return 'Brightness filter{} {}'.format(self.before_image_id, self.after_image_id)


class DoNothing(Filter):
    def __init__(self):
        super().__init__()

    def apply(self, array):
        pass

    def get_name(self):
        return 'DoNothing filter'


class Median(Filter):
    size = 1 # 奇数のみ有効

    def set_parameter(self, size):
        self.size = size

    @numba.jit
    def apply(self, array):
        height, width = array.shape[0], array.shape[1]
        d = int(self.size / 2)
        array_c = array.copy()
        for y in range(d, height - d):
            for x in range(d, width - d):
                array_c[y, x, 0] = np.median(array[y - d: y + d, x - d: x + d, 0])
                array_c[y, x, 1] = np.median(array[y - d: y + d, x - d: x + d, 1])
                array_c[y, x, 2] = np.median(array[y - d: y + d, x - d: x + d, 2])
        return array_c

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout

    def get_name(self):
        return 'Median filter'


class Linear(Filter):
    def __init__(self, ):
        super().__init__()

    def set_parameter(self, size, mask):
        self.size = size
        self.mask = mask

    @numba.jit
    def apply(self, array):
        height, width = array.shape[0], array.shape[1]
        d = int(self.size / 2)
        array_c = np.zeros_like(array)
        array_c[:, :, 3] = array[:, :, 3]

        for j in range(-d, d + 1):
            for i in range(-d, d + 1):
                array_c[d:height - d, d:width - d, 0] += array[d + j:height - d + j, d + i:width - d + i, 0] * \
                                                         self.mask[j][i]
                array_c[d:height - d, d:width - d, 1] += array[d + j:height - d + j, d + i:width - d + i, 1] * \
                                                         self.mask[j][i]
                array_c[d:height - d, d:width - d, 2] += array[d + j:height - d + j, d + i:width - d + i, 2] * \
                                                         self.mask[j][i]
        array_c = np.clip(array_c, 0, 255)

        return array_c

    def get_layout(self):
        label = QLabel(self.get_name())

        self.size = QLabel('size')
        self.mask = QLabel('mask')

        self.sizeEdit = QLineEdit()
        self.maskEdit = QTextEdit()

        # 格子状の配置を作り、各ウィジェットのスペースを空ける
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # ラベルの位置設定
        self.grid.addWidget(self.size, 1, 0)
        # 入力欄の位置設定
        self.grid.addWidget(self.sizeEdit, 1, 1)

        self.grid.addWidget(self.mask, 2, 0)
        self.grid.addWidget(self.maskEdit, 2, 1)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.grid)
        return layout

    def get_name(self):
        return 'Linear filter'


class FFT2D(Filter):
    def __init__(self):
        super().__init__()

        self.aaa = 0.1
        self.type = 0

    def set_parameter(self, aaa,type):
        self.aaa = aaa
        self.type = type

    def apply(self, array):
        # 高速フーリエ変換(2次元)
        gray = np.array(Image.fromarray(array.astype(np.uint8)).convert('L'))
        src = np.fft.fft2(gray)

        # 第1象限と第3象限、第1象限と第4象限を入れ替え
        fsrc = np.fft.fftshift(src)

        fsrc_abs = np.absolute(fsrc)

        fsrc_abs[fsrc<1] = 1

        P = np.log10(fsrc)

        P_norm = P/np.amax(P)

        y = np.uint8(np.around(P_norm.real*255))

        himg = Image.fromarray(y)

        array_c = np.array(Image.fromarray(y).convert("RGBA"), np.float32)
        return array_c

    def get_name(self):
        return 'FFT2D filter'

    @property
    def get_layout(self):
        label = QLabel(self.get_name())

        self.aaa = QLabel('aaa')
        self.type = QLabel('type')

        self.aaaEdit = QLineEdit()
        self.typeEdit = QTextEdit()

        # 格子状の配置を作り、各ウィジェットのスペースを空ける
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # ラベルの位置設定
        self.grid.addWidget(self.aaa, 1, 0)
        # 入力欄の位置設定
        self.grid.addWidget(self.aaaEdit, 1, 1)

        self.grid.addWidget(self.type, 2, 0)
        self.grid.addWidget(self.typeEdit, 2, 1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.grid)
        return layout