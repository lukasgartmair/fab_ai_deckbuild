#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:45:13 2024

@author: lukasgartmair
"""

from enemy import Enemy
from special_mechanics import Boost
from playstyle import Keyword, PlayerClass
from utils import n_chance


class Mechanologist(Enemy):
    def __init__(self, player_class=PlayerClass.mechanologist):
        super().__init__(player_class=PlayerClass.mechanologist)

        self.boost = Boost()

        self.banished_zone["boosted_cards"] = []

    def determine_if_boost_makes_sense(self):
        p = (len(self.hand) + self.arsenal.get_length()) / (
            self.intellect + self.arsenal.get_length()
        ) + 0.3
        print(p)
        if n_chance(p):
            return True
        else:
            return False

    def apply_boost_mechanic(self, card):
        print("boosting")
        if Keyword.boost in card.keywords:
            if self.determine_if_boost_makes_sense():
                if len(self.hand) > 0:
                    banished_card = self.deck.draw_top_card()
                    self.banished_zone["boosted_cards"].append(banished_card)
                    if banished_card.card_class == PlayerClass.mechanologist:
                        print("Mechanoligist boost activated")
                        self.boost.activation()
                        self.action_point_manager.obtain_action_points()
                    else:
                        self.boost.fail()

    def start_move(self):
        super().start_move()
        self.boost.move_reset()

    def reset_play(self):
        super().reset_play()
        self.boost.turn_reset()

    def class_specific_helper_1(self, card):
        self.apply_boost_mechanic(card)
