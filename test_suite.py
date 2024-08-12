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
from attack import Attack

n_iterations = 10

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.attack = Attack()
        # self.mod
        
        #             self.modifiers.modifier_dict[check_box.name] = True
        #         else:
        #             self.modifiers.modifier_dict[check_box.name] = False
        
    def test_gameplay(self):
        
        self.engine.state_machine.start_game()
        
        for i in range(n_iterations):
            print(i)

            if self.engine.enemy.stance == Stance.defend:
                print("defense test")
                pyhsical = np.random.randint(0,25)
                arcane = np.random.randint(0,25)
                self.attack.set_values_explicitly(physical=pyhsical, arcane=arcane)
                
                print(self.engine.enemy.check_if_further_defense_possible() == True)
                for i in range (100):
                    if self.engine.enemy.check_if_further_defense_possible() == True:
                        self.engine.play(self.attack)
                    else:

                        self.engine.enemy.finish_phase()
                        break
    
                self.attack.reset()
            elif self.engine.enemy.stance == Stance.attack:
                print("attack test")
                for i in range (100):
                    if self.engine.enemy.check_if_further_attack_possible() == True:
                        self.engine.play()
                    else:
                        self.engine.enemy.finish_phase()
                        break
            
        self.engine.check_win_condition()
        
        print(self.engine.state_machine.current_state)

        # self.assertEqual(result[i], solution[i])



if __name__ == "__main__":
    unittest.main()
