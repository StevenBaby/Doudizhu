import os
import random

import numpy as np
import torch

from douzero.evaluation.deep_agent import DeepAgent
from douzero.env.env import get_obs
from douzero.env.game import GameEnv
from douzero.env.game import InfoSet
from douzero.env.game import bombs
from douzero.evaluation.deep_agent import DeepAgent
from douzero.evaluation import simulation as sim

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


models = {
    'landlord': os.path.join(dirname, "baselines/douzero_WP/landlord.ckpt"),
    'landlord_up': os.path.join(dirname, "baselines/douzero_WP/landlord_up.ckpt"),
    'landlord_down': os.path.join(dirname, "baselines/douzero_WP/landlord_down.ckpt")
}


class Doudizhu(object):

    def __init__(self) -> None:
        data = list(Name2Real.keys())
        random.shuffle(data)

        self.own_cards = data[:17]
        self.down_cards = data[17:34]
        self.up_cards = data[34:-3]
        self.three_cards = data[-3:]

        self.own_cards += self.three_cards
        self.index = 0

        self.cards = [
            self.own_cards,
            self.down_cards,
            self.up_cards,
        ]

        self.marks = [
            {},
            {},
            {},
        ]

    def action(self, cards: list[str]):
        for name in cards:
            self.cards[self.index].remove(name)
            self.marks[self.index].setdefault(Name2Real[name], 0)
            self.marks[self.index][Name2Real[name]] += 1

    def next(self):
        self.index = (self.index + 1) % 3

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
