#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:04:48 2024

@author: lukasgartmair
"""

from playstyle import Keyword


class ActionPointManager:
    def __init__(self):
        self.action_points = 0

    def reset_action_points(self):
        self.action_points = 1

    def obtain_action_points(self, amount=1):
        self.action_points += amount

    def use_action_points(self, amount=1):
        if self.action_points >= amount:
            self.action_points -= amount
            return True
        else:
            return False

    def handle_go_again(self, c):
        if Keyword.go_again in c.keywords:
            self.obtain_action_points()
