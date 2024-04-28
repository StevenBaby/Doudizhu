import os
import sys
import collections

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


def imshow(img: np.ndarray, figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    plt.close()
