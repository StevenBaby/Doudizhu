import os
import sys
import collections

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


def imshow(img: np.ndarray, figsize=(12, 2)):
    if img is None:
        return
    if figsize:
        fig = plt.figure(figsize=figsize)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    plt.close()


def img_list_show(imgs: list[np.ndarray], ):
    if not imgs:
        return
    fig = plt.figure(figsize=(len(imgs), 2))
    axes = fig.subplots(1, ncols=len(imgs))

    for idx, img in enumerate(imgs):
        if len(imgs) > 1:
            axes[idx].imshow(img)
            axes[idx].axis("off")
            axes[idx].text(5, 5, idx)
        else:
            axes.imshow(img)
            axes.axis("off")
            axes.text(5, 5, idx)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imwrite(f"qq/images/{idx}.png", img)
    plt.show()
