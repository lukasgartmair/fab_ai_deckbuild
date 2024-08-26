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
from playstyle import CardType, CardColor
from colors import color_palette

id_iter = itertools.count()

TARGET_VALUE = 8
MAX_ATTACK = 6
MIN_ATTACK = 2

MAX_CARD_COST = 4


def generate_rnd_name():
    s = RandomSentence()
    sb = s.bare_bone_sentence()
    sb_split = sb.split()
    return "{} {}".format(sb_split[-1], sb_split[-2]).replace("s.", "")


def generate_rnd_image(size):
    img_size = (size, size)
    img = get_random_image(img_size)
    img = 255 * img / img.max()
    return pygame.surfarray.make_surface(img)


# card_colors = {"red": (255, 0, 0), "yellow": (255, 255, 0), "blue": (0, 0, 255)}
card_colors = {
    "red": pygame.Color(color_palette.color3),
    "yellow": pygame.Color(color_palette.color5),
    "blue": pygame.Color(color_palette.color2),
}

pitch_values = {"red": 1, "yellow": 2, "blue": 3}

defensive_values = {
    "non_attack_action": 2,
    "attack_action": 3,
    "attack_reaction": 2,
    "defensive_reaction": 4,
}


class Card:
    def __init__(self, card_resolution=5):
        self.card_id = next(id_iter)
        self.name = generate_rnd_name()
        self.card_type = None
        self.card_class = PlayerClass.generic
        self.cost = 0
        self.physical = 0
        self.arcane = 0
        self.defense = 0
        self.pitch = 0
        self.color = CardColor.red
        self.keywords = []
        self.card_resolution = card_resolution
        self.image = generate_rnd_image(card_resolution)

    def __str__(self):
        return (
            "Card {} -'{}' with physical {} / defense {} / pitch {} / cost {}".format(
                self.card_id,
                self.name,
                self.physical,
                self.defense,
                self.pitch,
                self.cost,
            )
        )

    def calc_card_values(self):
        # (physical (6) + Defense (3) + Pi
        # https://fab.cardsrealm.com/en-us/articles/guide-everything-about-value-and-turn-cycle-in-flesh-and-bloodtch (1)) - Cost (2) = 8

        self.pitch = pitch_values[self.color.name]
        self.defense = defensive_values[self.card_type.name]

        self.cost = (
            self.physical + self.arcane + self.defense + self.pitch - TARGET_VALUE
        )
        if self.cost < 0:
            self.cost = 0
        elif self.cost > 4:
            self.cost = MAX_CARD_COST

    # def adjust_arcane_physical(self):
    #     if self.physical > 0 and self.card_type != CardType.defensive_reaction:
    #         self.arcane = np.random.randint(1, 4)
    #         self.physical -= self.arcane // 2
    #         if self.physical < 0:
    #             self.physical = 0
