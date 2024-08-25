#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:21:39 2024

@author: lukasgartmair
"""


class LevelManager:
    def __init__(self, level=1):
        self.move_index = 1
        self.turn_index = 1
        self.current_level = level

    def advance_level(self):
        self.current_level += 1
        self.reset_move_index()
        self.reset_turn_index()

    def advandce_turn(self):
        self.turn_index += 1
        self.reset_move_index()

    def reset_move_index(self):
        self.move_index = 1

    def reset_turn_index(self):
        self.turn_index = 1

    def advandce_move(self):
        self.move_index += 1
