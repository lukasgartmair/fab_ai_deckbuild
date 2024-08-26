#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:48:29 2024

@author: lukasgartmair
"""


from settings import grid
from colors import color_palette
import pygame
from utils import add_two_with_possible_none_type


class LifeCounter:
    def __init__(self, life):
        self.life = life

    def decrease_life(self, value=1):
        self.life -= value

    def increase_life(self, value=1):
        self.life += value

    def calculate_life(self, player_attack, enemy_block):
        # print("Block balance:")

        block_total = enemy_block.calc_total_block()
        # print(block_total)

        attack_total = add_two_with_possible_none_type(player_attack.physical, player_attack.arcane)

        # print(attack_total)

        # print("result")
        result = attack_total - block_total
        if result > 0:
            self.life -= result

        if self.life <= 0:
            self.life = 0
