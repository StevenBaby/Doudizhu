import os
import collections
import numpy as np
import cv2
from doudizhu import Name2Real, Name2Color

dirname = os.path.dirname(os.path.abspath(__file__))

Area = collections.namedtuple('Area', ["x", "y", 'w', 'h'])

AREA_OWN = Area(x=50, y=660, w=1680, h=220)
AREA_DOWN = Area(x=1050, y=280, w=520, h=210)
AREA_UP = Area(x=300, y=280, w=520, h=210)
AREA_THREE = Area(x=870, y=60, w=160, h=80)


def get_patterns(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    h = img.shape[0]
    w = img.shape[1] // 54

    patterns = {}
    for i, name in enumerate(Name2Real.keys()):
        patterns[name] = img[0:h, i * w: (i + 1) * w]
    return patterns


def get_color_patterns(patterns, offset):
    results = {}
    for name, color in Name2Color.items():
        results[color] = patterns[name][0: offset, :]
    return results


def read_image(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


PATTERN_OWN = get_patterns(os.path.join(dirname, 'images/own.png'))
PATTERN_SIDE = get_patterns(os.path.join(dirname, 'images/side.png'))
PATTERN_THREE = {name: cv2.resize(img, (34, 68)) for name, img in PATTERN_OWN.items()}

PATTERN_OWN_COLOR = get_color_patterns(PATTERN_OWN, 85)
PATTERN_SIDE_COLOR = get_color_patterns(PATTERN_SIDE, 60)
PATTERN_THREE_COLOR = get_color_patterns(PATTERN_THREE, 42)
PATTERN_THREE_COLOR['1R'] = read_image(os.path.join(dirname, 'images/1R.png'))
PATTERN_THREE_COLOR['1B'] = read_image(os.path.join(dirname, 'images/1B.png'))


def find_cards(image: np.ndarray, area: Area, patterns: dict[str, np.ndarray], confidence=0.97):
    x, y, w, h = area
    img = image[y:y + h, x:x + w].copy()

    result = {}

    for name, pattern in patterns.items():
        match = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
        match[match >= confidence] = 1.0
        match[match < confidence] = 0.0
        if np.sum(match) > 0:
            result[name] = 1

    return result


def find_color_cards(
        image: np.ndarray, area: Area,
        patterns: dict[str, np.ndarray], confidence=0.95):

    x, y, w, h = area
    img = image[y:y + h, x:x + w].copy()

    result = {}

    for name, pattern in patterns.items():
        match = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
        match[match >= confidence] = 1.0
        match[match < confidence] = 0.0

        match = (match * 255).astype(np.uint8)

        cnts = cv2.findContours(match, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if len(cnts):
            result[name] = len(cnts)
        if name in ('1R', '1B') and name in result:
            result[name] = 1

    return result


def find_own_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_OWN, PATTERN_OWN_COLOR, confidence=0.97)


def find_down_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_DOWN, PATTERN_SIDE_COLOR)


def find_up_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_UP, PATTERN_SIDE_COLOR)


def find_three_color_cards(image: np.ndarray):
    count = 0
    confidence = 0.95
    kvp = {}
    while count < 3 and confidence > 0.80:
        result = find_color_cards(image, AREA_THREE, PATTERN_THREE_COLOR, confidence)
        confidence -= 0.01
        count = sum(result.values())
        for k, v in result.items():
            if (k, v) not in kvp:
                kvp[(k, v)] = confidence

    kvp = sorted(kvp.items(), key=lambda e: e[1], reverse=True)
    result = {}
    count = 0

    for (k, v), _ in kvp:
        result[k] = v
        count += v
        if count >= 3:
            break
    return result


def get_pattern_landlord():
    pattern = cv2.imread(os.path.join(dirname, 'images/landlord.png'))
    pattern = cv2.cvtColor(pattern, cv2.COLOR_RGB2BGR)
    return pattern


PATTERN_LANDLORD = get_pattern_landlord()

AREA_LANDLORD_OWN = Area(x=50, y=900, w=250, h=200)
AREA_LANDLORD_DOWN = Area(x=1620, y=260, w=250, h=200)
AREA_LANDLORD_UP = Area(x=50, y=260, w=250, h=200)
LANDLORD_AREA = {
    'own': AREA_LANDLORD_OWN,
    'down': AREA_LANDLORD_DOWN,
    'up': AREA_LANDLORD_UP,
}


def find_landlord(image: np.ndarray, confidence=0.96):
    pattern = PATTERN_LANDLORD

    for name, area in LANDLORD_AREA.items():
        x, y, w, h = area
        img = image[y:y + h, x:x + w].copy()

        match = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
        match[match >= confidence] = 1.0
        match[match < confidence] = 0.0
        if np.sum(match) > 0:
            return name
    return None
