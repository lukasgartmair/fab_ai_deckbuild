#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:59:06 2024

@author: lukasgartmair
"""

from enum import Enum
import numpy as np
import random
import pygame
from wonderwords import RandomWord
from randimage import get_random_image, show_array
from settings import CARD_RESOLUTION
from deck import Keyword
from utils import n_chance

r = RandomWord()


def generate_rnd_name():
    r.word()
    rnd_word = r.word(
        word_min_length=5,
        word_max_length=30,
        include_parts_of_speech=["nouns"],
        ends_with="er",
    )
    return rnd_word


def generate_rnd_image():
    size = CARD_RESOLUTION
    img_size = (size, size)
    img = get_random_image(img_size)
    img = img / img.max()
    return pygame.surfarray.make_surface(img)


class HandOccupation(Enum):
    one_handed = 0
    two_handed = 1


def get_weapons():
    hand_occupation = random.choice(list(HandOccupation))
    if hand_occupation == HandOccupation.one_handed:
        return [Weapon(hand_occupation.one_handed), Weapon(hand_occupation.one_handed)]
    else:
        return [Weapon(hand_occupation.two_handed)]


class Weapon:
    def __init__(self, hand_occupation):
        self.name = generate_rnd_name()
        self.hand_occupation = hand_occupation
        self.physical = np.random.randint(1, 4)
        self.arcane = np.random.randint(0, 3)
        self.keywords = [Keyword.go_again]
        self.cost = np.random.randint(1, 3)

        self.image = generate_rnd_image()
