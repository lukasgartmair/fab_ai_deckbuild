#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:16:25 2024

@author: lukasgartmair
"""
from enum import Enum
import numpy as np
import random


class CardColor(Enum):
    red = 0
    yellow = 1
    blue = 2


class WeaponType(Enum):
    bow = 0
    sword = 1
    cub = 2
    spear = 3
    axe = 4
    pistol = 5
    dagger = 6
    hammer = 8
    staff = 10
    scepter = 11
    claw = 12
    aura = 13


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
    no_talent = 0
    light = 1
    shadow = 2
    draconic = 3
    royal = 4
    lightning = 6
    ice = 7
    earth = 8


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
    equipment = 5


class Playstyle:
    def __init__(self):
        self.physical_parameters = {"mu": 4, "sigma": 3}
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
        if self.arcane_ratio > 0:
            self.arcane_parameters = {"mu": 2, "sigma": 2}

        self.pitch_ratios = {
            CardColor.red: 33,
            CardColor.yellow: 33,
            CardColor.blue: 33,
        }

        self.card_classes = [PlayerClass.generic]
        self.card_class_ratios = {"generic": 100}

        self.n_weapons = np.random.randint(1, 3)
        self.weapon_physical = np.random.randint(1, 5)
        self.weapon_arcane = 0
        self.go_again_chance = 0.5
        self.weapon_type = random.choice(list(WeaponType))

        assert len(self.keywords) == len(self.keyword_ratios)

    def __str__(self):
        return type(self).__name__


class NinjaBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 4, "sigma": 3}
        self.card_type_ratios = {
            "non_attack_action": 35,
            "attack_action": 50,
            "attack_reaction": 5,
            "defensive_reaction": 10,
        }

        self.keywords = [Keyword.go_again, Keyword.combo]
        self.keyword_ratios = {"go_again": 70, "combo": 30}

        self.pitch_ratios = {
            CardColor.red: 60,
            CardColor.yellow: 5,
            CardColor.blue: 35,
        }

        self.n_weapons = np.random.randint(1, 3)
        self.weapon_physical = np.random.randint(1, 3)
        self.weapon_arcane = 0
        self.go_again_chance = 1
        self.weapon_type = random.choice([WeaponType.dagger, WeaponType.staff])


class RangerBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 7, "sigma": 4}
        self.card_type_ratios = {
            "non_attack_action": 35,
            "attack_action": 50,
            "attack_reaction": 5,
            "defensive_reaction": 10,
        }

        self.keywords = [
            Keyword.go_again,
            Keyword.no_keyword,
        ]
        self.keyword_ratios = {"go_again": 70, "no_keyword": 30}

        self.pitch_ratios = {
            CardColor.red: 60,
            CardColor.yellow: 15,
            CardColor.blue: 25,
        }

        self.n_weapons = 1
        self.weapon_physical = np.random.randint(1, 8)
        self.weapon_arcane = 0
        self.go_again_chance = 0
        self.weapon_type = WeaponType.bow


class BruteBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 6, "sigma": 1}
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 60,
            "attack_reaction": 35,
            "defensive_reaction": 0,
        }

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

        self.pitch_ratios = {
            CardColor.red: 50,
            CardColor.yellow: 20,
            CardColor.blue: 30,
        }

        self.n_weapons = 1
        self.weapon_physical = np.random.randint(1, 10)
        self.weapon_arcane = 0
        self.go_again_chance = 0
        self.weapon_type = random.choice(
            [WeaponType.axe, WeaponType.cub, WeaponType.claw]
        )


class MechanologistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 4, "sigma": 4}
        self.card_type_ratios = {
            "non_attack_action": 50,
            "attack_action": 40,
            "attack_reaction": 5,
            "defensive_reaction": 5,
        }

        self.keywords = [Keyword.boost, Keyword.no_keyword]
        self.keyword_ratios = {"boost": 80, "no_keyword": 20}

        self.card_classes = [PlayerClass.generic, PlayerClass.mechanologist]
        self.card_class_ratios = {"generic": 20, "mechanologist": 80}

        self.pitch_ratios = {
            CardColor.red: 35,
            CardColor.yellow: 15,
            CardColor.blue: 40,
        }

        self.n_weapons = 1
        self.weapon_physical = np.random.randint(1, 7)
        self.weapon_arcane = 0
        self.go_again_chance = 50
        self.weapon_type = WeaponType.pistol


class RunebladeBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 6, "sigma": 2}
        self.card_type_ratios = {
            "non_attack_action": 60,
            "attack_action": 30,
            "attack_reaction": 5,
            "defensive_reaction": 5,
        }

        self.keywords = [Keyword.go_again, Keyword.blood_debt, Keyword.no_keyword]
        self.keyword_ratios = {"go_again": 70, "blood_debt": 0, "no_keyword": 30}

        self.arcane_ratio = 0.8
        self.arcane_parameters = {"mu": 2, "sigma": 3}

        self.pitch_ratios = {
            CardColor.red: 50,
            CardColor.yellow: 10,
            CardColor.blue: 40,
        }

        self.n_weapons = np.random.randint(1, 3)
        self.weapon_physical = np.random.randint(1, 5)
        self.weapon_arcane = np.random.randint(1, 5)
        self.go_again_chance = 50
        self.weapon_type = random.choice(
            [WeaponType.sword, WeaponType.staff, WeaponType.scepter]
        )


class WizardBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 3, "sigma": 3}
        self.card_type_ratios = {
            "non_attack_action": 60,
            "attack_action": 30,
            "attack_reaction": 5,
            "defensive_reaction": 5,
        }

        self.keywords = [Keyword.opt, Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {"opt": 50, "go_again": 30, "no_keyword": 20}

        self.arcane_ratio = 0.8
        self.arcane_parameters = {"mu": 2, "sigma": 1}

        self.pitch_ratios = {
            CardColor.red: 35,
            CardColor.yellow: 20,
            CardColor.blue: 45,
        }
        self.n_weapons = np.random.randint(1, 3)
        self.weapon_physical = np.random.randint(1, 5)
        self.weapon_arcane = np.random.randint(1, 5)
        self.go_again_chance = 50
        self.weapon_type = random.choice([WeaponType.staff, WeaponType.scepter])


class WarriorBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 3.5, "sigma": 2}
        self.card_type_ratios = {
            "non_attack_action": 40,
            "attack_action": 40,
            "attack_reaction": 15,
            "defensive_reaction": 5,
        }

        self.keywords = [Keyword.charge, Keyword.go_again, Keyword.no_keyword]
        self.keyword_ratios = {"charge": 50, "go_again": 30, "no_keyword": 20}

        self.pitch_ratios = {
            CardColor.red: 30,
            CardColor.yellow: 70,
            CardColor.blue: 0,
        }
        self.n_weapons = np.random.randint(1, 3)
        self.weapon_physical = np.random.randint(1, 5)
        self.weapon_arcane = 0
        self.go_again_chance = 50
        self.weapon_type = WeaponType.sword


class GuardianBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 7, "sigma": 2}
        self.card_type_ratios = {
            "non_attack_action": 5,
            "attack_action": 45,
            "attack_reaction": 25,
            "defensive_reaction": 25,
        }

        # self.keywords = [Keyword.dominate, Keyword.no_keyword]
        # self.keyword_ratios = {"dominate": 50, "no_keyword": 50}
        self.keywords = [Keyword.go_again, Keyword.combo]
        self.keyword_ratios = {"go_again": 100, "combo": 0}

        self.pitch_ratios = {
            CardColor.red: 0,
            CardColor.yellow: 50,
            CardColor.blue: 50,
        }
        self.n_weapons = 1
        self.weapon_physical = np.random.randint(7, 12)
        self.weapon_arcane = 0
        self.go_again_chance = 1
        self.weapon_type = random.choice([WeaponType.axe, WeaponType.hammer])


class IllusionistBasic(Playstyle):
    def __init__(self):
        super().__init__()
        self.physical_parameters = {"mu": 4, "sigma": 2}

        self.pitch_ratios = {
            CardColor.red: 25,
            CardColor.yellow: 25,
            CardColor.blue: 50,
        }

        self.n_weapons = 2
        self.weapon_physical = np.random.randint(1, 5)
        self.weapon_arcane = 0
        self.go_again_chance = 0.7
        self.weapon_type = random.choice(
            [WeaponType.aura, WeaponType.staff, WeaponType.scepter]
        )
