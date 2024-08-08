#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:45:02 2024

@author: lukasgartmair
"""

from enum import Enum


class EquipmentType(Enum):
    head = 0
    chest = 1
    arms = 2
    legs = 3


class Keyword(Enum):
    battleworn = 0
    blade_break = 1
    cloaked = 2
    none = 3


class EquipmentPiece:
    def __init__(self, equipment_type):
        self.equipment_type = equipment_type
        self.defensive_value = 1
        self.arcane_barrier = 2
        self.keywords = []
        self.destroyed = False


class EquipmentSuite:
    def __init__(self):
        self.head = EquipmentPiece(EquipmentType.head)
        self.chest = EquipmentPiece(EquipmentType.chest)
        self.arms = EquipmentPiece(EquipmentType.arms)
        self.legs = EquipmentPiece(EquipmentType.legs)

    def get_equipment_pieces(self):
        return [self.head, self.chest, self.arms, self.legs]
