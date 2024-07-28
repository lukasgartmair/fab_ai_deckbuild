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
from wonderwords import RandomSentence
from randimage import get_random_image, show_array

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
    size = 25
    img_size = (size, size)
    img = get_random_image(img_size)
    img = 255 * img / img.max()
    return pygame.surfarray.make_surface(img)


class CardType(Enum):
    # non_attack_action = 0
    attack_action = 1
    # attack_reaction = 2
    # defensive_reaction = 3


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
    def __init__(self, power):
        self.card_id = next(id_iter)
        self.name = generate_rnd_name()
        self.type = np.random.choice(list(CardType))
        self.cost = 0
        self.power = power
        self.defense = 0
        self.pitch = 0
        self.color = 0
        self.keyword = None
        self.image = generate_rnd_image()
        self.calc_card_values()

    def __str__(self):
        return "Card {} -'{}' with power {} / defense {} / pitch {} / cost {}".format(
            self.card_id, self.name, self.power, self.defense, self.pitch, self.cost
        )

    def calc_card_values(self):
        # (Power (6) + Defense (3) + Pi
        # https://fab.cardsrealm.com/en-us/articles/guide-everything-about-value-and-turn-cycle-in-flesh-and-bloodtch (1)) - Cost (2) = 8

        self.color = np.random.choice(list(CardColor))
        self.pitch = pitch_values[self.color.name]
        self.defense = defensive_values[self.type.name]
        self.cost = self.power + self.defense + self.pitch - TARGET_VALUE
        if self.cost < 0:
            self.cost = 0
