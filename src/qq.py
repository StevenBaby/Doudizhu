import os
import collections
import numpy as np
import cv2

from doudizhu import Name2Real, Name2Color, Real2Env, Color2Real
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
        return None, None

    cnt = contours[0]

    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y + h, x:x + w]
    crop = cv2.resize(crop, (1842, 1036))
    return crop, (x, y, w, h)


def read_image(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def get_patterns(filename):
    img = read_image(filename)
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


PATTERN_SHOW = get_patterns(os.path.join(dirname, 'images/qq/show.png'))
PATTERN_SIDE = get_patterns(os.path.join(dirname, 'images/qq/side.png'))
PATTERN_THREE = {name: cv2.resize(img, (34, 68)) for name, img in PATTERN_SHOW.items()}

PATTERN_SHOW_COLOR = get_color_patterns(PATTERN_SHOW, 85)
PATTERN_SIDE_COLOR = get_color_patterns(PATTERN_SIDE, 60)
PATTERN_THREE_COLOR = get_color_patterns(PATTERN_THREE, 42)
PATTERN_THREE_COLOR['1R'] = read_image(os.path.join(dirname, 'images/qq/1R.png'))
PATTERN_THREE_COLOR['1B'] = read_image(os.path.join(dirname, 'images/qq/1B.png'))


AREA_SHOW = Area(x=10, y=620, w=1800, h=220)
AREA_UP = Area(x=200, y=200, w=700, h=280)
AREA_DOWN = Area(x=900, y=200, w=700, h=280)
AREA_OWN = Area(x=550, y=350, w=700, h=300)
AREA_THREE = Area(x=800, y=0, w=220, h=150)


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


def find_show_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_SHOW, PATTERN_SHOW_COLOR, confidence=0.97)


def find_own_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_OWN, PATTERN_SIDE_COLOR)


def find_down_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_DOWN, PATTERN_SIDE_COLOR)


def find_up_color_cards(image: np.ndarray):
    return find_color_cards(image, AREA_UP, PATTERN_SIDE_COLOR)


def find_three_color_cards(image: np.ndarray):
    count = 0
    confidence = 0.95
    kvp = {}
    while count < 3 and confidence > 0.85:
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


PATTERN_PASS = read_image(os.path.join(dirname, 'images/qq/pass.png'))

AREA_OWN_PASS = Area(x=780, y=530, w=300, h=100)


def find_pass(
        image: np.ndarray, area: Area,
        pattern: dict[str, np.ndarray], confidence=0.8):

    x, y, w, h = area
    img = image[y:y + h, x:x + w].copy()

    match = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
    match[match >= confidence] = 1.0
    match[match < confidence] = 0.0

    match = (match * 255).astype(np.uint8)

    cnts = cv2.findContours(match, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if len(cnts):
        return True
    return False


def find_own_pass(image):
    return find_pass(image, AREA_OWN_PASS, PATTERN_PASS)


def find_down_pass(image):
    return find_pass(image, AREA_DOWN, PATTERN_PASS)


def find_up_pass(image):
    return find_pass(image, AREA_UP, PATTERN_PASS)


PATTERN_LANDLORD = read_image(os.path.join(dirname, 'images/qq/landlord.png'))

AREA_LANDLORD_OWN = Area(x=40, y=880, w=250, h=200)
AREA_LANDLORD_DOWN = Area(x=1550, y=220, w=250, h=200)
AREA_LANDLORD_UP = Area(x=40, y=220, w=250, h=200)

LANDLORD_AREA = {
    'own': AREA_LANDLORD_OWN,
    'down': AREA_LANDLORD_DOWN,
    'up': AREA_LANDLORD_UP,
}

OWN_INDEX = {
    'own': 0,
    'down': 2,
    'up': 1,
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
            return OWN_INDEX[name]
    return None


def get_pattern_counts():
    img = read_image(os.path.join(dirname, 'images/qq/counts.png'))

    h = img.shape[0]
    w = img.shape[1] // 21

    patterns = {}
    for i in range(21):
        patterns[i] = img[0:h, i * w: (i + 1) * w]
    return patterns


PATTERN_COUNTS = get_pattern_counts()

AREA_COUNTS_DOWN = Area(x=1550, y=400, w=150, h=150)
AREA_COUNTS_UP = Area(x=150, y=400, w=150, h=150)


def find_counts(
        image: np.ndarray, area: Area,
        patterns: dict[int, np.ndarray], confidence=0.89):

    x, y, w, h = area
    img = image[y:y + h, x:x + w]

    for name, pattern in patterns.items():
        match = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
        match[match >= confidence] = 1.0
        match[match < confidence] = 0.0

        match = (match * 255).astype(np.uint8)

        cnts = cv2.findContours(match, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if len(cnts):
            return name
    return 0


def find_down_counts(image: np.ndarray):
    return find_counts(image, AREA_COUNTS_DOWN, PATTERN_COUNTS)


def find_up_counts(image: np.ndarray):
    return find_counts(image, AREA_COUNTS_UP, PATTERN_COUNTS)


def convertColor2Env(data: dict[str, int]):
    if data is None:
        return None

    names = []
    for name, cnt in data.items():
        names += [name] * cnt
    # print(names)

    cards = [Real2Env[Color2Real[var]] for var in names]
    return cards


class InfoFrame(object):

    def __init__(self, image: np.ndarray, area: Area) -> None:
        self.image = image
        self.area = area
        self.landlord = find_landlord(image)

        self.three = find_three_color_cards(image)
        self.three_env = convertColor2Env(self.three)

        self.show = find_show_color_cards(image)
        self.show_env = convertColor2Env(self.show)

        self.own = find_own_color_cards(image)
        self.own_env = convertColor2Env(self.own)
        self.own_pass = find_own_pass(image)

        self.down = find_down_color_cards(image)
        self.down_env = convertColor2Env(self.down)
        self.down_pass = find_down_pass(image)
        if self.down_pass:
            self.down_env = []

        self.up = find_up_color_cards(image)
        self.up_env = convertColor2Env(self.up)
        self.up_pass = find_up_pass(image)
        if self.up_pass:
            self.up_env = []

        self.own_count = sum(self.show.values())
        self.down_count = find_down_counts(image)
        self.up_count = find_up_counts(image)
        self.count = sum([self.own_count, self.down_count, self.up_count])


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
