#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:16:25 2024

@author: lukasgartmair
"""
from enum import Enum


class PlayerClasses(Enum):
    ninja = 0
    ranger = 1
    brute = 2
    mechanologist = 3
    runeblade = 4
    wizard = 5
    warrior = 6
    guardian = 7
    illusionist = 8
    # merchant = 9
    # shapeshifter = 10
    # bard = 11
    generic = 12


class Keywords(Enum):
    go_again = 0
    dominate = 1
    intimidate = 2
    none = 3


class CardType(Enum):
    non_attack_action = 0
    attack_action = 1
    attack_reaction = 2
    defensive_reaction = 3


class Playstyle:
    def __init__(self):
        self.strategy_parameters = {"mu": 4, "sigma": 3}
        self.card_type_ratios = {
            "non_attack_action": 15,
            "attack_action": 60,
            "attack_reaction": 15,
            "defensive_reaction": 10,
        }
        self.keywords = list(Keywords)
        self.keyword_ratios = {
            "go_again": 75,
            "dominate": 20,
            "intimidate": 0,
            "none": 5,
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
            "go_again": 65,
            "dominate": 15,
            "intimidate": 0,
            "none": 20,
        }


class Ninjalike(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 3, "sigma": 2}
        self.keywords = [Keywords.go_again]
        self.keyword_ratios = {"go_again": 100}
