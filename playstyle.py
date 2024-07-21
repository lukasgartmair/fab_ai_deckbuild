#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:16:25 2024

@author: lukasgartmair
"""
from enum import Enum


class Keywords(Enum):
    go_again = 0
    dominate = 1
    intimidate = 2


class Playstyle:
    def __init__(self):
        self.strategy_parameters = {"mu": 0, "sigma": 0}

        self.keywords = []
        self.keyword_ratio = {}

    def __str__(self):
        return type(self).__name__


class DeckStrategy(Enum):
    defensive = 0
    neutral = 1
    aggressive = 2


strategy_parameters = {
    "aggressive": {"mu": 4, "sigma": 2},
    "neutral": {"mu": 3, "sigma": 1},
    "defensive": {"mu": 1.5, "sigma": 2},
}


class Aggressive(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 2}


class Ninjalike(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 3, "sigma": 2}

        self.keywords = [Keywords.go_again]

        self.keyword_ratio = {"go_again": 0.25}
