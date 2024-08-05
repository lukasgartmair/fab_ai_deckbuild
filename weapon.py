#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:59:06 2024

@author: lukasgartmair
"""

from enum import Enum
import numpy as np
import random


class Handed(Enum):
    one_handed = 0
    two_handed = 1


class Keyword(Enum):
    go_again = 0
    none = 1


class Weapon:
    def __init__(self):
        self.hand_occupation = Handed.two_handed
        self.attack = 1
        self.keywords = []
