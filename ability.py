#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:20:48 2024

@author: lukasgartmair
"""

import random
from enum import Enum


class SpecialAbilitiy(Enum):
    improved_defense = 0
    improved_offense = 1
    arcane = 2


class Ability:
    def __init__(self):
        self.special_ability = random.choice(list(SpecialAbilitiy))
