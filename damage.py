#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 12:02:42 2024

@author: lukasgartmair
"""

from enum import Enum
import block


class DamageType(Enum):
    physical = 0
    arcane = 1


class Damage:
    def __init__(self, damage_type=DamageType.physical):
        self.damage_steps = {}
        self.blocked_with = {}
        self.damage_played_out = {}
        self.block_played_out = {}
        self.arcane_block_pitches = {}
        self.damage_type = damage_type
        self.index = -1

    def increase_index(self):
        self.index += 1

    def init_next_step(self):
        self.increase_index()
        self.damage_steps[self.index] = None
        self.blocked_with[self.index] = None
        self.arcane_block_pitches[self.index] = None
        self.block_played_out[self.index] = False

    def set_step(self, value):

        self.init_next_step()
        self.damage_steps[self.index] = value
        self.damage_played_out[self.index] = True
        print("setting step")
        print(self.damage_steps[self.index])

    def set_block(self, blocking_cards, arcane_pitch=None):
        if self.blocked_with[self.index] is None:
            self.blocked_with[self.index] = []
        self.blocked_with[self.index] += blocking_cards
        self.arcane_block_pitches[self.index] = arcane_pitch
        self.block_played_out[self.index] = True

    def get_latest_step_value(self):
        if self.get_length() > 0:
            return self.damage_steps[self.index]
        else:
            return None

    def get_latest_block_cards(self):
        print(self.get_length())
        if self.get_length() > 0:
            return self.blocked_with[self.index]

    def get_latest_block_value(self):
        print(self.get_length())
        if self.get_length() > 0:
            if self.blocked_with[self.index] is not None:
                if self.damage_type == DamageType.physical:
                    if self.blocked_with[self.index] is not None:
                        sum_block = sum(
                            [p.defense for p in self.blocked_with[self.index]]
                        )
                        print(sum_block)
                        return sum_block if sum_block > 0 else None
                    else:
                        return None
            elif self.damage_type == DamageType.arcane:
                if self.arcane_block_pitches[self.index] is not None:
                    sum_block = sum(
                        [p.pitch for p in self.arcane_block_pitches[self.index]]
                    )
                    print(sum_block)
                    return sum_block if sum_block > 0 else None
                else:
                    return None
        else:
            return None

    def get_latest_step_blocked(self):
        if self.get_length() > 0:
            return self.block_played_out[self.index]
        else:
            return None

    def is_empty(self):
        return True if self.get_length() == 0 else False

    def get_length(self):
        return len(self.damage_steps)

    def has_to_be_defended(self):
        if self.get_length() == 0:
            return None
        else:
            return (
                True
                if (
                    self.block_played_out[self.index] == False
                    and self.get_latest_step_value() is not None
                )
                else False
            )

    def still_has_to_be_defended_with_reaction(self):
        if self.get_length() == 0:
            return None
        elif self.damage_type == DamageType.arcane:
            return None
        else:
            return block.check_defensive_reaction_trigger(
                self.get_latest_step_value(), self.get_latest_block_cards()
            )
