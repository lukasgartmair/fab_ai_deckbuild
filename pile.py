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

    def get_top_n_cards(self, n=1):
        if len(self.cards) > 0:
            return self.cards[:n]
        else:
            return None

    def get_bottom_n_cards(self, n=1):
        if len(self.cards) > 0:
            return self.cards[-n:]
        else:
            return None


class Graveyard(Pile):
    def __init__(self):
        super().__init__()


class BanishedZone(Pile):
    def __init__(self):
        super().__init__()
