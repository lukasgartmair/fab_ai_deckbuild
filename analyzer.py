#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 16:20:37 2024

@author: lukasgartmair
"""

import pprint
import copy
import dill


class GlobalAnalyzer:
    def __init__(self, engine):
        self.engine = engine
        self.data = {}

    def write_move_data(self):
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

        if (
            self.engine.level_manager.move_index
            not in self.data[self.engine.level_manager.current_level][
                self.engine.level_manager.turn_index
            ]
        ):
            self.data[self.engine.level_manager.current_level][
                self.engine.level_manager.turn_index
            ][self.engine.level_manager.move_index] = {}

        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ][self.engine.level_manager.move_index]["level_manager"] = copy.deepcopy(
            self.engine.level_manager
        )

        self.data[self.engine.level_manager.current_level][
            self.engine.level_manager.turn_index
        ][self.engine.level_manager.move_index]["life_counter"] = copy.copy(
            self.engine.enemy.life_counter
        )

        # print("here")
        # d = {'x':self.engine}
        # print(dill.detect.baditems(d))

        # self.data[self.engine.level_manager.current_level][
        #     self.engine.level_manager.turn_index
        # ][self.engine.level_manager.move_index]["enemy"] = copy.deepcopy(self.engine.enemy.arsenal)

    def analyze_game_data(self):
        print("GAME ANALYSIS")
        print("------------------")
        print()
        # for k, v in self.data.items():
        #     print("current_level")
        #     print(k)
        #     print("enemy")
        #     print(str(v["enemy"].player_class.name) + " " + str(v["enemy"].name))
        # pprint.pprint(self.data)

        print(self.data[1][1][1]["level_manager"].turn_index)
        print(self.data[1][2][1]["level_manager"].turn_index)

        print(self.data[1][1][1]["life_counter"].life_counter.life)

        print(self.data[1][2][1]["life_counter"].life_counter.life)
