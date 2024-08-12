#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:21:39 2024

@author: lukasgartmair
"""
import pygame


class LevelManager:
    def __init__(self, level=1):
        self.current_level = level

    def advance_level(self):
        self.current_level += 1
