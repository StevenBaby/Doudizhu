import os
import sys
import random
import collections
import traceback
import threading
import time

import cv2
import numpy as np
import keyboard

from PySide6 import QtCore, QtWidgets, QtGui
import ui
import qq
import capture
from doudizhu import AllEnvCards, Env2Real
import doudizhu

from logger import logger


class MonitorWidget(QtWidgets.QWidget):

    image_signal = QtCore.Signal(object)
    start_signal = QtCore.Signal(object)
    update_signal = QtCore.Signal(object)
    area_signal = QtCore.Signal(None)

    def __init__(self, parent: QtWidgets.QWidget | None = None, delay=0.1, image_width=600) -> None:
        super().__init__(parent)

        self.ui = ui.monitor.Ui_Monitor()
        self.ui.setupUi(self)
        self.ui.image.setScaledContents(True)
        self.delay = delay

        self.area = None
        self.area_signal.connect(self.reset_area)

        keyboard.add_hotkey("ctrl + shift + alt + r", lambda: self.area_signal.emit())

        self.running = False
        self.frame_thread = None

        self.image_signal.connect(self.update_image)

        self.index = 0
        self.image_width = image_width
        self.started = False
        self.remain_cards = collections.Counter(AllEnvCards)
        self.counts = [0, 0, 0]
        self.confirm = 2

        # test only
        self.players = doudizhu.init_agent()
        self.game = None
        self.hinted = None

    def check_action(self, action):
        action = collections.Counter(action)
        for k, v in action.items():
            if self.remain_cards[k] < v:
                return False
        return True

    def reset_area(self):
        self.area = None

    def capture_image(self):
        img = capture.capture("欢乐斗地主")
        if img is None:
            return None

        img = np.asarray(img).copy()
        image, area = qq.find_available_area(img, self.area)
        if image is None:
            return None

        self.image_signal.emit(image)
        if not self.area:
            if qq.find_show_color_cards(image):
                logger.info("lock area %s", area)
                self.area = area
            return None

        return image

    def capture_frame(self):
        image = self.capture_image()
        if image is None:
            return

        if not self.started:
            logger.debug("capture for start image...")
            frame = None
            for _ in range(self.confirm):
                frame0 = qq.find_start_frame(image)
                if not frame0:
                    continue
                if frame0 == frame:
                    break
                frame = frame0
            if not frame:
                return

            landlord, three, own, own_count, down_count, up_count = frame
            self.index = landlord
            logger.debug('started %s, %s, %s', landlord, own, three)
            self.started = True
            self.remain_cards = collections.Counter(AllEnvCards)
            self.counts = [own_count, down_count, up_count]
            self.start_signal.emit((landlord, own, three))

            # test only
            self.game = doudizhu.DoudizhuOne(self.players, landlord, own, three)
            return

        find_functions = [
            qq.find_own_action,
            qq.find_down_action,
            qq.find_up_action,
        ]

        # test only
        if not self.hinted:
            action, confidence = self.game.hint()
            if action is not None:
                logger.info(f"hint {[Env2Real[var] for var in sorted(action)]} confidence {confidence:0.3f}")
                self.hinted = True

        env, pas = None, None
        confirm = self.confirm
        while confirm:
            env1, pas1 = find_functions[self.index](image)
            # logger.debug("find %s -> %s, %s -> %s, %s", env1, env, pas1, pas, confirm)
            if tuple(env1) == env and pas1 == pas:
                confirm -= 1

            env = tuple(env1)
            pas = pas1

            image = self.capture_image()
            time.sleep(0.1)
            if image is None:
                return

        if not self.check_action(env):
            return

        action = collections.Counter(env)
        for k, v in action.items():
            self.remain_cards[k] -= v

        self.counts[self.index] -= len(env)
        if self.counts[self.index] == 0:
            self.started = False
            logger.info("game finished index %s win...", self.index)

        if env or pas:
            env = sorted(env)
            logger.debug('update action %s %s', self.index, [Env2Real[var] for var in env])

            # test only
            self.hinted = False
            self.game.action(env)

            self.update_signal.emit((self.index, env))
            self.index = (self.index + 1) % 3

    def update_image(self, image: qq.InfoFrame):
        # logger.debug('update info')
        img = image
        h, w, c = img.shape

        w = self.image_width
        h = int(w / 1.777)
        # self.setMaximumSize(w, h)

        img = cv2.resize(img, (w, h)).copy()
        bytes_per_line = c * w
        qimg = QtGui.QImage(
            img.data, w, h,
            bytes_per_line, QtGui.QImage.Format.Format_RGB888,
        )

        pixmap = QtGui.QPixmap.fromImage(qimg)
        self.ui.image.setPixmap(pixmap)

    def run(self):
        while self.running:
            try:
                time.sleep(self.delay)
                self.capture_frame()
            except Exception as e:
                logger.error(traceback.format_exc())
        self.frame_thread = None

    def start(self):
        self.running = True
        self.frame_thread = threading.Thread(target=self.run, daemon=True)
        self.frame_thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MonitorWidget()
    window.start()
    window.show()
    sys.exit(app.exec())
