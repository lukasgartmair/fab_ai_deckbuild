#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:48:29 2024

@author: lukasgartmair
"""
from block import calc_total_physical_block, calc_total_arcane_block
from utils import subtract_two_with_possible_none_type
import animation
import base_animation


class LifeCounter:
    def __init__(self, life, sound):
        self.life = life
        self.sound = sound
        self.current_amount = None

    def decrease_life(self, amount=1):

        self.current_amount = amount

        base_animation.animation_queue.add_to_animation_loop(
            self, animation.LifeCounterAnimation(self)
        )
        if amount >= 5:
            self.sound.play_pain()
        self.life -= amount

    def increase_life(self, amount=1):
        self.life += amount

    def calculate_life(self, player_attack):
        if player_attack.physical.is_empty() == False:
            for k, v in player_attack.physical.damage_steps.items():
                result = subtract_two_with_possible_none_type(
                    v, calc_total_physical_block(player_attack.physical.blocked_with[k])
                )
                if result > 0:
                    self.decrease_life(result)

        if player_attack.arcane.is_empty() == False:
            for k, v in player_attack.arcane.damage_steps.items():
                result = subtract_two_with_possible_none_type(
                    v, calc_total_arcane_block(player_attack.arcane.blocked_with[k])
                )
                if result > 0:
                    self.decrease_life(result)

        if self.life <= 0:
            self.life = 0

    # def calculate_life(self, enemy_block):
    #     # print("Block balance:")

    #     block_total = enemy_block.calc_total_block()
    #     # print(block_total)

    #     attack_total = add_two_with_possible_none_type(
    #         enemy_block.player_attack.physical, enemy_block.player_attack.arcane
    #     )

    #     result = attack_total - block_total
    #     if result > 0:
    #         self.decrease_life(amount=result)

    #     if self.life <= 0:
    #         self.life = 0
