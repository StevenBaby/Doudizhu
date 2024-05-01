import os
import random
import copy

import numpy as np
import torch

from douzero.evaluation.deep_agent import DeepAgent
from douzero.env.env import get_obs
from douzero.env.game import GameEnv
from douzero.env.game import InfoSet
from douzero.env.game import bombs
from douzero.evaluation import simulation as sim

from logger import logger

dirname = os.path.dirname(os.path.abspath(__file__))

Name2Real = {
    '1D': 'D', '1X': 'X',
    '2S': '2', '2H': '2', '2C': '2', '2D': '2',
    'AS': 'A', 'AH': 'A', 'AC': 'A', 'AD': 'A',
    'KS': 'K', 'KH': 'K', 'KC': 'K', 'KD': 'K',
    'QS': 'Q', 'QH': 'Q', 'QC': 'Q', 'QD': 'Q',
    'JS': 'J', 'JH': 'J', 'JC': 'J', 'JD': 'J',
    'TS': 'T', 'TH': 'T', 'TC': 'T', 'TD': 'T',
    '9S': '9', '9H': '9', '9C': '9', '9D': '9',
    '8S': '8', '8H': '8', '8C': '8', '8D': '8',
    '7S': '7', '7H': '7', '7C': '7', '7D': '7',
    '6S': '6', '6H': '6', '6C': '6', '6D': '6',
    '5S': '5', '5H': '5', '5C': '5', '5D': '5',
    '4S': '4', '4H': '4', '4C': '4', '4D': '4',
    '3S': '3', '3H': '3', '3C': '3', '3D': '3',
}

Real2Env = {
    'D': 30, 'X': 20, '2': 17,
    'A': 14, 'K': 13, 'Q': 12, 'J': 11,
    'T': 10, '9': 9, '8': 8, '7': 7,
    '6': 6, '5': 5, '4': 4, '3': 3
}

Env2Real = {
    30: 'D', 20: 'X', 17: '2', 14:
    'A', 13: 'K', 12: 'Q', 11: 'J',
    10: 'T', 9: '9', 8: '8', 7: '7',
    6: '6', 5: '5', 4: '4', 3: '3'}

Suit = {
    'D': 6,
    'X': 5,
    'S': 4,
    'H': 3,
    'C': 2,
    'D': 1,
}

AllEnvCards = [
    Real2Env[Name2Real[name]] for name in Name2Real
]

Name2Color = {
    '1D': '1R', '1X': '1B',
    '2S': '2B', '2H': '2R', '2C': '2B', '2D': '2R',
    'AS': 'AB', 'AH': 'AR', 'AC': 'AB', 'AD': 'AR',
    'KS': 'KB', 'KH': 'KR', 'KC': 'KB', 'KD': 'KR',
    'QS': 'QB', 'QH': 'QR', 'QC': 'QB', 'QD': 'QR',
    'JS': 'JB', 'JH': 'JR', 'JC': 'JB', 'JD': 'JR',
    'TS': 'TB', 'TH': 'TR', 'TC': 'TB', 'TD': 'TR',
    '9S': '9B', '9H': '9R', '9C': '9B', '9D': '9R',
    '8S': '8B', '8H': '8R', '8C': '8B', '8D': '8R',
    '7S': '7B', '7H': '7R', '7C': '7B', '7D': '7R',
    '6S': '6B', '6H': '6R', '6C': '6B', '6D': '6R',
    '5S': '5B', '5H': '5R', '5C': '5B', '5D': '5R',
    '4S': '4B', '4H': '4R', '4C': '4B', '4D': '4R',
    '3S': '3B', '3H': '3R', '3C': '3B', '3D': '3R'
}

Color2Real = {
    '1R': 'D', '1B': 'X', '2B': '2', '2R': '2',
    'AB': 'A', 'AR': 'A', 'KB': 'K', 'KR': 'K', 'QB': 'Q', 'QR': 'Q',
    'JB': 'J', 'JR': 'J', 'TB': 'T', 'TR': 'T', '9B': '9', '9R': '9',
    '8B': '8', '8R': '8', '7B': '7', '7R': '7', '6B': '6', '6R': '6',
    '5B': '5', '5R': '5', '4B': '4', '4R': '4', '3B': '3', '3R': '3'
}


LANDLORD = 'landlord'
LANDLORD_UP = 'landlord_up'
LANDLORD_DOWN = 'landlord_down'

models = {
    'landlord': os.path.join(dirname, "baselines/douzero_WP/landlord.ckpt"),
    'landlord_down': os.path.join(dirname, "baselines/douzero_WP/landlord_down.ckpt"),
    'landlord_up': os.path.join(dirname, "baselines/douzero_WP/landlord_up.ckpt"),
}

NAME_ZH = ['地主', '下家', "上家"]


class DoudizhuAgent(DeepAgent):

    def predict(self, infoset):
        # if len(infoset.legal_actions) == 1:
        #     return infoset.legal_actions[0]

        obs = get_obs(infoset)

        z_batch = torch.from_numpy(obs['z_batch']).float()
        x_batch = torch.from_numpy(obs['x_batch']).float()
        if torch.cuda.is_available():
            z_batch, x_batch = z_batch.cuda(), x_batch.cuda()
        y_pred = self.model.forward(z_batch, x_batch, return_value=True)['values']
        y_pred = y_pred.detach().cpu().numpy()
        return y_pred

    def act(self, infoset):
        y_pred = self.predict(infoset)

        best_action_index = np.argmax(y_pred, axis=0)[0]
        best_action = infoset.legal_actions[best_action_index]
        best_confidence = y_pred[best_action_index][0]
        best_confidence = max(best_confidence, -1.0)
        best_confidence = min(best_confidence, 1.0)

        return best_action, best_confidence


def init_agent():
    logger.info("init agent model...")
    players = {name: DoudizhuAgent(name, modelpath) for name, modelpath in models.items()}
    logger.info("init agent model finish...")
    return players


class DoudizhuEnv(GameEnv):

    def step(self, action=None):
        if action is None:
            action, confidence = self.players[self.acting_player_position].act(
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


class Doudizhu(object):

    def __init__(self, players) -> None:
        data = list(Name2Real.keys())
        random.shuffle(data)
        self.index = random.randint(0, 2)
        # self.index = 0
        self.landlord = self.index

        self.cards = [
            data[:17],
            data[17:34],
            data[34:-3],
            data[-3:]
        ]

        self.cards[self.landlord] += self.three_cards

        self.marks = [
            {},
            {},
            {},
        ]

        card_play_data = {
            'landlord': [Real2Env[Name2Real[name]] for name in self.cards[self.landlord]],
            'landlord_down': [Real2Env[Name2Real[name]] for name in self.cards[self.landlord - 2]],
            'landlord_up': [Real2Env[Name2Real[name]] for name in self.cards[self.landlord - 1]],
            'three_landlord_cards': [Real2Env[Name2Real[name]] for name in self.three_cards],
        }

        self.players = players
        self.env = DoudizhuEnv(players)
        self.env.card_play_init(card_play_data)

    def hint(self):
        infoset = self.env.info_sets[self.current_name]
        action, confidence = self.players[self.current_name].act(copy.deepcopy(infoset))
        logger.info("get action %s confidence %s", action, confidence)
        result = []

        for name in self.current_cards:
            env = Real2Env[Name2Real[name]]
            if env in action:
                result.append(name)
                action.remove(env)
        return result, confidence

    def check_action(self, action):
        action = sorted(action)
        for a in self.env.info_sets[self.current_name].legal_actions:
            if tuple(a) == tuple(action):
                return True
        return False

    def action(self, cards: list[str]):
        act = [Real2Env[Name2Real[name]] for name in cards]
        if not self.check_action(act):
            return False

        for name in cards:
            self.cards[self.index].remove(name)
            self.marks[self.index].setdefault(Name2Real[name], 0)
            self.marks[self.index][Name2Real[name]] += 1

        self.env.step(act)

    def next(self):
        self.index = (self.index + 1) % 3

    def index_zh_name(self, idx):
        return NAME_ZH[(idx - self.landlord) % 3]

    def index_name(self, idx):
        return list(models.keys())[(idx - self.landlord) % 3]

    @property
    def current_zh_name(self):
        return self.index_zh_name(self.index)

    @property
    def current_name(self):
        return self.index_name(self.index)

    @property
    def remain_cards(self):
        cards = {}
        for name in list(Name2Real.keys()):
            cards.setdefault(Name2Real[name], 0)
            cards[Name2Real[name]] += 1

        for i in range(3):
            mark = self.marks[i]
            for name, cnt in mark.items():
                cards[name] -= cnt

        return cards

    @property
    def three_cards(self):
        return self.cards[3]

    @property
    def current_cards(self):
        return self.cards[self.index]

    @property
    def current_mark(self):
        return self.marks[self.index]
