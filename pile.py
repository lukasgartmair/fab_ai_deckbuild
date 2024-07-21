#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:07:43 2024

@author: lukasgartmair
"""


class Pile:
    cards = None

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def get_current_card(self):
        if len(self.cards) > 0:
            return self.cards[-1]
        else:
            return None
