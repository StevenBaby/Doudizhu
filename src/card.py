
import os
import sys
import random

import cairosvg

from PySide6 import QtCore, QtWidgets, QtGui
from doudizhu import Name2Real, Real2Env, Env2Real

from logger import logger
import ui

dirname = os.path.dirname(os.path.abspath(__file__))


def read_svg_pixmap(filename):
    with open(filename) as file:
        data = cairosvg.svg2png(file_obj=file, scale=1)
        image = QtGui.QImage()
        image.loadFromData(data)
        return QtGui.QPixmap.fromImage(image)


def svg_filename(name):
    return os.path.join(dirname, f"images/cards/{name}.svg")


class Card(QtWidgets.QLabel):

    clicked = QtCore.Signal(object)

    def __init__(self, name, parent=None, back=False, width=100):
        super().__init__(parent=parent)
        assert (name in Name2Real)

        self.name = name
        self.real = Name2Real[name]
        self.env = Real2Env[self.real]
        self.back = back  # 显示背面
        self.selected = False  # 表示已选中

        self.front_pixmap = read_svg_pixmap(svg_filename(name))
        self.back_pixmap = read_svg_pixmap(os.path.join(dirname, f"images/cards/0B.svg"))
        if back:
            self.setPixmap(self.back_pixmap)
        else:
            self.setPixmap(self.front_pixmap)
        # 216 / 336

        height = int(width * 336 / 216)
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

    SELECT_OFFSET = 20
    LIST_OFFSET = 25
    CARD_WIDTH = 100

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
            card = Card(name, self, False, width=self.CARD_WIDTH)
            card.clicked.connect(self.selectCard)
            card.setVisible(False)
            self.all_cards[name] = card

    def update(self):
        # self.cards = sorted(self.cards, key=lambda e: Real2Env[Name2Real[e]])

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


class CardMarker(QtWidgets.QTableWidget):

    SELECT_OFFSET = 20
    LIST_OFFSET = 25
    CARD_WIDTH = 100
    CARD_TYPES = {
        '1D': 'D', '1X': 'X', '2H': '2',
        'AH': 'A', 'KH': 'K', 'QH': 'Q', 'JH': 'J',
        'TH': 'T', '9H': '9', '8H': '8', '7H': '7',
        '6H': '6', '5H': '5', '4H': '4', '3H': '3',
    }

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        font = QtGui.QFont()
        font.setFamilies([u"DengXian"])
        font.setPointSize(14)
        self.setFont(font)

        self.setColumnCount(len(self.CARD_TYPES.keys()))
        self.setRowCount(2)
        self.setRowHeight(0, 10)
        self.setRowHeight(1, 10)
        self.verticalHeader().setDefaultSectionSize(45)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setMinimumWidth(31 * len(self.CARD_TYPES))
        self.setMinimumHeight(27 * 2)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.cards = {
            name: 0 for name in self.CARD_TYPES.values()
        }

        for idx, name in enumerate(self.CARD_TYPES.values()):
            self.setColumnWidth(idx, 5)

            if name == 'T':
                name = '10'

            item = QtWidgets.QTableWidgetItem(name)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(0, idx, item)

            item = QtWidgets.QTableWidgetItem(str(0))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(1, idx, item)

    def updateCard(self):
        for idx, name in enumerate(self.CARD_TYPES.values()):
            self.item(1, idx).setText(str(self.cards[name]))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        w = self.width() // len(self.CARD_TYPES)
        h = self.height() // 2
        for i in range(len(self.CARD_TYPES)):
            self.setColumnWidth(i, w)
        for i in range(2):
            self.setRowHeight(i, h)

        return super().resizeEvent(event)


class TestWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("测试窗口")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        # self.cardlist = CardList(self)
        self.cardmarker = CardMarker(self)
        self.horizontalLayout.addWidget(self.cardmarker)

        # cards = list(Env2Real.keys())
        # # print(cards)
        # # random.shuffle(cards)
        # self.cardlist.cards = cards
        # self.cardlist.update()

        self.setGeometry(3200, 100, 1000, 600)

        self.cardmarker.cards['D'] = 1
        self.cardmarker.updateCard()

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
