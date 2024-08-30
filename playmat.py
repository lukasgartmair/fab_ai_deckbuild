#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:57:44 2024

@author: lukasgartmair
"""

from settings import (
    playmat_grid as grid,
    grid_width_playmat,
    grid_height_playmat,
    card_width,
    card_height,
)
import types


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Playmat:
    def __init__(self):
        self.field_text_offset_x = card_width / 7
        self.field_text_offset_y = card_height / 2.5

        self.positions = types.SimpleNamespace()
        self.positions.enemy = Position(
            grid.left_point(grid_width_playmat // 2 - 1),
            grid.top_point(grid_height_playmat // 2 - 1),
        )
        self.positions.arsenal = Position(
            grid.left_point(grid_width_playmat // 2 - 1),
            grid.top_point(grid_height_playmat - 5),
        )

        self.positions.pitch = Position(
            grid.left_point(grid_width_playmat // 2 + 4),
            grid.top_point(grid_height_playmat // 2 - 1),
        )
