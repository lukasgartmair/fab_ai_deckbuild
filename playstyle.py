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
    none = 3


class Playstyle:
    def __init__(self):
        self.strategy_parameters = {"mu": 4, "sigma": 3}

        self.keywords = list(Keywords)
        self.keyword_ratios = {
            "none": 25,
            "go_again": 25,
            "dominate": 25,
            "intimidate": 25,
        }

    def __str__(self):
        return type(self).__name__


strategy_parameters = {
    "aggressive": {"mu": 4, "sigma": 2},
    "neutral": {"mu": 3, "sigma": 1},
    "defensive": {"mu": 1.5, "sigma": 2},
}


class Aggressive(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 2}
        self.keywords = list(Keywords)
        self.keyword_ratios = {
            "none": 0,
            "go_again": 50,
            "dominate": 50,
            "intimidate": 0,
        }


class Ninjalike(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 3, "sigma": 2}
        self.keywords = [Keywords.go_again]
        self.keyword_ratios = {"go_again": 100}
