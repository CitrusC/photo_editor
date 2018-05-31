from abc import ABCMeta, abstractmethod
import numpy as np


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, array):
        pass


class Nega(Filter):
    def apply(self, array):
        array[:, :, 0] = 255 - array[:, :, 0]
        array[:, :, 1] = 255 - array[:, :, 1]
        array[:, :, 2] = 255 - array[:, :, 2]
