#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:56:46 2024

@author: lukasgartmair
"""
import itertools
import numpy as np

VALUE_MAX_PLACEHOLDER = 100


class Pitch:
    def __init__(self, enemy):
        self.enemy = enemy

    def get_combinations(self, array, current_index):
        combinations = []
        array_copy = array.copy()
        # print(array_copy)
        if len(array_copy) >= 2:
            array_copy.pop(current_index)
            for i in range(self.enemy.intellect):
                if i != current_index:
                    combos = itertools.combinations(array_copy, i)
                    for c in combos:
                        combinations.append(c)

        return combinations

    def determine_pitch_combination(self, cost_to_pay, pitch_combinations):
        number_of_cards_used = self.enemy.intellect
        diff_to_cost = cost_to_pay
        physical_wasted = VALUE_MAX_PLACEHOLDER
        defense_wasted = VALUE_MAX_PLACEHOLDER
        best_pitch = []
        for k, v in pitch_combinations.items():
            number_of_cards_used_temp = len(k)
            diff_to_cost_temp = cost_to_pay - v
            physical_cost_ratio_wasted_temp = np.sum(
                [ki.physical for ki in k]
            ) - np.sum([ki.cost for ki in k])
            defense_wasted_temp = np.sum([ki.defense for ki in k])

            if diff_to_cost_temp <= 0:
                if (
                    abs(diff_to_cost_temp) < diff_to_cost
                    and number_of_cards_used_temp < number_of_cards_used
                ):
                    diff_to_cost = diff_to_cost_temp
                    number_of_cards_used = number_of_cards_used_temp
                    best_pitch = k

        return best_pitch
