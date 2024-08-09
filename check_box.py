#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:28:33 2024

@author: lukasgartmair
"""

import PygameUtils as pu


class CheckBox:
    def __init__(self, name, y=180):
        self.name = name
        self.cb = pu.checkbox(
            "black", 400, y, 25, 25, font="z003", text=name, outline=3
        )

    def reset(self):
        if self.cb.isChecked() == True:
            self.cb.convert()

    def check_activation(self):
        if self.cb.isChecked() == True:
            self.cb.convert()
        elif self.cb.isChecked() == False:
            self.cb.convert()
