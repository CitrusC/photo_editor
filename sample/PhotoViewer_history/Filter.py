from abc import ABCMeta, abstractmethod
import numpy as np
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt


class Filter(metaclass=ABCMeta):
    isApplied = False
    image_id = None
    isUpdate = False

    @abstractmethod
    def apply(self, array):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_layout(self, parent):
        pass


class Nega(Filter):
    def apply(self, array):
        array[:, :, 0] = 255 - array[:, :, 0]
        array[:, :, 1] = 255 - array[:, :, 1]
        array[:, :, 2] = 255 - array[:, :, 2]
        return array

    def get_name(self):
        return 'Nega filter'

    def get_layout(self, parent):
        label = QLabel(self.get_name())
        layout = QHBoxLayout()
        layout.addWidget(label)
        return layout


class Brightness(Filter):
    brightness = 0

    def set_parameter(self, brightness):
        self.isApplied = False
        self.isUpdate =True
        self.brightness = brightness

    def apply(self, array):
        array[:, :, 0] = array[:, :, 0] + self.brightness
        array[:, :, 1] = array[:, :, 1] + self.brightness
        array[:, :, 2] = array[:, :, 2] + self.brightness
        array = np.clip(array, 0, 255)
        return array

    def get_layout(self, parent):
        label = QLabel(self.get_name())
        self.slider = QSlider(Qt.Horizontal, parent)
        self.slider.setRange(-255, 255)
        self.slider.sliderReleased.connect(self.release_mouse)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.slider)
        return layout

    def release_mouse(self):
        self.set_parameter(self.slider.value())

    def get_name(self):
        return 'Brightness filter'


class DoNothing(Filter):
    def apply(self, array):
        pass

    def get_name(self):
        return 'DoNothing filter'
