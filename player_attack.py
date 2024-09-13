#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:19:28 2024

@author: lukasgartmair
"""

from damage import Damage, DamageType


class PlayerAttack:
    def __init__(self):
        self.physical = Damage(damage_type=DamageType.physical)
        self.arcane = Damage(damage_type=DamageType.arcane)

    def reset(self):
        self.physical = Damage(damage_type=DamageType.physical)
        self.arcane = Damage(damage_type=DamageType.arcane)

    def set_value_physical(self, value=None):
        if value is not None:
            self.physical.set_step(int(value))

    def set_value_arcane(self, value=None):
        if value is not None:
            self.arcane.set_step(int(value))
