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

        self.layouts = [
            self.ui.own_layout,
            self.ui.down_layout,
            self.ui.up_layout,
            self.ui.three_layout,
        ]
        self.lists = [card.CardList(self) for _ in range(4)]
        self.lists[3].label.setVisible(False)

        for i in range(4):
            cardlist = self.lists[i]
            self.layouts[i].addWidget(cardlist)
            self.lists.append(cardlist)

        self.show_layouts = [
            self.ui.own_show_layout,
            self.ui.down_show_layout,
            self.ui.up_show_layout,
        ]
        self.show_lists = [card.CardList(self) for _ in range(3)]
        for i in range(3):
            cardlist = self.show_lists[i]
            cardlist.label.setVisible(False)
            cardlist.setSelectable(False)
            self.show_layouts[i].addWidget(cardlist)

        self.mark_layouts = [
            self.ui.own_mark_layout,
            self.ui.down_mark_layout,
            self.ui.up_mark_layout,
            self.ui.all_mark_layout,
        ]
        self.mark_lists = [card.CardMarker(self) for _ in range(4)]
        for i in range(4):
            marklist = self.mark_lists[i]
            self.mark_layouts[i].addWidget(marklist)

        self.frames = [
            self.ui.own_frame,
            self.ui.down_frame,
            self.ui.up_frame,
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

    @property
    def current_list(self):
        return self.lists[self.game.index]

    @property
    def current_mark(self):
        return self.mark_lists[self.game.index]

    @property
    def current_show(self):
        return self.show_lists[self.game.index]

    @property
    def three_list(self):
        return self.lists[3]

    @property
    def all_mark(self):
        return self.mark_lists[3]

    def switch_list(self):
        for i in range(3):
            if i == self.game.index:
                self.frames[i].setStyleSheet("background-color:#009999;")
                # self.frames[i].setEnabled(True)
                self.lists[i].setSelectable(True)
            else:
                self.frames[i].setStyleSheet("background-color: transparent;")
                # self.frames[i].setEnabled(False)
                self.lists[i].setSelectable(False)

    def start_game(self):
        logger.debug("start game")
        self.game = Doudizhu()

        for i in range(3):
            self.lists[i].cards = self.game.cards[i]
            self.lists[i].update()
            self.show_lists[i].clear()
            self.mark_lists[i].cards = self.game.marks[i]
            self.mark_lists[i].updateCard()

        self.three_list.cards = self.game.three_cards
        self.three_list.update(True)

        self.all_mark.cards = self.game.remain_cards()
        self.all_mark.updateCard()
        self.switch_list()
        # self.up_list.setBack(True)

    def show_cards(self):
        cards = self.current_list.getSelectedCards()

        self.game.action(cards)

        self.current_show.cards = cards
        self.current_show.update()

        self.current_list.clear()
        self.current_list.cards = self.game.cards[self.game.index]
        self.current_list.update()

        self.current_mark.cards = self.game.marks[self.game.index]
        self.current_mark.updateCard()

        self.all_mark.cards = self.game.remain_cards()
        self.all_mark.updateCard()
        self.game.next()
        self.switch_list()

    def hint(self):
        ...


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
