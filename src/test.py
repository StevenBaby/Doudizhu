import os
import sys
import glob
import random

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from PySide6 import (
    QtGui, QtCore, QtWidgets, QtSvg, QtSvgWidgets, QtWebEngineWidgets
)

import cairosvg
from logger import logger

dirname = os.path.dirname(os.path.abspath(__file__))


NameToReal = {
    '1D': 'D', '1X': 'X',
    '2C': '2', '2D': '2', '2H': '2', '2S': '2',
    '3C': '3', '3D': '3', '3H': '3', '3S': '3',
    '4C': '4', '4D': '4', '4H': '4', '4S': '4',
    '5C': '5', '5D': '5', '5H': '5', '5S': '5',
    '6C': '6', '6D': '6', '6H': '6', '6S': '6',
    '7C': '7', '7D': '7', '7H': '7', '7S': '7',
    '8C': '8', '8D': '8', '8H': '8', '8S': '8',
    '9C': '9', '9D': '9', '9H': '9', '9S': '9',
    'TC': 'T', 'TD': 'T', 'TH': 'T', 'TS': 'T',
    'JC': 'J', 'JD': 'J', 'JH': 'J', 'JS': 'J',
    'QC': 'Q', 'QD': 'Q', 'QH': 'Q', 'QS': 'Q',
    'KC': 'K', 'KD': 'K', 'KH': 'K', 'KS': 'K',
    'AC': 'A', 'AD': 'A', 'AH': 'A', 'AS': 'A',
}

Env2Real = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
    8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q',
    13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}

Real2Env = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30
}


class Card(QtWidgets.QLabel):

    def __init__(self, filename, parent=None):
        super().__init__(parent=parent)
        self.filename = filename
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        self.name = name
        assert (name in NameToReal)
        self.real = NameToReal[name]
        self.env = Real2Env[self.real]

        with open(filename, 'rb') as file:
            data = cairosvg.svg2png(file_obj=file)
            image = QtGui.QImage()
            image.loadFromData(data)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.setPixmap(pixmap)
        self.setGeometry(0, 0, 240, 336)
        self.setScaledContents(True)

        self.base_geometry = self.geometry()
        self.actived = False  # 表示已选中

    def setActived(self, actived):
        rect = self.base_geometry
        if not self.actived:
            self.setGeometry(rect.x(), rect.y() - 20, rect.width(), rect.height())
        else:
            self.setGeometry(self.base_geometry)
        self.actived = actived

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setActived(not self.actived)
        return super().mousePressEvent(ev)


class CardsWidget(QWidget):
    def __init__(self, cards, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.cards = cards  # 存储卡片的列表
        self.selected_cards = []  # 存储选中的卡片
        self.hovered_card = None  # 当前悬停的卡片
        self.mouse_init_pos = None  # 鼠标按下的位置
        self.mouse_move_pos = None  # 鼠标当前的位置

    def mousePressEvent(self, event):
        self.mouse_init_pos = event.pos()
        self.mouse_drag_select()

    def mouseMoveEvent(self, event):
        self.mouse_move_pos = event.pos()
        self.mouse_drag_select()

    def mouseReleaseEvent(self, event):
        self.mouse_move_pos = event.pos()
        logger.debug(self.mouse_move_pos)
        # self.mouse_drag_select()

    def mouse_drag_select(self):
        if self.mouse_init_pos and self.mouse_move_pos:
            selected_cards = []
            selection_rect = QRect(self.mouse_init_pos, self.mouse_move_pos).normalized()
            for card in self.cards:
                if selection_rect.intersects(card['rect']):
                    card['selected'] = True
                    selected_cards.append(card)
                else:
                    card['selected'] = False
            self.selected_cards = selected_cards
            self.update()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: red;")
        self.cards = []

        for name in NameToReal:
            cardname = os.path.join(dirname, f'images/{name}.svg')
            card = Card(cardname, self)
            self.cards.append(card)

        random.shuffle(self.cards)

        lists = [
            self.cards[: 17],
            self.cards[17: 34],
            self.cards[34:],
        ]

        self.cardswidgets = [
            CardsWidget(cards, self)
            for cards in lists
        ]

        y = 20
        for cardswidget in self.cardswidgets:
            cardswidget.setGeometry(0, y, 1000, 400)
            cardswidget.setStyleSheet("background-color: red;")
            x = 20
            cardswidget.cards = sorted(cardswidget.cards, key=lambda e: e.env)

            for card in cardswidget.cards:
                card.raise_()
                rect = card.geometry()
                card.setGeometry(x, y, rect.width(), rect.height())
                card.base_geometry = card.geometry()
                x += 35
            y += 360

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        return super().mouseMoveEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
