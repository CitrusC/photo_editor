from abc import ABCMeta, abstractmethod
import numpy as np
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt


class Filter(metaclass=ABCMeta):
    def __init__(self):
        self.before_image_id = None
        self.after_image_id = None
        self.isUpdate = False
        self.parent = None
        self.layout = None

    def set_parent(self, parent):
        self.parent = parent

    @abstractmethod
    def apply(self, array):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def update_layout(self):
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

    def update_layout(self):
        self.label.setText(self.get_name())

    def get_layout(self):
        if self.layout is None:
            self.label = QLabel(self.get_name())
            layout = QHBoxLayout()
            layout.addWidget(self.label)
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

    def update_layout(self):
        self.label.setText(self.get_name())
        self.slider.setValue(self.brightness)

    def get_layout(self):
        self.label=None
        self.label = QLabel(self.get_name())
        self.slider=None
        self.slider = QSlider(Qt.Horizontal, self.parent)
        self.slider.setRange(-255, 255)
        self.slider.setValue(self.brightness)
        self.slider.sliderReleased.connect(self.release_mouse)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
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
