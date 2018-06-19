import numpy as np

array = np.array([[250, 250, 250], [250, 250, 250], [250, 250, 250], ], dtype=np.uint8)
array = np.array([[255, 255, 255], [250, 250, 250], [0, 0, 0], ], dtype=np.uint8)
print(array)
array = array.astype(np.float32)
array = 255-array
array = np.clip(array, 0, 255)
array = array.astype(np.uint8)
print(array)
print(array.flags.writable)