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
from playstyle import Keyword, PlayerClass, Talent, CardType, get_playstyle
from equipment import EquipmentSuite
from weapon import initialize_weapons
import random
from fantasynames.fantasy_identity import FantasyIdentity
from block import Block
from utils import n_chance, shift_list
from ability import Ability
from life_counter import LifeCounter
import pygame
from sound import Sound

from lore import lore_dict
from modifiers import Modifiers
import image

VALUE_MAX_PLACEHOLDER = 100


class Stance(Enum):
    defend = 0
    attack = 1


class Enemy:
    playKey = None

    def __init__(self, player_class=PlayerClass.generic):
        self.player_class = player_class

        self.identity = FantasyIdentity(self.player_class)
        self.name = self.identity.name
        self.race = self.identity.race
        self.image_path = (
            "images/" + self.player_class.name + "/" + self.identity.image_number
        )
        self.image = image.load_image(self.image_path)

        if n_chance(p=0.5):
            self.stance = Stance.defend
        else:
            self.stance = Stance.attack

        self.intellect = 4
        self.talent = random.choice(list(Talent))
        self.starting_life = 20
        self.hand = []
        self.pile = Pile()
        self.play_key = pygame.K_SPACE

        self.soul = []

        self.playstyle = get_playstyle(self.player_class)
        self.original_deck = Deck(self.player_class, self.playstyle)

        self.deck = self.original_deck

        self.graveyard = []
        self.banished_zone = {}
        self.banished_zone["intimidated_cards"] = []

        self.arsenal = []

        self.weapons = initialize_weapons(self.playstyle)

        self.equipment_suite = EquipmentSuite()

        self.further_attack_possible = True
        self.further_defense_possible = True

        self.floating_resources = 0

        self.pitched_cards = []
        self.played_cards = []

        self.combat_chain_iterator = 0

        self.combat_chain = {}

        self.block = Block(self)

        self.modifiers = Modifiers()

        self.ability = Ability()

        self.life_counter = LifeCounter(self.starting_life)

        if self.player_class.name in lore_dict:
            self.lore = random.choice(lore_dict[self.player_class.name])
        else:
            self.lore = ""
        self.lore = self.lore.replace("{}", self.name)

        self.action_points = 0

        self.survival_mode = False
        self.check_if_in_survival_mode()

        self.sound = Sound()

    def check_if_in_survival_mode(self):
        if self.life_counter.life <= 5:
            self.survival_mode = True
        else:
            self.survival_mode = False

    def initialize_play(self):
        self.draw()
        if self.stance == Stance.attack:
            self.calc_combat_chain()
        self.reset_play()

    def reset_play(self):
        self.floating_resources = 0
        self.reset_action_points()
        self.further_attack_possible = True
        self.further_defense_possible = True

    def reset_action_points(self):
        self.action_points = 1

    def get_action_points(self, amount=1):
        self.action_points += amount

    def use_action_points(self, amount=1):
        if self.action_points >= amount:
            self.action_points -= amount
            return True
        else:
            return False

    def arsenal_empty(self):
        if len(self.arsenal) == 0:
            return True
        else:
            return False

    def fill_arsenal(self):
        if len(self.hand) > 0:
            c = self.hand[0]
            self.arsenal.append(c)
            self.hand.remove(c)

    def change_stance(self):
        if self.stance == Stance.defend:
            self.stance = Stance.attack
            self.calc_combat_chain()
            # print("combat_chain")
            # print(self.combat_chain)

            self.sound.play_change_stance_to_attack()

        elif self.stance == Stance.attack:
            if self.arsenal_empty():
                self.fill_arsenal()

            self.stance = Stance.defend
            self.check_if_in_survival_mode()
            self.draw()
            self.calc_combat_chain()
            # print("combat_chain")
            # print(self.combat_chain)

    def finish_move(self):
        pass

    def start_move(self):
        self.check_if_further_move_possible()

    def finish_turn(self):
        self.reset_play()

        for card in self.played_cards:
            if card.card_type not in [CardType.weapon, CardType.equipment]:
                self.graveyard.append(card)

            elif card.card_type == CardType.equipment:
                card.finish_defensive_turn()
                if card.destroyed == True:
                    self.graveyard.append(card)

        for pc in self.pitched_cards:
            self.deck.put_to_bottom(pc)

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

        self.change_stance()

    def check_if_further_move_possible(self):
        if self.stance == Stance.attack:
            self.check_if_further_attack_possible()
        elif self.stance == Stance.defend:
            self.check_if_further_defense_possible()

    def check_if_further_attack_possible(self):
        if (
            len(self.combat_chain) == 0
            or self.combat_chain_iterator > len(self.combat_chain)
            or (len(self.hand) == 0 and len(self.arsenal) == 0)
            or self.action_points == 0
        ):
            self.further_attack_possible = False

    def check_if_further_defense_possible(self):
        if (len(self.hand) == 0 and len(self.arsenal) == 0) or (
            (len(self.hand) == 0)
            and (len(self.arsenal) == 1)
            and (self.arsenal[0].card_type != CardType.defensive_reaction)
        ):
            self.further_defense_possible = False

    def draw(self):
        print("enemy is drawing")
        if self.deck.get_length() > 0:
            n_cards_to_draw = self.intellect - len(self.hand)
            if n_cards_to_draw > 0:
                if self.deck.get_length() < n_cards_to_draw:
                    n_cards_to_draw = self.deck.get_length()

                drawn_cards = self.deck.draw_top_cards(n=n_cards_to_draw)

                if type(drawn_cards) is list:
                    self.hand += drawn_cards

                self.sound.play_draw_cards(n_cards=len(drawn_cards))

        else:
            print("can't draw anymore, deck fatigued")

    def order_hand_by_physical_desc(self, hand):
        hand = sorted(hand, key=lambda x: x.physical, reverse=True)
        return hand

    def order_hand_by_go_again(self, hand):
        hand = sorted(hand, key=lambda x: x.keywords[0].value, reverse=False)
        return hand

    def calc_combat_chain(self):
        combat_chain_index = 0

        not_pitchable_cards = self.arsenal + self.weapons

        virtual_hand = self.hand.copy() + self.arsenal + self.weapons

        np.random.shuffle(virtual_hand)

        # play strongest attacks first, but by a small chance not to be not too predictable -> shuffle, weakest first makes no sense at all
        if n_chance(p=1):
            virtual_hand = self.order_hand_by_physical_desc(virtual_hand)
        else:
            np.random.shuffle(virtual_hand)

        # play go agains first with a certain chance
        if n_chance(p=1):
            virtual_hand = self.order_hand_by_go_again(virtual_hand)

        virtual_hand_tmp = virtual_hand.copy()
        for i in range(len(virtual_hand)):
            if len(virtual_hand_tmp) > 0:
                current_card = virtual_hand_tmp[0]

                if current_card.card_type not in [CardType.defensive_reaction]:
                    possible_cards_to_pitch = self.get_combinations(
                        [v for v in virtual_hand_tmp if v not in not_pitchable_cards], 0
                    )

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
        if self.floating_resources < 0:
            self.floating_resources = 0

    def remove_card_from_hand(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def check_if_attack(self):
        if len(self.combat_chain) > 0:
            if self.combat_chain_iterator in self.combat_chain:
                print(self.action_points)
                if self.action_points > 0:
                    return True
        else:
            return False

    def get_next_attacking_card(self):
        c = self.combat_chain[self.combat_chain_iterator]["attack"]
        self.played_cards.append(c)
        return c

    def pitch_cards(self):
        for p in self.combat_chain[self.combat_chain_iterator]["pitch"]:
            self.pitch_card(p)

    def remove_played_cards(self):
        for p in self.played_cards:
            if p in self.hand:
                self.remove_card_from_hand(p)
            if p in self.arsenal:
                self.arsenal.remove(p)

    def handle_go_again(self, c):
        # TODO for now combo also gives another action point
        if (Keyword.go_again in c.keywords) or (Keyword.combo in c.keywords):
            self.get_action_points()

    def base_attack(self):
        c = self.get_next_attacking_card()

        self.pitch_cards()
        self.remove_played_cards()
        self.use_floating_resources(c.cost)
        self.use_action_points()
        self.handle_go_again(c)

        self.sound.play_attack()

        return c

    def attack(self):
        if self.check_if_attack():
            c = self.base_attack()

            self.combat_chain_iterator += 1

        else:
            self.further_attack_possible = False

    def pitch_card(self, c):
        self.pitched_cards.append(c)
        self.pitch_floating_resources(c.pitch)
        self.hand.remove(c)

    def print_cards(self):
        print("HAND")
        for c in self.hand:
            print(c.name)

        print("ARSENAL")
        for c in self.arsenal:
            print(c.name)

    def defend(self, player_attack):
        # self.print_cards()

        self.calc_combat_chain()

        # print("enemy defending")
        # print(player_attack)
        if len(self.hand) > 0:
            if self.modifiers.modifier_dict["intimidate"] == True:
                random_banished_card = random.choice(self.hand)
                # print(self.banished_zone["intimidated_cards"])

                self.banished_zone["intimidated_cards"].append(random_banished_card)
                self.hand.remove(random_banished_card)

            # TODO arcane or physical first?
            if n_chance(p=0.5):
                if player_attack.arcane is not None:
                    self.block.defend_arcane(player_attack)
                self.block.defend_physical(player_attack)
            else:
                self.block.defend_physical(player_attack)
                if player_attack.arcane is not None:
                    self.sound.play_flip_card()
                    self.block.defend_arcane(player_attack)

            # print(self.block.physical_block_cards)
            if len(self.block.physical_block_cards) > 0:
                if self.modifiers.modifier_dict["dominate"] == True:
                    self.block.physical_block_cards = self.block.physical_block_cards[
                        :1
                    ]

                # print("banished zone")
                # print(self.banished_zone)

                self.sound.play_block()

                for bc in self.block.physical_block_cards:
                    # print(bc)
                    self.played_cards.append(bc)
                    # print("enemy defends with")
                    # print(bc.name)
                    # print("defense: {}".format(bc.defense))
                    if bc in self.hand:
                        self.hand.remove(bc)

                    if bc in self.arsenal:
                        self.arsenal.remove(bc)

        self.life_counter.calculate_life(player_attack, self.block)
        self.block.reset()

    def get_combinations(self, array, current_index):
        combinations = []
        array_copy = array.copy()
        # print(array_copy)
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
