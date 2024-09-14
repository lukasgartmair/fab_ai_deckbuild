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
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class Playmat:
    def __init__(self):
        self.field_text_offset_x = card_width / 7
        self.field_text_offset_y = card_height / 2.5

        self.positions = types.SimpleNamespace()

        self.positions.enemy = Position(
            "Enemy",
            grid.left_point(grid_width_playmat // 2 - 1),
            grid.top_point(grid_height_playmat // 2 - 1),
        )
        self.positions.weapon_0 = Position(
            "Weapon",
            grid.left_point(grid_width_playmat // 2 - 3),
            grid.top_point(grid_height_playmat // 2 - 1),
        )

        self.positions.weapon_1 = Position(
            "Weapon",
            grid.left_point(grid_width_playmat // 2 + 1),
            grid.top_point(grid_height_playmat // 2 - 1),
        )
        self.positions.arsenal = Position(
            "Arsenal",
            grid.left_point(grid_width_playmat // 2 - 1),
            grid.top_point(grid_height_playmat - 5),
        )

        self.positions.pitch = Position(
            "Pitch",
            grid.left_point(grid_width_playmat // 2 + 4),
            grid.top_point(grid_height_playmat // 2 - 1),
        )

        self.positions.deck = Position(
            "Deck",
            grid.left_point(grid_width_playmat // 2 + 6),
            grid.top_point(grid_height_playmat // 2 - 1),
        )

        self.positions.graveyard = Position(
            "Graveyard",
            grid.left_point(grid_width_playmat // 2 + 6),
            grid.top_point(3),
        )

        self.positions.banished_zone = Position(
            "Banished",
            grid.left_point(grid_width_playmat // 2 + 6),
            grid.top_point(grid_height_playmat - 5),
        )

        self.positions.combat_chain = Position(
            "Combat Chain",
            grid.left_point(3),
            grid.top_point(2),
        )

        self.positions.head = Position(
            "Head",
            grid.left_point(1),
            grid.top_point(3),
        )

        self.positions.chest = Position(
            "Chest",
            grid.left_point(1),
            grid.top_point(grid_height_playmat // 2 - 1),
        )

        self.positions.arms = Position(
            "Arms",
            grid.left_point(3),
            grid.top_point(grid_height_playmat // 2 - 1),
        )

        self.positions.legs = Position(
            "Legs",
            grid.left_point(1),
            grid.top_point(grid_height_playmat - 5),
        )

        self.positions.stance = Position(
            "Stance",
            grid.left_point(1),
            grid.top_point(grid_height_playmat - 5),
        )

        self.positions.inputs = Position(
            "Inputs", grid.left_point(4), grid.top_point(grid_height_playmat - 5)
        )

        self.positions.check_boxes = Position(
            "Check Boxes", grid.left_point(11), grid.top_point(grid_height_playmat - 5)
        )

        self.positions.enemy_message = Position(
            "Enemy Message", grid.left_point(4), grid.top_point(grid_height_playmat - 4)
        )

    def get_horizontal_spacing(self):
        return grid.width_gap(0, 1)

    def get_vertical_spacing(self):
        return grid.height_gap(0, 1)
