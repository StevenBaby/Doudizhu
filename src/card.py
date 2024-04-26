
import os
import sys
import random

import cairosvg

from PySide6 import QtCore, QtWidgets, QtGui
from doudizhu import Name2Real, Real2Env, Env2Real

from logger import logger

dirname = os.path.dirname(os.path.abspath(__file__))


class Card(QtWidgets.QLabel):

    clicked = QtCore.Signal(QtCore.QObject)

    def __init__(self, name, parent=None, back=False):
        super().__init__(parent=parent)
        assert (name in Name2Real)

        self.name = name
        self.real = Name2Real[name]
        self.env = Real2Env[self.real]
        self.back = back  # 显示背面
        self.selected = False  # 表示已选中

        filename = os.path.join(dirname, f"images/{name}.svg")
        with open(filename, 'rb') as file:
            data = cairosvg.svg2png(file_obj=file)
            image = QtGui.QImage()
            image.loadFromData(data)
            self.front_pixmap = QtGui.QPixmap.fromImage(image)
            self.setPixmap(self.front_pixmap)

        with open(os.path.join(dirname, f'images/2B.svg'), 'rb') as file:
            data = cairosvg.svg2png(file_obj=file)
            image = QtGui.QImage()
            image.loadFromData(data)
            self.back_pixmap = QtGui.QPixmap.fromImage(image)

        if back:
            self.setPixmap(self.back_pixmap)

        # 240 / 336
        width = 200
        height = int(width * 336 / 240)
        self.setGeometry(0, 0, width, height)
        self.setScaledContents(True)

    def setBack(self, back):
        self.back = back
        if self.back:
            self.setPixmap(self.back_pixmap)
        else:
            self.setPixmap(self.front_pixmap)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit(self)
        return False


class CardList(QtWidgets.QFrame):

    SELECT_OFFSET = 30
    LIST_OFFSET = 35

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.back = False
        self.all_cards = {}
        self.cards = []

        for idx, name in enumerate(sorted(
                Name2Real.keys(),
                key=lambda e: Real2Env[Name2Real[e]])):
            card = Card(name, self, False)
            card.clicked.connect(self.selectCard)
            card.setVisible(False)
            self.all_cards[name] = card

    def update(self):
        self.cards = sorted(self.cards, key=lambda e: Real2Env[Name2Real[e]])

        for card in self.all_cards.values():
            card.setVisible(False)

        for idx, name in enumerate(self.cards):
            card = self.all_cards[name]
            rect = card.geometry()
            card.setGeometry(
                self.LIST_OFFSET * idx,
                self.SELECT_OFFSET,
                rect.width(),
                rect.height())
            card.setVisible(True)
            card.raise_()

        super().update()

    def clear(self):
        self.cards = []
        for card in self.all_cards.values():
            card.selected = False
        self.update()

    def setBack(self, back: bool):
        self.back = back
        for card in self.all_cards.values():
            card.setBack(back)

    def selectCard(self, card: Card):
        card.selected = not card.selected
        rect = card.geometry()

        if card.selected:
            y = 0
        else:
            y = self.SELECT_OFFSET

        card.setGeometry(rect.x(), y, rect.width(), rect.height())

    def getSelectedCards(self):
        cards = []
        for card in self.all_cards.values():
            if card.selected:
                cards.append(card.env)
        return cards

    def getRealSelectedCards(self):
        cards = []
        for card in self.all_cards.values():
            if card.selected:
                cards.append(card.real)
        return cards


class TestWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("测试窗口")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.cardlist = CardList(self)
        self.horizontalLayout.addWidget(self.cardlist)

        cards = list(Name2Real.keys())
        random.shuffle(cards)
        self.cardlist.cards = cards[:20]
        self.cardlist.update()

        self.setGeometry(3200, 100, 1000, 600)

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     # self.cardlist.clear()
    #     # self.cardlist.setBack(not self.cardlist.back)
    #     logger.debug(self.cardlist.getRealSelectedCards())
    #     return super().mousePressEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = TestWidget()
    window.show()
    sys.exit(app.exec())
