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


def shift_list(a):
    x = a.pop()
    a.insert(0, x)
    return a


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

        self.floating_resources = 0

        self.pitched_cards = []
        self.played_cards = []

        self.combat_chain_iterator = 0

        self.combat_chain = {}
        self.pitch = []

    def finish_phase(self):
        self.floating_resources = 0

        for card in self.played_cards:
            self.graveyard.append(card)

        for p in self.pitched_cards:
            self.deck.append(p)

        self.played_cards = []
        self.pitched_cards = []

        self.combat_chain = {}

        self.combat_chain_iterator = 0

        if self.stance == Stance.attack:
            self.combat_chain = []
            self.pitch = []
            self.draw()

        if self.stance == Stance.defend:
            self.stance = Stance.attack
            self.calc_combat_chain()
            print("combat_chain")
            print(self.combat_chain)
        else:
            self.stance = Stance.defend

    def check_if_further_defense_possible(self):
        if len(self.hand) == 0:
            return False
        else:
            return True

    def check_if_further_attack_possible(self):
        print(self.combat_chain)
        attack_possible = True
        if (
            len(self.combat_chain) == 0
            or self.combat_chain_iterator > len(self.combat_chain)
            or len(self.hand) == 0
        ):
            attack_possible = False
        return attack_possible

    def draw(self):
        print("enemy is drawing")
        if len(self.deck) > 0:
            n_cards_to_draw = self.intellect - len(self.hand)
            if n_cards_to_draw > 0:
                if len(self.deck) < n_cards_to_draw:
                    n_cards_to_draw = len(self.deck)

                drawn_cards = self.deck[:n_cards_to_draw].copy()
                if len(drawn_cards) > 0:
                    for dc in drawn_cards:
                        self.hand.append(dc)
                    self.deck = self.deck[n_cards_to_draw:]

        else:
            print("can't draw anymore, deck fatigued")

    def calc_combat_chain(self):
        combat_chain_index = 0

        virtual_hand = self.hand.copy()
        virtual_hand_tmp = virtual_hand.copy()
        for i in range(len(virtual_hand)):
            if len(virtual_hand_tmp) > 0:
                current_card = virtual_hand_tmp[0]
                possible_cards_to_pitch = self.get_combinations(virtual_hand_tmp, 0)

                pitch_combinations = {}
                for j, pi in enumerate(possible_cards_to_pitch):
                    pitch_total = 0
                    for p in pi:
                        pitch_total += p.pitch

                    pitch_combinations[pi] = pitch_total

                if current_card.cost > 0:
                    cards_to_pitch = self.determine_pitch_combination(
                        current_card.cost, pitch_combinations
                    )

                    if len(cards_to_pitch) == 0:
                        print("no pitch possible")
                        virtual_hand = shift_list(virtual_hand_tmp)
                        continue
                    else:
                        self.combat_chain[combat_chain_index] = {
                            "attack": current_card,
                            "pitch": cards_to_pitch,
                        }
                        combat_chain_index += 1

                        virtual_hand_tmp.remove(current_card)
                        for p in cards_to_pitch:
                            virtual_hand_tmp.remove(p)
                else:
                    self.combat_chain[combat_chain_index] = {
                        "attack": current_card,
                        "pitch": [],
                    }
                    combat_chain_index += 1

                    virtual_hand_tmp.remove(current_card)

            else:
                break

    def attack(self):
        print("enemy attacking")

        print("enemy attacks with")
        if (
            len(self.combat_chain) > 0
            and self.combat_chain_iterator in self.combat_chain
        ):
            c = self.combat_chain[self.combat_chain_iterator]["attack"]
            print(c.name)
            print("power: {}".format(c.power))
            print("cost: {}".format(c.cost))
            print("pitch")
            pitch = self.combat_chain[self.combat_chain_iterator]["pitch"]
            if len(pitch) > 0:
                for p in pitch:
                    print(str(p))

            for p in pitch:
                self.pitched_cards.append(p)

                self.floating_resources += p.pitch

            self.played_cards.append(c)

            for p in self.played_cards:
                if p in self.hand:
                    self.hand.remove(p)

            for p in self.pitched_cards:
                if p in self.hand:
                    self.hand.remove(p)

            self.floating_resources -= c.cost

            self.combat_chain_iterator += 1

    def placeholder_block(self):
        if len(self.hand) > 0:
            return self.hand[0]
        else:
            return None

    def more_elaborate_block(self, player_attack_value):
        
        if player_attack_value is not None:
            match player_attack_value:
                case player_attack_value if 0 <= player_attack_value < 3:
                    print("attack not blocked at all")
                    return []
                case player_attack_value if 3 <= player_attack_value < 7:
                    print("attack blocked with {} cards".format(len(self.hand[:1])))
                    return self.hand[:1]
                case player_attack_value if 7 <= player_attack_value < 10:
                    print("attack blocked with {} cards".format(len(self.hand[:2])))
                    return self.hand[:2]
                case player_attack_value if 11 <= player_attack_value < 14:
                    print("attack blocked with {} cards".format(len(self.hand[:3])))
                    return self.hand[:3]
                case player_attack_value if 14 <= player_attack_value:
                    print("attack blocked with {} cards".format(len(self.hand)))
                    return self.hand[:]
                case _:
                    return []


    def get_block(self, player_attack_value):
        
        return self.more_elaborate_block(player_attack_value)

    def defend(self, player_attack_value):
        print("enemy defending")
        if player_attack_value and len(self.hand) > 0:
            blocking_cards = self.get_block(player_attack_value)

            if len(blocking_cards) > 0:
                for bc in blocking_cards:
                    print(bc)
                    self.played_cards.append(bc)
                    print("enemy defends with")
                    print(bc.name)
                    print("defense: {}".format(bc.defense))
                    self.hand.remove(bc)


    def get_combinations(self, array, current_index):
        combinations = []
        array_copy = array.copy()
        print(array_copy)
        if len(array_copy) >= 2:
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

    # def calc_possible_attacks(self):
    #     pitch = []

    #     max_damage_output = 0
    #     number_of_cards_to_pitch = VALUE_MAX_PLACEHOLDER
    #     power_minus_cost = 0
    #     combat_chain = []

    #     virtual_hand = self.hand.copy()

    #     for i, current_card in enumerate((virtual_hand)):
    #         cards_to_pitch = []
    #         print("---> card number {}, {}".format(i, current_card.name))
    #         print()

    #         possible_cards_to_pitch = self.get_combinations(virtual_hand, i)

    #         pitch_combinations = {}
    #         for j, pi in enumerate(possible_cards_to_pitch):
    #             pitch_total = 0
    #             for p in pi:
    #                 # print(p.name)
    #                 # print(p.pitch)
    #                 pitch_total += p.pitch

    #             pitch_combinations[pi] = pitch_total
    #             # print("total pitch {}".format(pitch_total))
    #             # print("-----")

    #         if current_card.cost > 0:
    #             cards_to_pitch = self.determine_pitch_combination(
    #                 current_card.cost, pitch_combinations
    #             )
    #             if len(cards_to_pitch) == 0:
    #                 print("no pitch possible")
    #                 continue

    #         print("")
    #         print(current_card.name)
    #         print(current_card.cost)
    #         print("best pitch")
    #         if current_card.cost > 0:
    #             for c in cards_to_pitch:
    #                 print(c.name)
    #                 print(c.pitch)
    #         else:
    #             print("no pitch neccessary")

    #         if (
    #             current_card.power >= max_damage_output
    #             and (current_card.power - current_card.cost) >= power_minus_cost
    #             and len(cards_to_pitch) <= number_of_cards_to_pitch
    #         ):
    #             combat_chain = [current_card]
    #             max_damage_output = current_card.power
    #             power_minus_cost = current_card.power - current_card.cost
    #             number_of_cards_to_pitch = len(cards_to_pitch)
    #             if len(cards_to_pitch) > 0:
    #                 pitch.append(cards_to_pitch)

    #     print("")
    #     print("best play")
    #     print(combat_chain)
    #     self.combat_chain = combat_chain
    #     self.pitch = pitch


if __name__ == "__main__":
    e = Enemy()
    e.draw()
    e.calc_combat_chain()
