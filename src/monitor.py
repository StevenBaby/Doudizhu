import os
import sys
import random
import traceback
import threading
import time

import cv2
import numpy as np

from PySide6 import QtCore, QtWidgets, QtGui
import ui
import qq

from logger import logger


class MonitorWidget(QtWidgets.QWidget):

    frame_signal = QtCore.Signal(object)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = ui.monitor.Ui_Monitor()
        self.ui.setupUi(self)
        self.ui.image.setScaledContents(True)

        self.running = False
        self.frame_thread = None

        self.frame_signal.connect(self.update_frame)

    def capture_frame(self):
        logger.debug("capture frame")
        frame = qq.get_info_frame()
        if not frame:
            return

        self.frame_signal.emit(frame)

    def update_frame(self, frame: qq.InfoFrame):
        # logger.debug('update info')
        img = frame.image
        h, w, c = img.shape

        # h //= 2
        # w //= 2
        h = 240
        w = int(h * 1.777)
        self.setMaximumSize(w, h)

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
                time.sleep(0.2)
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
