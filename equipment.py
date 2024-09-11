#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:45:02 2024

@author: lukasgartmair
"""

from enum import Enum
from card import Card, generate_rnd_image, img_to_surfarray
from playstyle import CardType
import random
from settings import CARD_RESOLUTION
from wonderwords import RandomSentence

# arcane_barriers = [0] * 3 + [1] * 2 + [2]
arcane_barriers = [1] * 2 + [2]

s = RandomSentence()


class EquipmentType(Enum):
    head = 0
    chest = 1
    arms = 2
    legs = 3


class EquipmentKeyword(Enum):
    battleworn = 0
    blade_break = 1
    # cloaked = 2


def generate_rnd_name():
    return " ".join(s.bare_bone_with_adjective().split()[1:-1])


class EquipmentPiece(Card):
    def __init__(self, equipment_type):
        super().__init__(card_resolution=CARD_RESOLUTION)
        self.name = generate_rnd_name()
        self.equipment_type = equipment_type
        self.defense = random.randint(0, 2)
        self.arcane_barrier = random.choice(arcane_barriers)
        self.keywords = [random.choice(list(EquipmentKeyword))]
        self.destroyed = False
        self.is_defending = False
        self.card_class = self.equipment_type
        self.card_type = CardType.equipment
        self.image = img_to_surfarray(generate_rnd_image(size=CARD_RESOLUTION))

    def remove_defense(self, amount=1):
        self.defense -= amount
        if self.defense < 0:
            self.defense = 0

    def destroy(self):
        self.destroyed = True

    def check_destruction(self):
        if self.defense == 0:
            self.destroy()

    def set_defending(self):
        self.is_defending = True

    def finish_defensive_move(self):
        if EquipmentKeyword.blade_break in self.keywords:
            self.destroy()
        elif EquipmentKeyword.battleworn in self.keywords:
            self.remove_defense()
            self.check_destruction()
            if self.destroyed == False:
                self.is_defending = False


class EquipmentSuite:
    def __init__(self):
        self.head = EquipmentPiece(EquipmentType.head)
        self.chest = EquipmentPiece(EquipmentType.chest)
        self.arms = EquipmentPiece(EquipmentType.arms)
        self.legs = EquipmentPiece(EquipmentType.legs)

    def get_current_length(self):
        return len([ep for ep in self.get_all_pieces() if ep.destroyed == False])

    def get_all_pieces(self):
        return [self.head, self.chest, self.arms, self.legs]

    def get_pieces_in_play(self):
        return [ep for ep in self.get_all_pieces() if ep.destroyed == False]

    def get_possible_blocking_pieces_in_play(self):
        return [
            ep
            for ep in self.get_all_pieces()
            if ep.destroyed == False and ep.is_defending == False and ep.defense > 0
        ]

    def get_all_arcane_barriers_in_play(self):
        available_arcane_barriers = [
            ep
            for ep in self.get_all_pieces()
            # TODO can I use the arcane barrier of an equipment used in the current combat chain?
            if ep.destroyed == False
            and ep.is_defending == False
            and ep.arcane_barrier > 0
        ]
        return sorted(
            available_arcane_barriers, key=lambda x: x.arcane_barrier, reverse=False
        )
