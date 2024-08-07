#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:00:56 2024

@author: lukasgartmair
"""

from enum import Enum
import itertools
import pygame
import numpy as np
from playstyle import PlayerClass
from wonderwords import RandomSentence
from randimage import get_random_image, show_array
from settings import CARD_RESOLUTION
from playstyle import CardType

id_iter = itertools.count()

TARGET_VALUE = 8
MAX_ATTACK = 6
MIN_ATTACK = 2


def generate_rnd_name():
    s = RandomSentence()
    sb = s.bare_bone_sentence()
    sb_split = sb.split()
    return "{} {}".format(sb_split[-1], sb_split[-2]).replace("s.", "")


def generate_rnd_image():
    size = CARD_RESOLUTION
    img_size = (size, size)
    img = get_random_image(img_size)
    img = 255 * img / img.max()
    return pygame.surfarray.make_surface(img)


class CardColor(Enum):
    red = (0,)
    yellow = (1,)
    blue = 2


card_colors = {"red": (255, 0, 0), "yellow": (255, 255, 0), "blue": (0, 0, 255)}

pitch_values = {"red": 1, "yellow": 2, "blue": 3}

defensive_values = {
    "non_attack_action": 2,
    "attack_action": 3,
    "attack_reaction": 2,
    "defensive_reaction": 4,
}


class Card:
    def __init__(self):
        self.card_id = next(id_iter)
        self.name = generate_rnd_name()
        self.card_type = None
        self.card_class = PlayerClass.generic
        self.cost = 0
        self.power = 0
        self.arcane = 0
        self.defense = 0
        self.pitch = 0
        self.color = 0
        self.keywords = []
        self.image = generate_rnd_image()

    def __str__(self):
        return "Card {} -'{}' with power {} / defense {} / pitch {} / cost {}".format(
            self.card_id, self.name, self.power, self.defense, self.pitch, self.cost
        )

    def calc_values(self):
        # (Power (6) + Defense (3) + Pi
        # https://fab.cardsrealm.com/en-us/articles/guide-everything-about-value-and-turn-cycle-in-flesh-and-bloodtch (1)) - Cost (2) = 8

        self.color = np.random.choice(list(CardColor))
        self.pitch = pitch_values[self.color.name]
        self.defense = defensive_values[self.card_type.name]

        self.cost = self.power + self.defense + self.pitch - TARGET_VALUE
        if self.cost < 0:
            self.cost = 0
            
    def adjust_arcane_power(self):
        
        if self.power > 0 and self.card_type != CardType.defensive_reaction:
            
            self.arcane = np.random.randint(1,4)
            self.power -= self.arcane
            if self.power < 0:
                self.power = 0
        