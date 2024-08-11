#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:07:57 2023

@author: lukasgartmair
"""

from title_scene import TitleScene
from game_scene import GameScene
from end_scene import EndScene


def get_title_scene(*kargs):
    return TitleScene(*kargs)


def get_game_scene(*kargs):
    return GameScene(*kargs)


def get_end_scene(*kargs):
    return EndScene(*kargs)
