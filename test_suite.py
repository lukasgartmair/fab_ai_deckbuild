#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:13:25 2023

@author: lukasgartmair
"""

import unittest
from engine import GameEngine, GameStateMachine
import numpy as np
from enemy import Stance
import random
from modifiers import Modifiers

n_runs = 2
n_turns = 5
n_iterations = 4


class TestMethods(unittest.TestCase):
    def setUp(self):
        pass
        # self.mod

        #             self.modifiers.modifier_dict[check_box.name] = True
        #         else:
        #             self.modifiers.modifier_dict[check_box.name] = False

    # def test_deckbuilding(self):

    #     for i in range(100):
    #         self.engine = GameEngine()
    #         print(self.engine.enemy.player_class)

    def test_test(self):
        pass

    def test_gameplay(self):
        self.engine = GameEngine()

        for n in range(n_runs):
            if n != 0:
                self.engine.advance_level()

            if self.engine.state_machine.current_state == GameStateMachine.starting:
                self.engine.state_machine.start_game()

            print(self.engine.level_manager.current_level)

            print(self.engine.state_machine.current_state)
            while self.engine.state_machine.current_state == GameStateMachine.playing:
                print("--------------------")
                print("TURN")
                print(self.engine.level_manager.turn_index)

                if self.engine.enemy.stance == Stance.defend:
                    for j in range(random.randint(1, n_iterations + 1)):
                        print("MOVE")
                        print(self.engine.level_manager.move_index)

                        pyhsical = np.random.randint(0, 6)
                        arcane = np.random.randint(0, 3)
                        self.engine.attack.set_values(
                            inp_box=None, physical=pyhsical, arcane=arcane
                        )
                        self.engine.play(self.engine.attack)

                        self.engine.attack.reset()

                        print("enemy life:")
                        print(self.engine.enemy.life)
                        print()

                        self.engine.check_win_condition()
                        if (
                            self.engine.state_machine.current_state
                            == GameStateMachine.ended
                        ):
                            break
                        else:
                            continue  # only executed if the inner loop did NOT break
                        break  # only executed if the inner loop DID break

                    self.engine.enemy.finish_turn()
                    self.engine.finish_turn()

                elif self.engine.enemy.stance == Stance.attack:
                    print("MOVE")
                    print(self.engine.level_manager.move_index)

                    for j in range(n_iterations):
                        if self.engine.enemy.further_attack_possible:
                            self.engine.play()

                            print("enemy life:")
                            print(self.engine.enemy.life)

                            self.engine.check_win_condition()
                            if (
                                self.engine.state_machine.current_state
                                == GameStateMachine.ended
                            ):
                                break

                        else:
                            continue  # only executed if the inner loop did NOT break
                        break  # only executed if the inner loop DID break

                    self.engine.enemy.finish_turn()
                    self.engine.finish_turn()

        self.engine.analyzer.analyze_game_data()


if __name__ == "__main__":
    unittest.main()
