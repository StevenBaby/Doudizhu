import os
import sys
import glob
import random
import time

import cairosvg
from PySide6 import QtGui, QtCore, QtWidgets

from douzero.env.game import GameEnv
from douzero.env.game import InfoSet
from douzero.env.game import bombs
from douzero.evaluation.deep_agent import DeepAgent
from douzero.evaluation import simulation as sim

from logger import logger
import doudizhu

from doudizhu import models, Name2Real, Real2Env, Env2Real

import ui

dirname = os.path.dirname(os.path.abspath(__file__))


player_names = [
    'landlord',
    'landlord_down',
    'landlord_up',
]

player_zh_names = [
    '地主',
    '下家',
    '上家',
]


class Card(QtWidgets.QLabel):

    def __init__(self, filename, name, parent=None, hide_card=False):
        super().__init__(parent=parent)
        self.filename = filename
        self.name = name
        assert (name in Name2Real)
        self.real = Name2Real[name]
        self.env = Real2Env[self.real]

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

        self.hide_card = hide_card
        if hide_card:
            self.setPixmap(self.back_pixmap)

        # 240 / 336
        width = 200
        height = int(width * 336 / 240)
        self.setGeometry(0, 0, width, height)
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

    def setHide(self, hide_card):
        self.hide_card = hide_card
        if self.hide_card:
            self.setPixmap(self.back_pixmap)
        else:
            self.setPixmap(self.front_pixmap)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setActived(not self.actived)
        return super().mousePressEvent(ev)


class CardList(QtWidgets.QWidget):

    PREPARE_OFFSET = 30
    CARD_OFFSET = 35

    def __init__(self, parent: QtWidgets.QWidget, hide_card=False) -> None:
        super().__init__(parent)
        # self.raise_()
        # self.setStyleSheet("background-color: red;")
        self.setStyleSheet("background-color: transparent;")

        self.hide_card = hide_card
        self.all_cards = {}
        for name in Name2Real:
            cardname = os.path.join(dirname, f'images/{name}.svg')
            card = Card(cardname, name, self, hide_card)
            self.all_cards[name] = card
            card.setVisible(False)
            rect = card.geometry()
            card.setGeometry(rect.x(), self.PREPARE_OFFSET, rect.width(), rect.height())

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
            card.setGeometry(x, self.PREPARE_OFFSET, rect.width(), rect.height())
            card.base_geometry = card.geometry()

            if card.actived:
                card.setGeometry(rect.x(), rect.y() - self.PREPARE_OFFSET, rect.width(), rect.height())
            x += self.CARD_OFFSET

    def clearlist(self):
        self.cards = []
        for card in self.all_cards.values():
            card.setVisible(False)
            card.actived = False
            rect = card.geometry()
            card.setGeometry(0, self.PREPARE_OFFSET, rect.width(), rect.height())

    def hidelist(self, hide_card):
        self.hide_card = hide_card
        for card in self.all_cards.values():
            if card.isVisible():
                card.setHide(hide_card)

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
        self.ui.hintButton.clicked.connect(self.hint)

        self.cardlists = [
            CardList(self.ui.card_frame, False),
            CardList(self.ui.card_frame, True),
            CardList(self.ui.card_frame, True),
        ]

        self.showlists = [
            CardList(self.ui.card_frame, False),
            CardList(self.ui.card_frame, False),
            CardList(self.ui.card_frame, False),
        ]

        logger.info("loading models....")

        self.players = {}
        for name in player_names:
            self.players[name] = doudizhu.DouDizhuAgent(name, models[name])

        self.timer = QtCore.QTimer(self)
        # 连接 timeout 信号到自定义的槽函数
        self.timer.timeout.connect(self.show_step)

        # 设置定时器间隔（以毫秒为单位）
        self.sleep_duration = 1000  # 1 秒
        self.timer.setSingleShot(True)  # 设置为单次触发定时器

        self.start_game()

    def start_game(self):
        logger.debug("start game")
        self.ui.startButton.setEnabled(True)
        self.ui.showButton.setEnabled(True)
        self.ui.hintButton.setEnabled(True)

        for i in [1, 2]:
            self.cardlists[i].hidelist(True)

        names = list(Name2Real.keys())
        random.shuffle(names)

        deck = [Real2Env[Name2Real[name]] for name in names]

        card_play_data = {'landlord': deck[:20],
                          'landlord_up': deck[20:37],
                          'landlord_down': deck[37:54],
                          'three_landlord_cards': deck[17:20],
                          }

        self.envs = {}
        for name in player_names:
            ...

        self.env = doudizhu.DouDiZhuEnv(self.players)
        self.env.card_play_init(card_play_data)

        y = 10
        for idx, namelist in enumerate([
            names[:20],
            names[37:],
            names[20: 37],
        ]):
            self.cardlists[idx].clearlist()
            self.showlists[idx].clearlist()

            for name in namelist:
                self.cardlists[idx].add_card(name)
            rect = self.cardlists[idx].geometry()
            self.cardlists[idx].setGeometry(50, y, 1000, 350)
            self.showlists[idx].setGeometry(900, y, 1000, 350)
            y += 320

        self.activeindex = 0
        self.activelist = self.cardlists[self.activeindex]
        self.activelist.setStyleSheet("background-color: green;")

    def hint(self):
        action, confidence = self.env.hint()
        logger.debug("hint %s", action)
        actionname = ",".join([Env2Real[var] for var in action])
        if not action:
            actionname = '要不起'
        self.ui.statusbar.showMessage(f"提示{player_zh_names[self.activeindex]}出牌 {actionname} 胜率 {confidence:0.2f}")

        for name in self.activelist.cards:
            card = self.activelist.all_cards[name]
            if card.env in action:
                card.actived = True
                action.remove(card.env)
        self.activelist.update_cards()

    def check_action(self, action):
        action = sorted(action)
        for a in self.env.info_sets[player_names[self.activeindex]].legal_actions:
            if tuple(a) == tuple(action):
                return True
        return False

    def show_step(self):
        self.hint()
        self.show_cards()

    def show_cards(self):
        logger.debug("show cards")

        cards = self.activelist.get_actived_cards()
        logger.debug(cards)
        action = [Real2Env[Name2Real[name]] for name in cards]
        logger.debug(action)

        if not self.check_action(action):
            self.ui.statusbar.showMessage("出牌不合法！！！")
            return
        actionname = ",".join([Env2Real[var] for var in action])
        if not action:
            actionname = '要不起'

        action, confidence = self.env.step(action)
        self.ui.statusbar.showMessage(f"{player_zh_names[self.activeindex]}出牌 {actionname} 胜率 {confidence:0.2f}")

        self.showlists[self.activeindex].clearlist()
        for name in cards:
            self.activelist.remove_card(name)
            self.showlists[self.activeindex].add_card(name)

        if self.env.game_over:
            if self.env.num_wins['landlord'] > 0:
                message = '地主胜利'
            elif self.env.num_wins['farmer'] > 0:
                message = '农民胜利'

            self.ui.statusbar.showMessage(f"{message}，游戏结束！！！")
            self.ui.startButton.setEnabled(True)
            self.ui.showButton.setEnabled(False)
            self.ui.hintButton.setEnabled(False)

            for list in self.cardlists:
                list.hidelist(False)
            return

        self.activelist.setStyleSheet("background-color: transparent;")
        self.activeindex = (self.activeindex + 1) % 3
        self.activelist = self.cardlists[self.activeindex]
        self.activelist.setStyleSheet("background-color: green;")

        if self.activeindex in (1, 2):
            # 启动定时器
            self.timer.start(self.sleep_duration)
            self.ui.startButton.setEnabled(False)
            self.ui.showButton.setEnabled(False)
            self.ui.hintButton.setEnabled(False)
        else:
            self.ui.startButton.setEnabled(True)
            self.ui.showButton.setEnabled(True)
            self.ui.hintButton.setEnabled(True)


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
