from abc import ABCMeta, abstractmethod
import numpy as np
import numba
from PIL import Image
import cv2


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, array):
        pass

    @abstractmethod
    def get_name(self):
        pass


class Nega(Filter):
    def apply(self, array):
        array[:, :, 0] = 255 - array[:, :, 0]
        array[:, :, 1] = 255 - array[:, :, 1]
        array[:, :, 2] = 255 - array[:, :, 2]
        return array

    def get_name(self):
        return 'Nega filter'


class Brightness(Filter):
    brightness = 0

    def set_parameter(self, brightness):
        self.brightness = brightness

    def apply(self, array):
        array[:, :, 0] = array[:, :, 0] + self.brightness
        array[:, :, 1] = array[:, :, 1] + self.brightness
        array[:, :, 2] = array[:, :, 2] + self.brightness
        array = np.clip(array, 0, 255)
        return array

    def get_name(self):
        return 'Brightness filter'


class DoNothing(Filter):
    def apply(self, array):
        pass

    def get_name(self):
        return 'DoNothing filter'


class Median(Filter):
    size = 3  # 奇数のみ有効

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

    def get_name(self):
        return 'Median filter'


class DoFFT(Filter):
    a = 0.1
    type = 0

    def set_parameter(self, a,type):
        self.a = a
        self.type = type

    def apply(self, array):
        # 高速フーリエ変換(2次元)
        #print("Eneter");
        ##img = cv2.imread("sample.jpg")
        gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
        #print(gray)
        src = np.fft.fft2(gray)

        # 画像サイズ
        h, w = src.shape

        # 画像の中心座標
        cy, cx = int(h / 2), int(w / 2)

        # フィルタのサイズ(矩形の高さと幅)
        rh, rw = int(self.a * cy), int(self.a * cx)

        # 第1象限と第3象限、第1象限と第4象限を入れ替え
        fsrc = np.fft.fftshift(src)

        fsrc_abs = np.absolute(fsrc)
        fsrc_abs[fsrc<1] = 1

        P = np.log10(fsrc)

        P_norm = P/np.amax(P)
        ##print(P_norm*255)
        y = np.uint8(np.around(P_norm.real*255))
        print(y)
        #パスフィルタ
        #if self.type == 0:  # LowPass
            # 入力画像と同じサイズで値0の配列を生成
            #fdst = np.zeros(src.shape, dtype=complex)

            # 中心部分の値だけ代入（中心部分以外は0のまま）
            #fdst[cy - rh:cy + rh, cx - rw:cx + rw] = fsrc[cy - rh:cy + rh, cx - rw:cx + rw]
        #else:  # HighPass
            # 入力画像と同じサイズで値0の配列を生成
            #fdst = fsrc

            # 中心部分の値だけ代入（中心部分以外は0のまま）
            #fdst[cy - rh:cy + rh, cx - rw:cx + rw] = 0

        # 第1象限と第3象限、第1象限と第4象限を入れ替え(元に戻す)
        #fdst = np.fft.fftshift(fdst)

        # 高速逆フーリエ変換
        #dst = np.fft.ifft2(fdst)

        # 実部の値のみを取り出し、符号なし整数型に変換して返す
        #himg = np.uint8(dst.real)
        #return himg.real
        ##パスフィルタ
        himg = Image.fromarray(y)
        return himg

    def get_name(self):
        return 'DoFFT filter'