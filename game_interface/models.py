#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:14:02 2023

@author: lukasgartmair
"""

from enum import Enum
import pygame
import random
import database

default_deck = {'tree_0':1, 'tree_1':1, 'wise_man_0':2}

class CardClass(Enum):
    PLAYER = 0
    TREE = 1
    WISE_MAN = 2

class Card:
    card_class = None
    image = None
    index = 0

    def __init__(self, card_id, card_name):
        self.card_id = card_id
        self.card_name = card_name
        self.image = pygame.image.load(
            'images/' + self.card_name.lower().replace(" ","_") + '.png')

class Deck:
    cards = None

    def __init__(self):
        self.cards = []
        cards = database.get_cards_from_database()
        # for key, value in default_deck.items():
        #     self.cards.append(Card(value, key))

        for card in cards:
            self.cards.append(Card(int(card[0]), card[1]))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)


class Pile:
    cards = None

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def get_current_card(self):
        if (len(self.cards) > 0):
            return self.cards[-1]
        else:
            return None

class Player:

    name = None
    playKey = None


    def __init__(self, name, playKey):
        self.deck = None
        self.pile = Pile()
        self.hand = []
        self.playKey = playKey
        self.name = name
        self.deck = Deck()

    def init_hand(self):
        self.deck.shuffle()
        self.hand = self.deck.cards

    def play(self):
        popped_card = self.hand.pop(0)
        self.pile.add(popped_card)
        return popped_card
    
