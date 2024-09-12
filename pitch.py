#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:56:46 2024

@author: lukasgartmair
"""

# TODO find sweetspot values here
# the current ones are working basically but not well

VALUE_MAX_PLACEHOLDER = 100
a = 0.75
b = 0.25
c = 0.5
d = 0.5


def pitch_formula_offense(diff_to_cost, number_of_cards_used, overpitch):
    print(diff_to_cost)
    print(number_of_cards_used)
    result = (
        abs(diff_to_cost) * a + number_of_cards_used * b
    ) + 1 / number_of_cards_used * a

    return result + 1 if overpitch == True else result


def pitch_formula_arcane_defense(diff_to_cost, number_of_cards_used):
    print(diff_to_cost)
    print(number_of_cards_used)
    return abs(diff_to_cost) * c + number_of_cards_used * d


def determine_offensive_pitch_combination(cost_to_pay, pitch_combinations):
    print("cost_to_pay")
    print(cost_to_pay)
    number_of_cards_used = VALUE_MAX_PLACEHOLDER
    diff_to_cost = cost_to_pay
    best_pitch = []
    pitch_value_calculated = VALUE_MAX_PLACEHOLDER

    for k, v in pitch_combinations.items():
        number_of_cards_used_temp = len(k)
        print(k)
        print(v)
        diff_to_cost_temp = cost_to_pay - v
        underpitch = True if diff_to_cost_temp > 0 else False
        overpitch = True if diff_to_cost_temp < 0 else False
        print(diff_to_cost_temp)

        if underpitch == False:
            pitch_value_calculated_temp = pitch_formula_offense(
                diff_to_cost_temp, number_of_cards_used, overpitch
            )

            if pitch_value_calculated_temp <= pitch_value_calculated:
                diff_to_cost = diff_to_cost_temp
                number_of_cards_used = number_of_cards_used_temp
                pitch_value_calculated = pitch_value_calculated_temp
                best_pitch = k

    return best_pitch


def determine_arcane_defense_pitch_combination(cost_to_pay, pitch_combinations):
    number_of_cards_used = VALUE_MAX_PLACEHOLDER
    diff_to_cost = cost_to_pay
    best_pitch = []
    pitch_value_calculated = VALUE_MAX_PLACEHOLDER

    for k, v in pitch_combinations.items():
        number_of_cards_used_temp = len(k)
        diff_to_cost_temp = cost_to_pay - v
        underpitch = True if diff_to_cost_temp > 0 else False
        if underpitch == False:

            pitch_value_calculated_temp = pitch_formula_arcane_defense(
                diff_to_cost_temp, number_of_cards_used
            )
            if pitch_value_calculated_temp <= pitch_value_calculated:
                diff_to_cost = diff_to_cost_temp
                number_of_cards_used = number_of_cards_used_temp
                pitch_value_calculated = pitch_value_calculated_temp
                best_pitch = k

    return best_pitch
