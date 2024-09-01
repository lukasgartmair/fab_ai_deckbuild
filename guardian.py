#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:07:01 2024

@author: lukasgartmair
"""

from enemy import Enemy
from playstyle import PlayerClass
from utils import n_chance


class Guardian(Enemy):
    def __init__(self, player_class=PlayerClass.guardian):
        super().__init__(player_class=PlayerClass.guardian)

    def reorder_hand(self, hand):
        if n_chance(p=1):
            hand = sorted(
                hand, key=lambda x: (x.physical, x.card_type.value * -1), reverse=True
            )
            self.print_reordered_hand(hand)
        return hand
