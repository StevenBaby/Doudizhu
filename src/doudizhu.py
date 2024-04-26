import os

import torch
import numpy as np

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

models = {
    'landlord': os.path.join(dirname, "baselines/douzero_WP/landlord.ckpt"),
    'landlord_up': os.path.join(dirname, "baselines/douzero_WP/landlord_up.ckpt"),
    'landlord_down': os.path.join(dirname, "baselines/douzero_WP/landlord_down.ckpt")
}


class DouDizhuAgent(DeepAgent):

    def predict(self, infoset):
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

    def confident(self, infoset, action):
        y_pred = self.predict(infoset)

        for idx, act in enumerate(infoset.legal_actions):
            if tuple(act) == tuple(action):
                break

        confidence = y_pred[idx][0]
        confidence = max(confidence, -1.0)
        confidence = min(confidence, 1.0)

        return confidence


class DouDiZhuEnv(GameEnv):

    def hint(self):
        return self.players[self.acting_player_position].act(self.game_infoset)

    def step(self, action=None):
        if action is None:
            action, confidence = self.players[self.acting_player_position].act(
                self.game_infoset)
        else:
            confidence = self.players[self.acting_player_position].confident(
                self.game_infoset, action)

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

        return action, confidence
