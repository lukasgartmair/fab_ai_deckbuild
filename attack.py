#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:51:34 2024

@author: lukasgartmair
"""


class Attack:
    def __init__(self, enemy):
        self.enemy = enemy

    def get_next_attacking_card(self):
        c = self.enemy.combat_chain.chain[self.enemy.combat_chain.iterator]["attack"]
        self.enemy.played_cards.append(c)
        return c

    def base_attack(self):
        c = self.get_next_attacking_card()

        self.enemy.pitch_cards()
        self.enemy.remove_played_cards()
        self.enemy.use_floating_resources(c.cost)
        self.enemy.use_action_points()
        self.enemy.handle_go_again(c)

        self.enemy.sound.play_attack(c)

        return c
