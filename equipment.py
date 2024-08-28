#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:45:02 2024

@author: lukasgartmair
"""

from enum import Enum
from card import Card
from playstyle import CardType
import random

arcane_barriers = [0] * 3 + [1] * 2 + [2]


class EquipmentType(Enum):
    head = 0
    chest = 1
    arms = 2
    legs = 3


class EquipmentKeyword(Enum):
    battleworn = 0
    blade_break = 1
    cloaked = 2


class EquipmentPiece(Card):
    def __init__(self, equipment_type):
        super().__init__()
        self.equipment_type = equipment_type
        self.arcane_barrier = random.choice(arcane_barriers)
        self.keywords = [EquipmentKeyword.blade_break]
        self.destroyed = False
        self.card_class = self.equipment_type
        self.card_type = CardType.equipment


class EquipmentSuite:
    def __init__(self):
        self.head = EquipmentPiece(EquipmentType.head)
        self.chest = EquipmentPiece(EquipmentType.chest)
        self.arms = EquipmentPiece(EquipmentType.arms)
        self.legs = EquipmentPiece(EquipmentType.legs)

    def get_pieces(self):
        return [self.head, self.chest, self.arms, self.legs]
