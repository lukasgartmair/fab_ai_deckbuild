#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:55:49 2024

@author: lukasgartmair
"""

from enum import Enum
import numpy as np
import itertools

id_iter = itertools.count()

TARGET_VALUE = 8
MAX_ATTACK = 6
MIN_ATTACK = 2
n_cards = 30

def generate_attack_distribution(n_cards):
    n, p = 10, .5
    s = np.random.binomial(n, p, n_cards*2)
    s_clipped = np.array([x for x in s if MIN_ATTACK <= x <= MAX_ATTACK])
    s_choice = np.random.choice(s_clipped,n_cards)
    return s_choice

def get_rnd_power(n=1):
    v = -1
    while v:
        mu, sigma = 4, 2 # mean and standard deviation
        s = np.random.normal(mu, sigma, n)
        v = s[0]
        if MIN_ATTACK <= v <= MAX_ATTACK:
            break
    return np.round(v).astype(int)

class CardType(Enum):

    action = 0
    attack_action = 1
    # attack_reaction = 2
    # defensive_reaction = 3
    
class CardColor(Enum):
    red = 0,
    yellow = 1,
    blue = 2
    
class Keywords(Enum):
    go_again = 0
    dominate = 1
    intimidate = 2
    
pitch_values = {
    "red" : 1,
    "yellow" : 2,
    "blue" : 3
    }

defensive_values = {
    "action" : 2,
    "attack_action" : 3,
    "defensive_reaction" : 4
    }
    
class Deck:
    def __init__(self):
        self.n_cards = 10
        self.cards = []
        self.stats = {}
        
        self.build_deck()
        self.calc_stats()
    
    def build_deck(self):
        self.cards = [Card() for n in range(self.n_cards)]
    
    def calc_stats(self):
        self.card_types = [c.card_type.name for c in self.cards]
        
        self.n_reds = len([c for c in self.cards if c.color == CardColor.red])
        self.n_yellows = len([c for c in self.cards if c.color == CardColor.yellow])
        self.n_blues = len([c for c in self.cards if c.color == CardColor.blue])
        
        self.powers = [c.power for c in self.cards]
        self.defenses = [c.defense for c in self.cards]
        self.pitches = [c.pitch for c in self.cards]
        self.costs = [c.cost for c in self.cards]
        
        
class Card:
    def __init__(self):
        self.card_id = next(id_iter)
        self.card_type = np.random.choice(list(CardType))
        self.cost = 0
        self.power = 0
        self.defense = 0
        self.pitch = 0
        self.color = 0
        
        self.calc_card_values()
        
    def __str__(self):
        return "Card {} w. power {} / defense {} / pitch {} / cost {}".format(self.card_id, self.power, self.defense, self.pitch, self.cost)
        
    def calc_card_values(self):
        # (Power (6) + Defense (3) + Pi
        #https://fab.cardsrealm.com/en-us/articles/guide-everything-about-value-and-turn-cycle-in-flesh-and-bloodtch (1)) - Cost (2) = 8
        
        self.color = np.random.choice(list(CardColor))
        self.pitch = pitch_values[self.color.name]
        self.power = get_rnd_power()
        self.defense = defensive_values[self.card_type.name]
        self.cost = TARGET_VALUE - self.power - self.defense - self.pitch
        if self.cost <= 0:
            self.cost = 0
         
         
class Enemy:
    def __init__(self):
        self.name = "ai_enemy"
        self.intellect = 4
        self.life = 20
        self.hand = []
        self.original_deck = Deck()
        self.deck = self.original_deck.cards
        self.graveyard = []
        self.banished_zone = []
        self.arsenal = []
        self.weapon_zone_1 = []
        self.weapon_zone_2 = []
        
    def show_hand(self):
        for c in self.hand:
            print(str(c))
        
    def draw(self):
        
        self.hand = self.deck[:4]
        
        
        
        
        
        
        