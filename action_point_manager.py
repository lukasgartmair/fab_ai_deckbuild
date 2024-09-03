#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:04:48 2024

@author: lukasgartmair
"""

from playstyle import Keyword


class ActionPointManager:
    def __init__(self, action_points=1):
        self.action_points = 1

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

    def handle_go_again(self, card):
        if Keyword.go_again in card.keywords:
            self.obtain_action_points()

    def handle_combo(self, card, combat_chain):
        if Keyword.combo in card.keywords:
            if combat_chain.iterator > 0:
                if (
                    Keyword.combo
                    in combat_chain.chain[combat_chain.iterator - 1]["play"].keywords
                ):
                    print("combo activated")
                    self.obtain_action_points()

    def handle_boost(self, card):
        if Keyword.boost in card.keywords:
            return True
        else:
            return False

    def handle_keywords(self, card, combat_chain=None):
        self.handle_go_again(card)
        self.handle_boost(card)
        # if combat_chain is not None:
        #     self.handle_combo(card, combat_chain)

    def has_action_points_left(self):
        return True if self.action_points > 0 else False
