#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 15:06:49 2024

@author: lukasgartmair
"""


class Boost:
    def __init__(self):
        self.activated = False
        self.failed = False
        self.counter = 0

    def increase_counter(self):
        self.counter += 1

    def move_reset(self):
        self.activated = False
        self.failed = False

    def turn_reset(self):
        self.activated = False
        self.failed = False
        self.counter = 0

    def fail(self):
        self.failed = True

    def activation(self):
        self.activated = True
        self.increase_counter()
