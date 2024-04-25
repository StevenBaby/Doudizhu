import os
import sys
import glob
import random

from PySide6 import (
    QtGui, QtCore, QtWidgets
)

import cairosvg
from logger import logger

import ui

dirname = os.path.dirname(os.path.abspath(__file__))

dirname = os.path.dirname(os.path.abspath(__file__))


Name2Real = {
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
        assert (name in Name2Real)
        self.real = Name2Real[name]
        self.env = Real2Env[self.real]

        with open(filename, 'rb') as file:
            data = cairosvg.svg2png(file_obj=file)
            image = QtGui.QImage()
            image.loadFromData(data)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.setPixmap(pixmap)
        self.setGeometry(0, 0, 160, 224)
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


class CardList(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        # self.raise_()
        # self.setStyleSheet("background-color: red;")
        self.setStyleSheet("background-color: transparent;")

        self.all_cards = {}
        for name in Name2Real:
            cardname = os.path.join(dirname, f'images/{name}.svg')
            card = Card(cardname, self)
            self.all_cards[name] = card
            card.setVisible(False)
            rect = card.geometry()
            card.setGeometry(rect.x(), 20, rect.width(), rect.height())

        self.cards = []

    def add_card(self, name):
        if name in self.cards:
            return
        assert (name in Name2Real)
        self.cards.append(name)
        self.update_cards()

    def remove_card(self, name):
        self.all_cards[name].actived = False
        self.cards.remove(name)
        self.update_cards()

    def update_cards(self):
        for card in self.all_cards.values():
            card.setVisible(False)

        self.cards = sorted(self.cards, key=lambda e: Real2Env[Name2Real[e]])

        x = 0
        for name in self.cards:
            card = self.all_cards[name]
            card.setVisible(True)
            card.raise_()
            rect = card.geometry()
            card.setGeometry(x, rect.y(), rect.width(), rect.height())
            card.base_geometry = card.geometry()
            x += 30

    def clearlist(self):
        self.cards = []
        for card in self.all_cards.values():
            card.setVisible(False)

    def get_actived_cards(self):
        cards = []
        for card in self.all_cards.values():
            if card.actived:
                cards.append(card.name)
        return cards


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = ui.mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("斗地主")
        # self.setStyleSheet("background-color: red;")

        self.ui.startButton.clicked.connect(self.start_game)
        self.ui.showButton.clicked.connect(self.show_cards)

        self.cardlists = [
            CardList(self.ui.card_frame),
            CardList(self.ui.card_frame),
            CardList(self.ui.card_frame),
            CardList(self.ui.card_frame),
        ]

        self.start_game()

    def start_game(self):
        logger.debug("start game")
        names = list(Name2Real.keys())
        random.shuffle(names)

        y = 0
        for idx, namelist in enumerate([
            names[:17],
            names[17: 34],
            names[34:],
            [],
        ]):
            self.cardlists[idx].clearlist()
            for name in namelist:
                self.cardlists[idx].add_card(name)
            rect = self.cardlists[idx].geometry()
            self.cardlists[idx].setGeometry(rect.x(), y, 1000, 300)
            y += 240

        self.activeindex = 2
        self.activelist = self.cardlists[2]
        self.activelist.setStyleSheet("background-color: green;")
        self.showlist = self.cardlists[3]

    def show_cards(self):
        logger.debug("show cards")

        cards = self.activelist.get_actived_cards()
        logger.debug(cards)
        if cards:
            self.showlist.clearlist()
        for name in cards:
            self.activelist.remove_card(name)
            self.showlist.add_card(name)

        self.activelist.setStyleSheet("background-color: transparent;")
        self.activeindex = (self.activeindex + 1) % 3
        self.activelist = self.cardlists[self.activeindex]
        self.activelist.setStyleSheet("background-color: green;")


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
