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

    def set_values(self, inp_box=None):
        if inp_box is not None:
            if inp_box.box_type == "physical":
                self.physical.set_step(inp_box.send_input())
                self.arcane.set_step(None)

            elif inp_box.box_type == "arcane":
                self.physical.set_step(None)
                self.arcane.set_step(inp_box.send_input())
