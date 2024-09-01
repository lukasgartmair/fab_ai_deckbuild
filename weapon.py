#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:59:06 2024

@author: lukasgartmair
"""

from enum import Enum
import numpy as np
import random
import pygame
from playstyle import PlayerClass, CardType
from wonderwords import RandomWord
from settings import CARD_RESOLUTION
from playstyle import Keyword, WeaponType
from utils import n_chance
from card import Card, CardColor, generate_rnd_image, img_to_surfarray
from sound import Sound

r = RandomWord()


def generate_rnd_name():
    r.word()
    rnd_word = r.word(
        word_min_length=5,
        word_max_length=30,
        include_parts_of_speech=["nouns"],
        ends_with="er",
    )
    return rnd_word


class HandOccupation(Enum):
    one_handed = 0
    two_handed = 1


def initialize_weapons(playstyle_obj):
    if playstyle_obj.n_weapons == 1:
        return [Weapon(playstyle_obj, HandOccupation.two_handed, weapon_id=0)]

    elif playstyle_obj.n_weapons == 2:
        return [
            Weapon(playstyle_obj, HandOccupation.one_handed, weapon_id=0),
            Weapon(playstyle_obj, HandOccupation.one_handed, weapon_id=1),
        ]


def get_weapon_sound(weapon):
    match weapon.weapon_type:
        case weapon.weapon_type if weapon.weapon_type == WeaponType.pistol:
            if weapon.weapon_id == 0:
                return Sound.sound_effect.steampunk_pistol
            elif weapon.weapon_id == 1:
                return Sound.sound_effect.pistol
        case weapon.weapon_type if weapon.weapon_type == WeaponType.bow:
            return Sound.sound_effect.bow
        case weapon.weapon_type if weapon.weapon_type == WeaponType.hammer:
            return Sound.sound_effect.hammer
        case weapon.weapon_type if weapon.weapon_type == WeaponType.dagger:
            return Sound.sound_effect.dagger
        case weapon.weapon_type if weapon.weapon_type == WeaponType.aura:
            return Sound.sound_effect.aura
        case weapon.weapon_type if weapon.weapon_type == WeaponType.axe:
            return Sound.sound_effect.axe
        case _:
            return Sound.sound_effect.attack


class Weapon(Card):
    def __init__(self, playstyle_obj, hand_occupation, weapon_id=0):
        super().__init__()

        self.weapon_id = weapon_id

        self.weapon_type = playstyle_obj.weapon_type

        self.sound = get_weapon_sound(self)

        self.name = generate_rnd_name()

        self.image = img_to_surfarray(generate_rnd_image(size=CARD_RESOLUTION))

        self.card_class = self.weapon_type

        self.physical = playstyle_obj.weapon_physical
        self.arcane = playstyle_obj.weapon_arcane

        if n_chance(p=playstyle_obj.go_again_chance):
            self.keywords = [Keyword.go_again]
        else:
            self.keywords = [Keyword.no_keyword]

        power = self.physical + self.arcane
        match power:
            case power if power < 2:
                self.cost = 0
            case power if 2 <= power < 4:
                self.cost = 1
            case power if 4 <= power < 7:
                self.cost = 2
            case power if 7 <= power:
                self.cost = 3

        self.color = CardColor.red
        self.card_type = CardType.weapon

        self.hand_occupation = hand_occupation
