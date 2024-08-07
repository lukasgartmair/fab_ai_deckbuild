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
from playstyle import Keyword, PlayerClass, CardType, get_playstyle
from equipment import EquipmentSuite
from weapon import Weapon
import random
from fantasynames.fantasy_identity import FantasyIdentity
from enemy_block import EnemyBlock
from utils import n_chance, shift_list
from ability import Ability

VALUE_MAX_PLACEHOLDER = 100


class Stance(Enum):
    defend = 0
    attack = 1


class Enemy:
    playKey = None

    def __init__(self, play_key=None):
        self.player_class = random.choice(
            [p for p in list(PlayerClass) if p.name != "generic"]
        )
        self.identity = FantasyIdentity(self.player_class)
        self.name = self.identity.name
        self.race = self.identity.race
        self.image = self.identity.image

        self.stance = Stance.defend
        self.intellect = 5
        self.talents = []
        self.life = 20
        self.hand = []
        self.pile = Pile()
        self.play_key = None

        self.playstyle = get_playstyle(self.player_class)
        self.original_deck = Deck(self.player_class, self.playstyle)
        self.deck = self.original_deck.cards

        self.graveyard = []
        self.banished_zone = {}
        self.banished_zone["intimidated_cards"] = []
        self.arsenal = []

        self.weapon_zone_1 = Weapon()
        self.weapon_zone_2 = []

        self.equipment_suite = EquipmentSuite()

        self.further_attack_possible = True
        self.further_defense_possible = True

        self.floating_resources = 0

        self.pitched_cards = []
        self.played_cards = []

        self.combat_chain_iterator = 0

        self.combat_chain = {}
        self.pitch = []

        self.block = EnemyBlock(self.hand, self.combat_chain)

        self.ability = Ability()

    def reduce_life(self, value):
        self.life -= value

    def add_life(self, value):
        self.life += value

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

        self.further_attack_possible = True
        self.further_defense_possible = True

        if "intimidated_cards" in self.banished_zone:
            self.hand += self.banished_zone["intimidated_cards"]

            self.banished_zone["intimidated_cards"] = []

        self.block.reset()

        if self.stance == Stance.attack:
            self.pitch = []
            self.draw()

        if self.stance == Stance.defend:
            self.stance = Stance.attack
            self.calc_combat_chain()
            print("combat_chain")
            print(self.combat_chain)
        else:
            self.stance = Stance.defend
            self.calc_combat_chain()
            print("combat_chain")
            print(self.combat_chain)

    def check_if_further_defense_possible(self):
        if len(self.hand) == 0:
            self.further_defense_possible = False

    def check_if_further_attack_possible(self):
        print(self.combat_chain)
        if (
            len(self.combat_chain) == 0
            or self.combat_chain_iterator > len(self.combat_chain)
            or len(self.hand) == 0
        ):
            self.further_attack_possible = False

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

    def calc_combat_chain_damage_output(self):
        combat_chain_index = 0

        max_damage_output = 0
        number_of_cards_to_pitch = VALUE_MAX_PLACEHOLDER
        power_minus_cost = 0

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

    def order_hand_by_power_desc(self, hand):
        hand = sorted(hand, key=lambda x: x.power, reverse=True)
        return hand

    def order_hand_by_go_again_desc(self, hand):
        hand = sorted(hand, key=lambda x: x.keywords[0].value, reverse=False)
        return hand

    def calc_combat_chain(self):
        combat_chain_index = 0

        virtual_hand = self.hand.copy()

        # play strongest attacks first, but by a small chance not to be not too predictable -> shuffle, weakest first makes no sense at all
        if n_chance():
            virtual_hand = self.order_hand_by_power_desc(virtual_hand)
        else:
            np.random.shuffle(virtual_hand)

        # play go agains first with a certain chance
        if n_chance(p=0.50):
            virtual_hand = self.order_hand_by_go_again_desc(virtual_hand)

        virtual_hand_tmp = virtual_hand.copy()
        for i in range(len(virtual_hand)):
            if len(virtual_hand_tmp) > 0:
                current_card = virtual_hand_tmp[0]

                if current_card.card_type in [
                    CardType.attack_action,
                    CardType.non_attack_action,
                    CardType.attack_reaction,
                ]:
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

    def pitch_floating_resources(self, amount):
        self.floating_resources += amount

    def use_floating_resources(self, amount):
        self.floating_resources -= amount

    def remove_card_from_hand(self, card):
        if card in self.hand:
            self.hand.remove(card)
        else:
            print("card not in hand but should be !?")

    def attack(self):
        print("enemy attacking")

        print("enemy attacks with")
        if len(self.combat_chain) > 0:
            if self.combat_chain_iterator in self.combat_chain:
                if (
                    self.combat_chain_iterator == 0
                    or self.combat_chain[self.combat_chain_iterator - 1][
                        "attack"
                    ].keywords[0]
                    == Keyword.go_again
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

                        self.pitch_floating_resources(p.pitch)

                    self.played_cards.append(c)

                    for p in self.played_cards:
                        if p in self.hand:
                            self.remove_card_from_hand(p)

                    for p in self.pitched_cards:
                        if p in self.hand:
                            self.remove_card_from_hand(p)

                    self.use_floating_resources(c.cost)

                    self.combat_chain_iterator += 1

            else:
                self.further_attack_possible = False

    def defend(self, player_attack, modifiers):
        print("enemy defending")
        print(player_attack)
        if len(self.hand) > 0:
            if modifiers.modifier_dict["intimidate"] == True:
                random_banished_card = random.choice(self.hand)
                print(self.banished_zone["intimidated_cards"])

                self.banished_zone["intimidated_cards"].append(random_banished_card)
                self.hand.remove(random_banished_card)

            print(player_attack.physical)

            self.block.preserve_good_chain()
            blocking_cards = self.block.defend(player_attack)

            print(blocking_cards)
            if len(blocking_cards) > 0:
                if modifiers.modifier_dict["dominate"] == True:
                    blocking_cards = blocking_cards[:1]

                print("banished zone")
                print(self.banished_zone)

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


if __name__ == "__main__":
    e = Enemy()
    e.draw()
    e.calc_combat_chain()
