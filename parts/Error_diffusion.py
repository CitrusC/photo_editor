from abc import ABCMeta, abstractmethod
import numpy as np
from PIL import Image

class Filter(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, array):
        pass


class Error_diffusion(Filter):
    def __init__(self, ):
        super().__init__()

def apply(self, array):
    gray = np.array(Image.fromarray(array.astype(np.uint8)).convert('L'))

    for y in range(H)  :
        for x in range(W)  :
        #二値化
        if(array[y,x] > 127):
            array[y,x] = 255
            e = array[y,x] - 255
        else:
            array[y,x] = 0
            e = array[y,x] - 0

        if x < W-1:
            array[y, x + 1] += e * 5 / 16

        if y < H-1:
            array[y + 1, x - 1] += e * 3 / 16
            array[y + 1, x] += e * 5 / 16

        if x < W-1 and y <H - 1:
            array[y + 1, x + 1] += e * 3 / 16

    array_c = np.array(Image.fromarray(array).convert("RGBA"), np.float32)
    return array_c

            def get_name(self):
                return 'Error_diffusion filter'
