#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:17:47 2024

@author: lukasgartmair
"""

import numpy as np
from colors import color_palette
import itertools
from numpy import prod
from settings import height, width


def factorial(n):
    return prod(range(1, n + 1))


def normalize_position(position):
    return (position[0] / width * 100, position[1] / height * 100)


def n_chance(p=0.85):
    if np.random.rand() < p:
        # print("chance True")
        return True
    else:
        # print("chance False")
        return False


def have_common_items(a, b):
    return not set(a).isdisjoint(b)


def get_permutations(array, max_length=None):
    if max_length is None:
        max_length = len(array) + 1
    permutations = []
    array_copy = array.copy()
    if len(array_copy) > 0:
        for i in range(max_length):
            combos = itertools.permutations(array_copy, r=i)
            for c in combos:
                permutations.append(c)
    return permutations[1:]


def get_combinations(array, max_length=None):
    if max_length is None:
        max_length = len(array) + 1
    combinations = []
    array_copy = array.copy()
    if len(array_copy) > 0:
        for i in range(max_length):
            combos = itertools.combinations(array_copy, r=i)
            for c in combos:
                combinations.append(c)
    return combinations[1:]


def map_permutations_to_original(array, permutations):
    return [[array[pi] for pi in p] for p in permutations]


def map_combinations_to_original(array, combinations):
    return [[array[pi] for pi in p] for p in combinations]


def shift_list(a):
    x = a.pop()
    a.insert(0, x)
    return a


def add_two_with_possible_none_type(a, b):
    return (a or 0) + (b or 0)


def subtract_two_with_possible_none_type(a, b):
    return (a or 0) - (b or 0)


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
