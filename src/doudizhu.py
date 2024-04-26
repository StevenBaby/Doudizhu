import os

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
