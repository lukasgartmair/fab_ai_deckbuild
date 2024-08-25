#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:48:29 2024

@author: lukasgartmair
"""

import PygameUtils as pu
from settings import grid
from colors import color_palette
import pygame
from utils import add_two_with_possible_none_type

button_size = 25


class LifeCounter:
    def __init__(self, enemy):
        self.enemy = enemy
        self.button_up = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(0),
            button_size,
            button_size,
        )
        self.button_down = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(0) + button_size + 5,
            button_size,
            button_size,
        )

    def increase_life(self):
        self.enemy.increase_life()

    def decrease_life(self):
        self.enemy.decrease_life()

    def calculate_life(self, player_attack):
        # print("Block balance:")

        block_total = self.enemy.block.calc_total_block()
        # print(block_total)

        attack_total = add_two_with_possible_none_type(
            player_attack.physical, player_attack.arcane
        )

        # print(attack_total)

        # print("result")
        result = attack_total - block_total
        if result > 0:
            self.enemy.life -= result

        if self.enemy.life <= 0:
            self.enemy.life = 0
