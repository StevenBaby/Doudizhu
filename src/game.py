import os
import sys
import glob
import random
import time

from PySide6 import QtGui, QtCore, QtWidgets

import card
import ui
import monitor
from logger import logger
from doudizhu import *
from qq import InfoFrame


class GameWindow(QtWidgets.QMainWindow):

    FONT_STYLE = '''font:14pt DengXian;'''

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
        self.lists[3].card_count.setVisible(False)

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
            cardlist.card_count.setVisible(False)
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

        self.monitor = monitor.MonitorWidget(self)
        self.ui.image_layout.addWidget(self.monitor)
        self.monitor.start()
        self.monitor.start_signal.connect(self.start_frame)
        self.monitor.update_signal.connect(self.update_frame)

        self.players = init_agent()

        self.timer = QtCore.QTimer(self)
        # 连接 timeout 信号到自定义的槽函数
        self.timer.timeout.connect(self.show_step)

        # 设置定时器间隔（以毫秒为单位）
        self.sleep_duration = 3000  # 1 秒
        self.timer.setSingleShot(True)  # 设置为单次触发定时器

        self.game = None
        # self.start_game()

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
                name = self.frames[i].objectName()
                style = f'QFrame {{{self.FONT_STYLE}}} QFrame#{name}{{ border: 2px solid #00ff99;}}'
                self.frames[i].setStyleSheet(style)
                # self.frames[i].setEnabled(True)
                self.lists[i].setSelectable(True)
            else:
                # name = self.frames[i].objectName()
                self.frames[i].setStyleSheet(self.FONT_STYLE)
                # self.frames[i].setEnabled(False)
                self.lists[i].setSelectable(False)

    def start_frame(self, frame: InfoFrame):
        logger.info("start frame ...")
        self.game = DoudizhuOne(
            self.players,
            frame.landlord,
            frame.show_env,
            frame.three_env,
        )

        self.ui.statusbar.showMessage("")

        for i in range(3):
            self.lists[i].update(self.game.cards[i])
            self.lists[i].name.setText(self.game.index_zh_name(i))
            self.show_lists[i].clear()
            self.mark_lists[i].updateCard(self.game.marks[i])

        for i in (1, 2):
            self.lists[i].setBack(True)

        self.three_list.update(self.game.three_cards)
        self.all_mark.updateCard(self.game.remain_cards)
        self.switch_list()

    def update_frame(self, frame: tuple[int, list, InfoFrame]):
        index, action, info = frame
        logger.info("update frame %s, %s", index, action)

        self.show_lists[index].update(convertEnv2Name(action))
        self.lists[0].update(convertEnv2Name(info.show_env))

    def start_game(self):
        logger.debug("start game")

        self.game = Doudizhu(self.players)

        self.ui.statusbar.showMessage("")

        for i in range(3):
            self.lists[i].update(self.game.cards[i])
            self.lists[i].name.setText(self.game.index_zh_name(i))
            self.show_lists[i].clear()
            self.mark_lists[i].updateCard(self.game.marks[i])

        for i in (1, 2):
            self.lists[i].setBack(True)

        self.three_list.update(self.game.three_cards)
        self.all_mark.updateCard(self.game.remain_cards)
        self.switch_list()

        if self.game.index != 0:
            self.show_step()

    def show_step(self):
        self.hint()
        self.show_cards()

    def show_cards(self):
        cards = self.current_list.getSelectedCards()

        self.game.action(cards)

        self.current_show.cards = cards
        self.current_show.update()

        self.current_list.clear()
        self.current_list.cards = self.game.current_cards
        self.current_list.update()

        self.current_mark.cards = self.game.current_mark
        self.current_mark.updateCard()

        self.all_mark.cards = self.game.remain_cards
        self.all_mark.updateCard()

        self.game.next()
        self.switch_list()

        if self.game.env.game_over:
            if self.game.env.num_wins['landlord'] > 0:
                message = '地主胜利'
            elif self.game.env.num_wins['farmer'] > 0:
                message = '农民胜利'
            for i in (1, 2):
                self.lists[i].setBack(False)
            self.ui.statusbar.showMessage(f"{message}，游戏结束！！！")
            return

        if self.game.index in (1, 2):
            self.timer.start(self.sleep_duration)

    def hint(self):
        action, confidence = self.game.hint()
        if not action:
            string = '不出'
        else:
            string = ' '.join(sorted([Name2Real[var] for var in action]))

        self.current_list.setSelected(action)
        self.ui.statusbar.showMessage(f"{self.game.current_zh_name}出牌：{string}; 胜率：{confidence:0.3f}")


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
