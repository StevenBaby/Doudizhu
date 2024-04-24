import os
import sys

from PySide6 import (
    QtGui, QtCore, QtWidgets, QtSvg, QtSvgWidgets, QtWebEngineWidgets
)

import cairosvg

dirname = os.path.dirname(os.path.abspath(__file__))


def load_svg(filename) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel()
    with open(filename, 'rb') as file:
        data = cairosvg.svg2png(file_obj=file)
        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QtGui.QPixmap.fromImage(image)
        label.setPixmap(pixmap)
    return label


def main():
    app = QtWidgets.QApplication(sys.argv)

    cardname = os.path.join(dirname, 'images/4H.svg')

    label = load_svg(cardname)
    label.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
