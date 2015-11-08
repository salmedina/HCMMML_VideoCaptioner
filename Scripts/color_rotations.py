import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage import data
from skimage import io


def colorize(image, hue):
    """Return image tinted by the given hue based on a grayscale image."""
    hsv = color.rgb2hsv(color.gray2rgb(image))
    hsv[:, :, 0] = hue
    hsv[:, :, 1] = 1  # Turn up the saturation; we want the color to pop!
    return color.hsv2rgb(hsv)

image = io.imread("/Users/zal/Desktop/bounty.png")

hue_rotations = np.linspace(0, 1, 6)  # 0--1 is equivalent to 0--180
colorful_images = [colorize(image, hue) for hue in hue_rotations]

fig, axes = plt.subplots(nrows=2, ncols=3)

for ax, array in zip(axes.flat, colorful_images):
    ax.imshow(array, vmin=0, vmax=1)
    ax.set_axis_off()

plt.show()