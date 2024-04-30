
import os
import sys
import random

import cairosvg

from PySide6 import QtCore, QtWidgets, QtGui
from doudizhu import Name2Real, Real2Env, Env2Real, Suit

from logger import logger
import ui

dirname = os.path.dirname(os.path.abspath(__file__))


def read_svg_pixmap(filename):
    with open(filename) as file:
        data = cairosvg.svg2png(file_obj=file, scale=1)
        image = QtGui.QImage()
        image.loadFromData(data)
        return QtGui.QPixmap.fromImage(image)


def read_svg_image(filename):
    with open(filename) as file:
        data = cairosvg.svg2png(file_obj=file, scale=1)
        image = QtGui.QImage()
        image.loadFromData(data)
        return image


def svg_filename(name):
    return os.path.join(dirname, f"images/cards/{name}.svg")


def read_card_pixmap():
    result = {}
    result['0B'] = read_svg_image(svg_filename('0B'))
    for name in Name2Real:
        result[name] = read_svg_image(svg_filename(name))
    return result


CARD_PIXMAP = read_card_pixmap()


class Card(QtWidgets.QLabel):

    clicked = QtCore.Signal(object)

    def __init__(self, name, parent=None, back=False, width=100, height=155):
        super().__init__(parent=parent)
        assert (name in Name2Real)

        self.name = name
        self.real = Name2Real[name]
        self.env = Real2Env[self.real]
        self.back = back  # 显示背面
        self.selected = False  # 表示已选中

        self.front_pixmap = QtGui.QPixmap.fromImage(CARD_PIXMAP[name])
        self.back_pixmap = QtGui.QPixmap.fromImage(CARD_PIXMAP['0B'])
        if back:
            self.setPixmap(self.back_pixmap)
        else:
            self.setPixmap(self.front_pixmap)
        # 216 / 336

        # height = int(width * 336 / 216)
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


class CardList(QtWidgets.QWidget):

    SELECT_OFFSET = 20
    LIST_OFFSET = 25
    CARD_WIDTH = 100
    CARD_HEIGHT = int(CARD_WIDTH * 336 / 216)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        # self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.setFrameShadow(QtWidgets.QFrame.Sunken)

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

        self.setMaximumHeight(self.CARD_HEIGHT + self.SELECT_OFFSET)

        self.label = QtWidgets.QLabel(self)
        self.label.setText('0')

    def update(self, sort=True):
        if sort:
            self.cards = sorted(
                self.cards,
                key=lambda e: (Real2Env[Name2Real[e]], Suit[e[1]]),
                reverse=True)

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

        self.label.setText(str(len(self.cards)))
        self.label.raise_()

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
                cards.append(card.name)
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
        self.setMaximumWidth(31 * len(self.CARD_TYPES))
        self.setMaximumHeight(27 * 2)

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
            if name in self.cards:
                text = str(self.cards[name])
            else:
                text = '0'
            self.item(1, idx).setText(text)

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
