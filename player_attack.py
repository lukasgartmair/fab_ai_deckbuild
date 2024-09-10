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
        self.damage_played_out = {}
        self.block_played_out = {}
        self.damage_type = damage_type
        self.index = -1

    def increase_index(self):
        self.index += 1

    def init_next_step(self):
        self.increase_index()
        self.damage_steps[self.index] = None
        self.blocked_with[self.index] = None
        self.damage_played_out[self.index - 1] = False
        self.block_played_out[self.index - 1] = False

    def set_step(self, value):
        if self.index not in self.damage_steps:
            self.init_next_step()
        self.damage_steps[self.index] = value
        self.damage_played_out[self.index] = True
        print("setting step")
        print(self.damage_steps[self.index])
        self.init_next_step()

    def set_block(self, value):
        self.blocked_with[self.index - 1] = value
        self.block_played_out[self.index - 1] = True

    def get_latest_step_value(self):
        if self.index > 0:
            return self.damage_steps[self.index - 1]
        elif self.index == 0:
            return self.damage_steps[self.index]

    def get_latest_virtual_step_value(self):
        if self.index >= 0:
            return self.damage_steps[self.index]

    def is_empty(self):
        return True if self.get_length() == 0 else False

    def get_length(self):
        return len(self.damage_steps)

    def has_to_be_defended(self):
        return True if self.block_played_out[self.index - 1] == False else False


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
