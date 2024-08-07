#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:20:01 2024

@author: lukasgartmair
"""


class Modifiers:
    def __init__(self):
        self.modifier_dict = {"dominate": False, "intimidate": False}

    def reset(self):
        self.modifier_dict = {"dominate": False, "intimidate": False}
