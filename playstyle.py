#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:16:25 2024

@author: lukasgartmair
"""
from enum import Enum


class CardColor(Enum):
    red = 0
    yellow = 1
    blue = 2


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
    combo = 5
    # spectra = 6
    # phantasm = 7
    # soul = 8
    blood_debt = 9
    # quell = 10
    beat_chest = 10
    boost = 11
    charge = 12
    opt = 13
    reload = 14
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
        self.keywords = [Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {
            "go_again": 60,
            "no_keyword": 40,
        }

        self.arcane_ratio = 0

        self.pitch_ratios = {
            CardColor.red: 33,
            CardColor.yellow: 33,
            CardColor.blue: 33,
        }

        assert len(self.keywords) == len(self.keyword_ratios)

    def __str__(self):
        return type(self).__name__


class NinjaBasic(Playstyle):
    def __init__(self):
        super().__init__()

        self.strategy_parameters = {"mu": 4, "sigma": 3}
        self.keywords = [Keyword.go_again, Keyword.combo]
        self.keyword_ratios = {"go_again": 70, "combo": 30}

        self.card_type_ratios = {
            "non_attack_action": 35,
            "attack_action": 50,
            "attack_reaction": 5,
            "defensive_reaction": 10,
        }

        self.pitch_ratios = {
            CardColor.red: 60,
            CardColor.yellow: 5,
            CardColor.blue: 35,
        }


class RangerBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 7, "sigma": 4}
        self.keywords = [
            Keyword.go_again,
            Keyword.no_keyword,
        ]
        self.keyword_ratios = {"go_again": 70, "no_keyword": 30}

        self.card_type_ratios = {
            "non_attack_action": 35,
            "attack_action": 50,
            "attack_reaction": 5,
            "defensive_reaction": 10,
        }

        self.pitch_ratios = {
            CardColor.red: 60,
            CardColor.yellow: 15,
            CardColor.blue: 25,
        }


class BruteBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 6, "sigma": 1}
        self.keywords = [
            Keyword.go_again,
            Keyword.beat_chest,
            Keyword.dominate,
            Keyword.intimidate,
            Keyword.no_keyword,
        ]
        self.keyword_ratios = {
            "go_again": 30,
            "beat_chest": 10,
            "dominate": 25,
            "intimidate": 25,
            "no_keyword": 10,
        }
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 60,
            "attack_reaction": 35,
            "defensive_reaction": 0,
        }

        self.pitch_ratios = {
            CardColor.red: 50,
            CardColor.yellow: 20,
            CardColor.blue: 30,
        }


class MechanologistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 4}
        self.keywords = [Keyword.boost, Keyword.no_keyword]
        self.keyword_ratios = {"boost": 80, "no_keyword": 20}

        self.card_classes = [PlayerClass.generic, PlayerClass.mechanologist]
        self.card_class_ratios = {"generic": 20, "mechanologist": 80}

        self.card_type_ratios = {
            "non_attack_action": 50,
            "attack_action": 40,
            "attack_reaction": 5,
            "defensive_reaction": 5,
        }

        self.pitch_ratios = {
            CardColor.red: 35,
            CardColor.yellow: 15,
            CardColor.blue: 40,
        }


class RunebladeBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 6, "sigma": 2}
        self.arcane_ratio = 0.5

        self.keywords = [Keyword.go_again, Keyword.blood_debt, Keyword.no_keyword]
        self.keyword_ratios = {"go_again": 70, "blood_debt": 10, "no_keyword": 20}

        self.card_type_ratios = {
            "non_attack_action": 60,
            "attack_action": 30,
            "attack_reaction": 5,
            "defensive_reaction": 5,
        }

        self.pitch_ratios = {
            CardColor.red: 50,
            CardColor.yellow: 10,
            CardColor.blue: 40,
        }


class WizardBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 3, "sigma": 3}
        self.keywords = [Keyword.opt, Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {"opt": 50, "go_again": 30, "no_keyword": 20}
        self.arcane_ratio = 0.8
        self.pitch_ratios = {
            CardColor.red: 35,
            CardColor.yellow: 20,
            CardColor.blue: 45,
        }


class WarriorBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 3.5, "sigma": 2}
        self.keywords = [Keyword.charge, Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {"charge": 50, "go_again": 30, "no_keyword": 20}
        self.card_type_ratios = {
            "non_attack_action": 40,
            "attack_action": 40,
            "attack_reaction": 15,
            "defensive_reaction": 5,
        }

        self.pitch_ratios = {
            CardColor.red: 30,
            CardColor.yellow: 70,
            CardColor.blue: 0,
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
        self.pitch_ratios = {
            CardColor.red: 0,
            CardColor.yellow: 50,
            CardColor.blue: 50,
        }


class IllusionistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.strategy_parameters = {"mu": 4, "sigma": 2}

        self.pitch_ratios = {
            CardColor.red: 25,
            CardColor.yellow: 25,
            CardColor.blue: 50,
        }


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

        self.pitch_ratios = {
            CardColor.red: 50,
            CardColor.yellow: 50,
            CardColor.blue: 0,
        }
