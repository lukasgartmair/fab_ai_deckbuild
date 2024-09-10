#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:19:28 2024

@author: lukasgartmair
"""

from enum import Enum


class DamageType(Enum):
    physical = 0
    arcane = 1


class Damage:
    def __init__(self, damage_type=DamageType.physical):
        self.damage_steps = {}
        self.blocked_with = {}
        self.damage_type = damage_type
        self.index = -1

    def increase_index(self):
        self.index += 1

    def init_next_step(self):
        self.increase_index()
        self.damage_steps[self.index] = None
        self.blocked_with[self.index] = None

    def set_step(self, value):
        self.init_next_step()
        self.damage_steps[self.index] = value
        print("setting step")
        print(self.damage_steps[self.index])

    def set_block(self, value):
        self.blocked_with[self.index] = value

    def get_latest_step_value(self):
        max_key = 0
        if self.is_empty() == False:
            max_key = max(self.damage_steps.keys())
            return self.damage_steps[max_key]
        else:
            return None

    def is_empty(self):
        return True if self.get_length() == 0 else False

    def get_length(self):
        return len(self.damage_steps)

    def has_to_be_defended(self):
        return True if self.get_latest_step_value() is not None else False


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
