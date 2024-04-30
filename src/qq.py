import os
import collections
import numpy as np
import cv2

import capture

dirname = os.path.dirname(os.path.abspath(__file__))


Area = collections.namedtuple('Area', ["x", "y", 'w', 'h'])

MAIN_WINDOW_SIZE = (1843, 1036)


def find_available_area(image: np.ndarray, area: Area = None):
    if area:
        x, y, w, h = area
        crop = image[y:y + h, x:x + w]
        crop = cv2.resize(crop, (1843, 1036))
        return crop, area

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray[gray > 0xfe] = 0

    _, thresh = cv2.threshold(gray, 0xF, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    cnt = contours[0]

    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y + h, x:x + w]
    crop = cv2.resize(crop, (1842, 1036))
    return crop, (x, y, w, h)


class InfoFrame(object):

    def __init__(self, image: np.ndarray, area: Area) -> None:
        self.image = image
        self.area = area


def get_info_frame(area: Area = None):
    img = capture.capture("欢乐斗地主")
    if img is None:
        return None

    img = np.asarray(img).copy()
    image, area = find_available_area(img, area)
    if image is None:
        return None

    info = InfoFrame(image, area)
    return info
