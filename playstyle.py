#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:16:25 2024

@author: lukasgartmair
"""
from enum import Enum


class PlayerClass(Enum):
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
    generic = 9


def get_playstyle(player_class):
    match player_class:
        case player_class if player_class == PlayerClass.ninja:
            return NinjaBasic()
        case player_class if player_class == PlayerClass.ranger:
            return RangerBasic()
        case player_class if player_class == PlayerClass.brute:
            return BruteBasic()
        case player_class if player_class == PlayerClass.mechanologist:
            return MechanologistBasic()
        case player_class if player_class == PlayerClass.runeblade:
            return RunebladeBasic()
        case player_class if player_class == PlayerClass.wizard:
            return WizardBasic()
        case player_class if player_class == PlayerClass.warrior:
            return WarriorBasic()
        case player_class if player_class == PlayerClass.guardian:
            return GuardianBasic()
        case player_class if player_class == PlayerClass.illusionist:
            return IllusionistBasic()

        case _:
            return Playstyle()


class Talent(Enum):
    light = 0
    shadow = 1
    draconic = 2
    royal = 3
    draconic_illusionist = 4
    elemental_lightning = 5
    elemental_ice = 6
    elemental_earth = 7


class Keyword(Enum):
    go_again = 0
    dominate = 1
    intimidate = 2
    # crush = 3
    # reprise = 4
    # combo = 5
    # spectra = 6
    # phantasm = 7
    # soul = 8
    # blood_debt = 9
    # quell = 10
    boost = 11
    no_keyword = 3


class CardType(Enum):
    non_attack_action = 0
    attack_action = 1
    attack_reaction = 2
    defensive_reaction = 3
    weapon = 4


class Playstyle:
    def __init__(self):
        self.strategy_parameters = {"mu": 4, "sigma": 3}
        self.card_type_ratios = {
            "non_attack_action": 15,
            "attack_action": 60,
            "attack_reaction": 15,
            "defensive_reaction": 10,
        }
        self.keywords = list(Keyword)
        self.keyword_ratios = {
            "go_again": 60,
            "dominate": 0,
            "intimidate": 0,
            "boost": 0,
            "no_keyword": 40,
        }

        self.arcane_ratio = 0

    def __str__(self):
        return type(self).__name__


strategy_parameters = {
    "aggressive": {"mu": 4, "sigma": 2},
    "neutral": {"mu": 3, "sigma": 1},
    "defensive": {"mu": 1.5, "sigma": 2},
}


class NinjaBasic(Playstyle):
    def __init__(self):
        super().__init__()

        self.strategy_parameters = {"mu": 3, "sigma": 2}
        self.keywords = [Keyword.go_again]
        self.keyword_ratios = {"go_again": 100}


class RangerBasic(Playstyle):
    def __init__(self):
        super().__init__()


class BruteBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 5, "sigma": 1}
        self.keywords = [Keyword.dominate, Keyword.intimidate]
        self.keyword_ratios = {"dominate": 50, "intimidate": 50}
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 80,
            "attack_reaction": 10,
            "defensive_reaction": 5,
        }


class MechanologistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 5, "sigma": 1}
        self.keywords = [Keyword.boost]
        self.keyword_ratios = {"boost": 80, "no_keyword": 20}


class RunebladeBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 3}
        self.arcane_ratio = 0.5


class WizardBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 2, "sigma": 3}
        self.arcane_ratio = 0.8


class WarriorBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 3}
        self.keywords = [Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {"go_again": 50, "no_keyword": 50}
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 60,
            "attack_reaction": 30,
            "defensive_reaction": 5,
        }


class GuardianBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 7, "sigma": 2}
        self.keywords = [Keyword.dominate, Keyword.no_keyword]
        self.keyword_ratios = {"dominate": 50, "no_keyword": 50}
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 45,
            "attack_reaction": 25,
            "defensive_reaction": 25,
        }


class IllusionistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 2}


class Aggressive(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 2}
        self.keywords = [Keyword.go_again, Keyword.dominate, Keyword.no_keyword]
        self.keyword_ratios = {
            "go_again": 65,
            "dominate": 15,
            "no_keyword": 20,
        }
