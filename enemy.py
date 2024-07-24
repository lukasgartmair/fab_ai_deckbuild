#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:55:49 2024

@author: lukasgartmair
"""

import numpy as np
import itertools
from deck import Deck
from pile import Pile
from enum import Enum

VALUE_MAX_PLACEHOLDER = 100


class Stance(Enum):
    defend = 0
    attack = 1


class Enemy:
    playKey = None

    def __init__(self, play_key=None):
        self.name = "ai_enemy"
        self.stance = Stance.defend
        self.intellect = 4
        self.life = 20
        self.hand = []
        self.pile = Pile()
        self.play_key = None
        self.original_deck = Deck()
        self.deck = self.original_deck.cards
        self.graveyard = []
        self.banished_zone = []
        self.arsenal = []
        self.weapon_zone_1 = []
        self.weapon_zone_2 = []

        self.pitched_cards = []
        self.played_cards = []

        self.best_play = []
        self.pitch = []

    def finish_phase(self):
        for card in self.played_cards:
            self.graveyard.append(card)
        
        for p in self.pitched_cards:
            for pc in p:
                self.deck.append(p)

        self.played_cards = []
        self.pitched_cards = []

        if self.stance == Stance.attack:
            self.best_play = []
            self.pitch = []
            
        if self.stance == Stance.attack:
            self.draw()
            
    def check_if_further_defense_possible(self):
        if len(self.hand) == 0:
            return False
        else:
            return True

    def check_if_further_attack_possible(self):
        print(self.best_play)
        if len(self.best_play) == 0:
            return False
        else:
            return True

    def draw(self):
        print("deck")
        print(self.deck)
        print("enemy is drawing")
        if len(self.deck) > 0:
            n_cards_to_draw = self.intellect - len(self.hand)
            print("n_cards_to_draw")
            print(n_cards_to_draw)
            print("len deck")
            print(len(self.deck))
            if n_cards_to_draw > 0:
                if len(self.deck) < n_cards_to_draw:
                    n_cards_to_draw = len(self.deck)
                    
                drawn_cards = self.deck[:n_cards_to_draw].copy()
                if len(drawn_cards) > 0:

                    for dc in drawn_cards:
                        print(dc)
                        self.hand.append(dc)
                    self.deck = self.deck[n_cards_to_draw:]
                print(self.hand)
        else:
            print("can't draw anymore, deck fatigued")
            
        print("len deck after draw")
        print(len(self.deck))
        

    def attack(self):
        print("enemy attacking")

        if len(self.best_play) > 0:
            
            print("here")
            print(self.hand)
            self.hand = [
                item
                for item in self.hand
                if item.card_id not in [c.card_id for c in self.best_play]
            ]
            print(self.hand)
        if len(self.pitch) > 0:
            self.hand = [
                item
                for item in self.hand
                if item.card_id not in [c[0].card_id for c in self.pitch]
            ]

        print("enemy attacks with")
        if len(self.best_play) > 0:
            c = self.best_play[0]
            print(c.name)
            print("power: {}".format(c.power))
            print("cost: {}".format(c.cost))
            print("pitch")
            if len(self.pitch) > 0:
                for p in self.pitch:
                    print(str(p[0]))

        self.played_cards += self.best_play
        self.pitched_cards.append(self.pitch)
        
    def get_block(self):
        print(self.hand)
        if len(self.hand) > 0:
            return self.hand[0]
        else:
            return None

    def defend(self):
        print("enemy defending")
        if len(self.hand) > 0:
            
            c = self.get_block()

            print(c)
            self.played_cards.append(c)
            print("enemy defends with")
            print(c.name)
            print("defense: {}".format(c.defense))
            self.hand.remove(c)
            
            


    def get_combinations(self, array, current_index):
        combinations = []
        array_copy = array.copy()
        array_copy.pop(current_index)
        for i in range(self.intellect):
            if i != current_index:
                combos = itertools.combinations(array_copy, i)
                for c in combos:
                    combinations.append(c)
        return combinations

    def determine_pitch_combination(self, cost_to_pay, pitch_combinations):
        number_of_cards_used = self.intellect
        diff_to_cost = cost_to_pay
        power_wasted = VALUE_MAX_PLACEHOLDER
        defense_wasted = VALUE_MAX_PLACEHOLDER
        best_pitch = []
        for k, v in pitch_combinations.items():
            # print([ki.name for ki in k])
            # print(v)
            number_of_cards_used_temp = len(k)
            diff_to_cost_temp = cost_to_pay - v
            power_cost_ratio_wasted_temp = np.sum([ki.power for ki in k]) - np.sum(
                [ki.cost for ki in k]
            )
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

    def calc_possible_attacks(self):
        pitch = []

        max_damage_output = 0
        number_of_cards_to_pitch = VALUE_MAX_PLACEHOLDER
        power_minus_cost = 0
        best_play = []

        virtual_hand = self.hand.copy()

        for i, current_card in enumerate((virtual_hand)):
            cards_to_pitch = []
            print("---> card number {}, {}".format(i, current_card.name))
            print()

            possible_cards_to_pitch = self.get_combinations(virtual_hand, i)

            pitch_combinations = {}
            for j, pi in enumerate(possible_cards_to_pitch):
                pitch_total = 0
                for p in pi:
                    # print(p.name)
                    # print(p.pitch)
                    pitch_total += p.pitch

                pitch_combinations[pi] = pitch_total
                # print("total pitch {}".format(pitch_total))
                # print("-----")

            if current_card.cost > 0:
                cards_to_pitch = self.determine_pitch_combination(
                    current_card.cost, pitch_combinations
                )
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

            if (
                current_card.power >= max_damage_output
                and (current_card.power - current_card.cost) >= power_minus_cost
                and len(cards_to_pitch) <= number_of_cards_to_pitch
            ):
                best_play = [current_card]
                max_damage_output = current_card.power
                power_minus_cost = current_card.power - current_card.cost
                number_of_cards_to_pitch = len(cards_to_pitch)
                if len(cards_to_pitch) > 0:
                    pitch.append(cards_to_pitch)

        print("")
        print("best play")
        print(best_play)
        self.best_play = best_play
        self.pitch = pitch


if __name__ == "__main__":
    e = Enemy()
    e.draw()
    e.calc_possible_attacks()
