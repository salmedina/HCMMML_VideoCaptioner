import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from time import time
from skimage import io
from skimage import color

n_colors = 1

inImage = io.imread("/Users/zal/Desktop/bounty.png")
inImage = np.array(inImage, dtype=np.float64) / 255
plt.imshow(inImage)

# Convert to floats instead of the default 8 bits integer coding. Dividing by
# 255 is important so that plt.imshow behaves works well on float data (need to
# be in the range [0-1]
hsvImage = color.convert_colorspace(inImage, 'RGB', 'HSV')

inImage = np.array(hsvImage, dtype=np.float64) / 255
plt.figure(1)
plt.imshow(inImage)