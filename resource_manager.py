#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:04:48 2024

@author: lukasgartmair
"""


class ResourceManager:
    def __init__(self):
        self.floating_resources = 0

    def reset(self):
        self.floating_resources = 0

    def pitch_floating_resources(self, amount):
        self.floating_resources += amount

    def use_floating_resources(self, amount):
        print((self.floating_resources - amount))
        if (self.floating_resources - amount) < 0:
            raise Exception("Not enough resources")
        else:
            self.floating_resources -= amount
