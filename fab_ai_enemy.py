#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:55:49 2024

@author: lukasgartmair
"""

import itertools
from card_and_deck import Deck
import numpy as np         

VALUE_MAX_PLACEHOLDER = 100            

class Enemy:
    def __init__(self):
        self.name = "ai_enemy"
        self.intellect = 4
        self.life = 20
        self.hand = []
        self.original_deck = Deck()
        self.deck = self.original_deck.cards
        self.graveyard = []
        self.banished_zone = []
        self.arsenal = []
        self.weapon_zone_1 = []
        self.weapon_zone_2 = []
        
    def get_hand(self):
        for c in self.hand:
            print(str(c))
            
        return self.hand
        
    def draw(self):
        self.hand = self.deck[:self.intellect-len(self.get_hand())]
        del self.deck[:self.intellect-len(self.get_hand())]
        
    def get_combinations(self, array, current_index):
        combinations = []
        array_copy = array.copy()
        array_copy.pop(current_index)
        for i in range(self.intellect):
            if i != current_index:
                combos = itertools.combinations(array_copy,i)
                for c in combos:
                    combinations.append(c)
        return combinations
        
    def determine_pitch_combination(self, cost_to_pay, pitch_combinations):
        
        number_of_cards_used = self.intellect
        diff_to_cost = cost_to_pay
        power_wasted = VALUE_MAX_PLACEHOLDER
        defense_wasted = VALUE_MAX_PLACEHOLDER
        best_pitch = []
        for k,v in pitch_combinations.items():
            # print([ki.name for ki in k])
            # print(v)
            number_of_cards_used_temp = len(k)
            diff_to_cost_temp = cost_to_pay-v
            power_cost_ratio_wasted_temp = np.sum([ki.power for ki in k]) - np.sum([ki.cost for ki in k])
            defense_wasted_temp =np.sum([ki.defense for ki in k])
            
            if diff_to_cost_temp <= 0:
                if abs(diff_to_cost_temp) < diff_to_cost and number_of_cards_used_temp < number_of_cards_used:
                    
                    diff_to_cost = diff_to_cost_temp
                    number_of_cards_used = number_of_cards_used_temp
                    best_pitch = k
        
        return best_pitch
        
    def calc_possible_attacks(self):

        plays = []
        pitch = []
        
        max_damage_output = 0
        number_of_cards_to_pitch = VALUE_MAX_PLACEHOLDER
        power_minus_cost = 0
        best_play = []
        
        virtual_hand = self.hand.copy()

        
        for i,current_card in enumerate((virtual_hand)):
            cards_to_pitch = []
            print("---> card number {}, {}".format(i, current_card.name))
            print()
            
            damage_output = current_card.power
            possible_cards_to_pitch = self.get_combinations(virtual_hand, i)

            pitch_combinations = {}
            for j,pi in enumerate(possible_cards_to_pitch):
                pitch_total = 0
                for p in pi:
                    # print(p.name)
                    # print(p.pitch)
                    pitch_total += p.pitch
                
                pitch_combinations[pi] = pitch_total
                # print("total pitch {}".format(pitch_total))
                # print("-----")
                
            if current_card.cost > 0:
                cards_to_pitch = self.determine_pitch_combination(current_card.cost, pitch_combinations)
                if len(cards_to_pitch) == 0:
                    print("no pitch possible")
                    continue
                
            print("")
            print(current_card.name)
            print(current_card.cost)
            print("best pitch")
            if current_card.cost > 0:
                for c in cards_to_pitch:
                    print(c.name)
                    print(c.pitch)
            else:
                print("no pitch neccessary")
            
            if current_card.power >= max_damage_output and (current_card.power-current_card.cost) >= power_minus_cost  and len(cards_to_pitch) <= number_of_cards_to_pitch:
                best_play = current_card
                max_damage_output = current_card.power
                power_minus_cost = current_card.power - current_card.cost
                number_of_cards_to_pitch = len(cards_to_pitch)
                pitch.append(cards_to_pitch)
    
        print("")
        print("best play")
        print(best_play)
                
        
        
        
        
        