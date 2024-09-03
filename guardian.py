#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:07:01 2024

@author: lukasgartmair
"""

from enemy import Enemy
from playstyle import PlayerClass
from utils import n_chance


class Guardian(Enemy):
    def __init__(self, player_class=PlayerClass.guardian):
        super().__init__(player_class=PlayerClass.guardian)
