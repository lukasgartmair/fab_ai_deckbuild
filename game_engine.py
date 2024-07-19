#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:06:24 2023

@author: lukasgartmair
"""

from enum import Enum

class GameState(Enum):
    PLAYING = 0
    ENDED = 1
    
class GameEngine:

    player1 = None
    enemy = None
    state = None

    def __init__(self):
        self.state = GameState.PLAYING

    def check_win_condition(self):

        self.state = GameState.ENDED