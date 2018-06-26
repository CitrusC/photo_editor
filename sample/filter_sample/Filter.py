from abc import ABCMeta, abstractmethod
import numpy as np
import numba


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
