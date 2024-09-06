#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:17:12 2024

@author: lukasgartmair
"""

from enemy import Enemy
from playstyle import PlayerClass


class Ranger(Enemy):
    def __init__(self, player_class=PlayerClass.ranger):
        super().__init__(player_class=PlayerClass.ranger)
