from abc import ABCMeta, abstractmethod
import numpy as np
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSlider, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PIL import Image
import numba


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
        # return 'Nega filter {} {}'.format(self.before_image_id, self.after_image_id)
        return 'Nega filter'

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
        # return 'Brightness filter{} {}'.format(self.before_image_id, self.after_image_id)
        return 'Brightness filter'


class DoNothing(Filter):
    def __init__(self):
        super().__init__()

    def apply(self, array):
        pass

    def get_name(self):
        return 'DoNothing filter'


class Median(Filter):
    def __init__(self):
        super().__init__()
        self.size = 1  # 奇数のみ有効

    def set_parameter(self, size):
        # self.size=self.slider.value()
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
        return 'Median filter'

    def clicked(self):
        self.set_parameter(int(self.sizeEdit.text()))

    def get_layout(self):
        try:
            label = QLabel(self.get_name())

            layout = QHBoxLayout()

            self.validator = QIntValidator(0, 100)
            self.sizeEdit = QLineEdit()
            self.sizeEdit.setValidator(self.validator)
            self.sizeEdit.setText(str(self.size))
            self.button = QPushButton(self.parent)
            self.button.setText("apply")
            self.button.clicked.connect(self.clicked)
            # self.slider = QSlider(Qt.Horizontal, self.parent)
            # self.slider.setValue(self.size)
            # self.slider.setRange(1, 99)
            # self.slider.setTickInterval(2)
            # self.slider.set
            # self.slider.setSingleStep(2)
            # self.slider.setPageStep(2)
            # self.slider.sliderReleased.connect(self.set_parameter)
            layout.addWidget(label)
            # layout.addWidget(self.slider)
            layout.addWidget(self.sizeEdit)
            layout.addWidget(self.button)

            # if self.sizeEdit.setModified(False):
            #     self.size = self.sizeEdit.int()

            # size = keydown.connect(self.sizeEdit.toPlainText())
            # mask = keydown.connect(self.maskEdit.toPlainText())

            # self.size = int(self.sizeEdit.text())
            # self.mask = int(self.maskEdit.text())

            return layout
        except:
            import traceback
            traceback.print_exc()


class Linear(Filter):
    def __init__(self, ):
        super().__init__()
        self.size = 1
        self.mask = [[1]]
        # 以下サンプル
        # self.size = 3
        # self.mask = np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]], np.float32)
        # self.mask/=9

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

    def get_name(self):
        return 'Linear filter'

    def get_layout(self):
        try:
            label = QLabel(self.get_name())

            size = QLabel('size')
            mask = QLabel('mask')

            self.validator1 = QIntValidator(0, 100)
            # self.validator2 = QDoubleValidator(0, 100)

            self.sizeEdit = QLineEdit()
            self.maskEdit = QLineEdit()

            self.sizeEdit.setValidator(self.validator1)


            # str = self.sizeEdit.toPlainText()
            str = self.sizeEdit.text()
            str.split()
            # val = int(str,10)
            # mask = np.array(self.str[self.size][self.size])
            for i in range (self.size):
                for j in range (self.size):
                    # mask[i][j] = val
                    mask[i][j] = str[i + j]
            # self.maskEdit.setValidator(self.validator2)

            # 格子状の配置を作り、各ウィジェットのスペースを空ける
            grid = QGridLayout()
            # ラベルの位置設定
            grid.addWidget(size, 1, 0)
            # 入力欄の位置設定
            grid.addWidget(self.sizeEdit, 1, 1)

            grid.addWidget(mask, 2, 0)
            grid.addWidget(self.maskEdit, 2, 1)

            layout = QHBoxLayout()
            # layout = QGridLayout()
            layout.addWidget(label)
            layout.addLayout(grid)

            if self.sizeEdit.setModified(False):
                size = self.sizeEdit.text()
                # for i in range size:
                #     maskEdit
                #     for j in range size:

            if self.sizeEdit.setModified(False):
                mask = self.maskEdit.text()
            #             # size = keydown.connect(self.sizeEdit.toPlainText())
            # mask = keydown.connect(self.maskEdit.toPlainText())

            # self.size = int(self.sizeEdit.text())
            # self.mask = int(self.maskEdit.text())

            return layout
        except:
            import traceback
            traceback.print_exc()


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

        P = np.log10(fsrc)

        P_norm = P / np.amax(P)

        y = np.uint8(np.around(P_norm.real * 255))

        himg = Image.fromarray(y)

        array_c = np.array(Image.fromarray(y).convert("RGBA"), np.float32)
        return array_c

    def get_name(self):
        return 'FFT2D filter'

    def get_layout(self):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout

class Thiza(Filter):
    def set_parameter(self, mask):
        # 4*4の正方行列、0から15の値で型はndarray
        self.mask=mask

    def apply(self,array):
        a = array[:,:,0] * 0.298912 + array[:,:,1] * 0.586611 + array[:,:,2] * 0.114478
        array[:, :, 0], array[:, :, 1], array[:, :, 2]=a, a, a
        H = array.shape[0]
        W = array.shape[1]
        for y in range(H):
            for x in range(W):
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
        return 'thiza filter'

    class Gray(Filter):
        def set_parameter(self, mask):
            # 4*4の正方行列、0から15の値で型はndarray
            self.mask = mask

        def apply(self, array):
            a = array[:, :, 0] * 0.298912 + array[:, :, 1] * 0.586611 + array[:, :, 2] * 0.114478
            array[:, :, 0], array[:, :, 1], array[:, :, 2] = a, a, a

            return array

        def get_name(self):
            return 'gray filter'

