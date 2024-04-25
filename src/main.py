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

import ui

dirname = os.path.dirname(os.path.abspath(__file__))

models = {
    'landlord': os.path.join(dirname, "baselines/douzero_WP/landlord.ckpt"),
    'landlord_up': os.path.join(dirname, "baselines/douzero_WP/landlord_up.ckpt"),
    'landlord_down': os.path.join(dirname, "baselines/douzero_WP/landlord_down.ckpt")
}

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

AllEnvCard = [i for i in range(3, 15) for _ in range(4)]
AllEnvCard.extend([17 for _ in range(4)])
AllEnvCard.extend([20, 30])

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


class DouDiZhuEnv(GameEnv):

    def hint(self):
        return self.players[self.acting_player_position].act(self.game_infoset)

    def step(self, action=None):
        if action is None:
            action = self.players[self.acting_player_position].act(
                self.game_infoset)

        if len(action) > 0:
            self.last_pid = self.acting_player_position

        if action in bombs:
            self.bomb_num += 1

        self.last_move_dict[
            self.acting_player_position] = action.copy()

        self.card_play_action_seq.append(action)
        self.update_acting_player_hand_cards(action)

        self.played_cards[self.acting_player_position] += action

        if self.acting_player_position == 'landlord' and \
                len(action) > 0 and \
                len(self.three_landlord_cards) > 0:
            for card in action:
                if len(self.three_landlord_cards) > 0:
                    if card in self.three_landlord_cards:
                        self.three_landlord_cards.remove(card)
                else:
                    break

        self.game_done()
        if not self.game_over:
            self.get_acting_player_position()
            self.game_infoset = self.get_infoset()

        return action


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
        self.players = sim.load_card_play_models(models)

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

        self.env = DouDiZhuEnv(self.players)
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
        action = self.env.hint()
        logger.debug("hint %s", action)
        actionname = ",".join([Env2Real[var] for var in action])
        if not action:
            actionname = '要不起'
        self.ui.statusbar.showMessage(f"提示{player_zh_names[self.activeindex]}出牌 {actionname}")

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

        self.ui.statusbar.showMessage(f"{player_zh_names[self.activeindex]}出牌 {actionname}")
        self.env.step(action)

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
