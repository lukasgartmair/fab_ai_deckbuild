#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:48:29 2024

@author: lukasgartmair
"""
from utils import add_two_with_possible_none_type


class LifeCounter:
    def __init__(self, life, sound):
        self.life = life
        self.sound = sound

    def decrease_life(self, amount=1):
        self.life -= amount

        if amount >= 5:
            self.sound.play_pain()

    def increase_life(self, amount=1):
        self.life += amount

    def calculate_life(self, enemy_block):
        # print("Block balance:")

        block_total = enemy_block.calc_total_block()
        # print(block_total)

        attack_total = add_two_with_possible_none_type(
            enemy_block.player_attack.physical, enemy_block.player_attack.arcane
        )

        result = attack_total - block_total
        if result > 0:
            self.decrease_life(amount=result)

        if self.life <= 0:
            self.life = 0
