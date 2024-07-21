#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:14:02 2023

@author: lukasgartmair
"""

import pygame
import random
from deck import Deck
from pile import Pile


class Player:
    name = None
    playKey = None

    def __init__(self, play_key=None):
        self.deck = None
        self.pile = Pile()
        self.hand = []
        self.play_key = play_key
        self.name = "Player"
        self.deck = Deck()

    def init_hand(self):
        self.deck.shuffle()
        self.hand = self.deck.cards

    def play(self):
        popped_card = self.hand.pop(0)
        self.pile.add(popped_card)
        return popped_card
