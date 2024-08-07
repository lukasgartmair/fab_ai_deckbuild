#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:19:28 2024

@author: lukasgartmair
"""


class Attack:
    def __init__(self):
        self.physical = None
        self.arcane = None

    def reset(self):
        self.physical = None
        self.arcane = None

    def set_values(self, inp_box):
        if inp_box.box_type == "physical":
            self.physical = inp_box.send_input()
            print("self.physical")
            print(self.physical)
        elif inp_box.box_type == "arcane":
            self.arcane = inp_box.send_input()
            print("self.arcane")
            print(self.arcane)
