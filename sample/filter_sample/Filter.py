from abc import ABCMeta, abstractmethod
import numpy as np


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
