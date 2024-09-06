#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:07:15 2024

@author: lukasgartmair
"""

from enum import Enum
from utils import get_permutations


class LinkType(Enum):
    attack = 0
    attack_reaction = 1


attack_action_succession = [[1], [2, 1], [2, 2, 1], [2, 2, 2, 1]]
weapon_succession = [[4], [2, 4], [2, 2, 4], [2, 2, 2, 4]]

valid_card_type_successions = attack_action_succession + weapon_succession


class ChainLink:
    def __init__(self, play={}, pitch={}, link_type=LinkType.attack):
        self.play = play
        self.link_type = link_type
        self.pitch = pitch

    def is_empty(self):
        return True if len(self.play) == 0 else False

    def set_play(self, index, play, pitch=[]):
        self.play[index] = play
        self.pitch[index] = pitch


class CombatChain:
    def apply_succesion_restrictions(self, playable_cards):
        permutations = get_permutations(playable_cards)
        valid_combinations = []
        for combo in permutations:
            # print([c.card_type.value for c in combo])
            if [c.card_type.value for c in combo] in valid_card_type_successions:
                valid_combinations.append(combo)

        return valid_combinations
