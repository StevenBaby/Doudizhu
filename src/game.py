import os
import sys
import glob
import random
import time

from PySide6 import QtGui, QtCore, QtWidgets

import card
import ui
from logger import logger
from doudizhu import *


class GameWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        logger.debug("init ui....")
        self.ui = ui.game.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("斗地主")
        # self.setStyleSheet("background-color: red;")

        self.ui.startButton.clicked.connect(self.start_game)
        self.ui.showButton.clicked.connect(self.show_cards)
        self.ui.hintButton.clicked.connect(self.hint)

        self.own_list = card.CardList(self)
        self.ui.own_layout.addWidget(self.own_list)

        self.down_list = card.CardList(self)
        self.ui.down_layout.addWidget(self.down_list)

        self.up_list = card.CardList(self)
        self.ui.up_layout.addWidget(self.up_list)

        self.three_list = card.CardList(self)
        self.ui.three_layout.addWidget(self.three_list)
        self.three_list.label.setVisible(False)

        self.lists = [
            self.own_list,
            self.down_list,
            self.up_list,
        ]

        self.own_show_list = card.CardList(self)
        self.own_show_list.label.setVisible(False)
        self.ui.own_show_layout.addWidget(self.own_show_list)

        self.down_show_list = card.CardList(self)
        self.down_show_list.label.setVisible(False)
        self.ui.down_show_layout.addWidget(self.down_show_list)

        self.up_show_list = card.CardList(self)
        self.up_show_list.label.setVisible(False)
        self.ui.up_show_layout.addWidget(self.up_show_list)

        self.show_lists = [
            self.own_show_list,
            self.down_show_list,
            self.up_show_list,
        ]

        self.own_mark = card.CardMarker(self)
        self.ui.own_mark_layout.addWidget(self.own_mark)

        self.down_mark = card.CardMarker(self)
        self.ui.down_mark_layout.addWidget(self.down_mark)

        self.up_mark = card.CardMarker(self)
        self.ui.up_mark_layout.addWidget(self.up_mark)

        self.all_mark = card.CardMarker(self)
        self.ui.all_mark_layout.addWidget(self.all_mark)

        self.mark_lists = [
            self.own_mark,
            self.down_mark,
            self.up_mark
        ]

        # logger.info("loading models....")

        # self.players = {}
        # for name in player_names:
        #     self.players[name] = doudizhu.DouDizhuAgent(name, models[name])

        # self.timer = QtCore.QTimer(self)
        # # 连接 timeout 信号到自定义的槽函数
        # self.timer.timeout.connect(self.show_step)

        # # 设置定时器间隔（以毫秒为单位）
        # self.sleep_duration = 1000  # 1 秒
        # self.timer.setSingleShot(True)  # 设置为单次触发定时器

        self.start_game()

    def start_game(self):
        logger.debug("start game")
        self.game = Doudizhu()

        self.own_list.cards = self.game.own_cards
        self.own_list.update(True)

        self.down_list.cards = self.game.down_cards
        self.down_list.update(True)

        self.up_list.cards = self.game.up_cards
        self.up_list.update(True)

        self.three_list.cards = self.game.three_cards
        self.three_list.update(True)

        self.all_mark.cards = self.game.remain_cards()
        self.all_mark.updateCard()

        # self.up_list.setBack(True)

    def show_cards(self):
        l = self.lists[self.game.index]
        cards = l.getSelectedCards()

        self.game.action(cards)
        self.show_lists[self.game.index].cards = cards
        self.show_lists[self.game.index].update(True)

        l.clear()
        l.cards = self.game.cards[self.game.index]
        l.update(True)

        self.mark_lists[self.game.index].cards = self.game.marks[self.game.index]
        self.mark_lists[self.game.index].updateCard()

        self.all_mark.cards = self.game.remain_cards()
        self.all_mark.updateCard()
        self.game.next()

    def hint(self):
        ...


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
