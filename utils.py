#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:17:47 2024

@author: lukasgartmair
"""

import numpy as np
import pygame
from colors import color_palette
import itertools


def n_chance(p=0.85):
    if np.random.rand() < p:
        return True
    else:
        return False


def get_combinations(array):
    combinations = []
    array_copy = array.copy()
    if len(array_copy) > 0:
        for i in range(len(array) + 1):
            combos = itertools.combinations(array_copy, i)
            for c in combos:
                combinations.append(c)
    return combinations[1:]


def shift_list(a):
    x = a.pop()
    a.insert(0, x)
    return a


def add_two_with_possible_none_type(a, b):
    return (a or 0) + (b or 0)


def blit_text(surface, text, pos, font, color=color_palette.color5):
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
