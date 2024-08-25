#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 16:20:37 2024

@author: lukasgartmair
"""


class GlobalAnalyzer:
    def __init__(self, engine):
        self.engine = engine
        self.data = {}

    def write_enemy_turn_data(self):
        if self.engine.level_manager.current_level not in self.data:
            self.data[self.engine.level_manager.current_level] = {}

            self.data[self.engine.level_manager.current_level][
                "enemy"
            ] = self.engine.enemy

        if (
            self.engine.level_manager.turn_index
            not in self.data[self.engine.level_manager.current_level]
        ):
            self.data[self.engine.level_manager.current_level][
                self.engine.level_manager.turn_index
            ] = {}

        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["stance"] = self.engine.enemy.stance.name
        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["life"] = self.engine.enemy.life
        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["hand"] = self.engine.enemy.hand
        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["arsenal"] = self.engine.enemy.arsenal
        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["graveyard"] = self.engine.enemy.graveyard
        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ]["banished_zone"] = self.engine.enemy.banished_zone

    def analyze_game_data(self):
        print("GAME ANALYSIS")
        print("------------------")
        for k, v in self.data.items():
            print("current_level")
            print(k)
            print("enemy")
            print(str(v["enemy"].player_class.name) + " " + str(v["enemy"].name))
            print("# enemy turns played")
            print(len(v))
