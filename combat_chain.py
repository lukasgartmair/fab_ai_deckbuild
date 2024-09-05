#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType
from utils import get_combinations
import pitch
from arsenal import Arsenal
from action_point_manager import ActionPointManager
import random
import copy
from enum import Enum


class LinkType(Enum):
    attack = 0
    attack_reaction = 1


attack_action_succession = [[1], [0, 1], [0, 0, 1], [0, 0, 0, 1]]
weapon_succession = [[xj * 4 for xj in xi] for xi in attack_action_succession]

valid_card_type_successions = attack_action_succession + weapon_succession


class ChainLink:
    def __init__(self, play={}, pitch={}, link_type=LinkType.attack):
        self.play = play
        self.link_type = link_type
        self.pitch = pitch

    def is_empty(self):
        return True if len(self.play) == 0 else False

    def set_play(self, index, play, pitch=[]):
        self.play[index] = play
        self.pitch[index] = pitch


class CombatChain:
    def __init__(
        self,
        hand,
        action_point_manager=ActionPointManager(),
        arsenal=Arsenal(),
        weapons=[],
    ):
        self.hand = hand
        self.arsenal = arsenal
        self.weapons = weapons
        self.action_point_manager = action_point_manager
        self.chain = {}
        self.iterator = 0

        self.playable_cards = []
        self.reaction_cards = []
        self.pitch_bans = []
        self.turn_bans = []

        self.current_card = None

        self.initialize_card_lists()

        self.valid_combinations = self.get_valid_combinations(self.playable_cards)

    def get_length(self):
        return len(self.chain)

    def move_reset(self):
        self.clear_chain()
        self.current_card = None
        self.iterator = 0
        self.playable_cards = []
        self.pitch_bans = []
        self.valid_combinations = []
        self.initialize_card_lists()

    def turn_reset(self):
        self.move_reset()
        self.turn_bans = []

    def initialize_card_lists(self):
        self.pitch_bans = self.get_pitch_bans()
        self.playable_cards = self.get_playable_cards()
        self.reaction_cards = self.get_reaction_step_cards()
        self.valid_combinations = self.get_valid_combinations(self.playable_cards)

    def clear_chain(self):
        self.chain = {}

    def iterator_in_chain(self):
        if self.iterator in self.chain:
            return True
        else:
            return False

    def started(self):
        return True if self.iterator > 0 else False

    def has_content(self):
        if self.get_length() > 0:
            return True
        else:
            return False

    def is_last_link(self, card):
        for key, link in self.chain.items():
            if card in link.play.values():
                if key == self.get_length():
                    return True
        return False

    def is_empty(self):
        if self.get_length() == 0:
            return True
        else:
            return False

    def end_reached(self):
        if self.iterator_in_chain():
            return False
        else:
            return True

    def increase_iterator(self):
        self.iterator += 1

    def get_reaction_step_cards(self):
        return [
            c
            for c in self.hand.copy() + self.arsenal.get_arsenal() + self.weapons
            if c.card_type == CardType.attack_reaction
        ]

    def print_combat_chain(self):
        print("COMBAT CHAIN")
        print(self.chain)
        print("------------")
        for key, link in self.chain.items():
            print()
            print(key)
            print("play")
            for k, p in link.play.items():
                print(p.name)
            print("pitch")
            for k, p in link.pitch.items():
                for pi in p:
                    print(pi.name)

            print("current_iterator")
            print(self.iterator)

    def get_next_link(self):
        return self.chain[self.iterator]

    def add_link(self, link):
        self.chain[self.iterator] = link
        self.increase_iterator()

    def get_pitch_bans(self):
        return self.arsenal.get_arsenal() + self.weapons

    def get_playable_cards(self):
        return [
            c
            for c in self.hand + self.arsenal.get_arsenal() + self.weapons
            if c.card_type in [CardType.attack_action, CardType.non_attack_action]
            and c not in self.turn_bans
        ]

    def remove_pitch_from_card_lists(self, cards_to_pitch):
        self.hand = [c for c in self.hand if c not in cards_to_pitch]

        self.playable_cards = [
            c for c in self.playable_cards if (c not in cards_to_pitch)
        ]

    def remove_current_card_from_lists(self):
        self.hand = [c for c in self.hand if c in self.hand and c != self.current_card]

        self.playable_cards = [
            c
            for c in self.playable_cards
            if c in self.playable_cards and c != self.current_card
        ]

    def get_pitchable_cards(self, card):
        return [
            c
            for c in self.hand
            if (c != card and c not in self.pitch_bans and c.pitch > 0)
        ]

    def calc_damage_output(self):
        return sum(
            [
                sum([c.physical for c in link.play.values()])
                + sum([c.arcane for c in link.play.values()])
                for link in self.chain.values()
            ]
        )

    def apply_chain_restriction(self, combinations):
        return [
            combo
            for combo in combinations
            if [c.card_type.value for c in combo] in valid_card_type_successions
        ]

    def get_valid_combinations(self, playable_cards):
        combinations = get_combinations(playable_cards)

        # print("HERE")
        # print(len((combinations)))

        valid_combinations = self.apply_chain_restriction(combinations)

        # print(len((valid_combinations)))

        return [list(v) for v in valid_combinations]

    def create_virtual_combat_chain(self):
        virtual_combat_chain = CombatChain(
            self.hand.copy(),
            action_point_manager=ActionPointManager(
                action_points=self.action_point_manager.action_points
            ),
            arsenal=copy.copy(self.arsenal),
            weapons=self.weapons.copy(),
        )
        virtual_combat_chain.valid_combinations = self.get_valid_combinations(
            self.get_playable_cards()
        )

        return virtual_combat_chain

    def has_another_link(self):
        if len(self.playable_cards) > 0:
            if self.action_point_manager.has_action_points_left() == True:
                return True
        else:
            return False

    def get_current_card(self):
        if len(self.playable_cards) > 0:
            return self.playable_cards.pop()

    def calc_pitch_totals(self, possible_pitch_combinations):
        pitch_totals = {}
        for j, pi in enumerate(possible_pitch_combinations):
            pitch_totals[pi] = sum([c.pitch for c in pi])
        return pitch_totals

    def get_pitch_for_card(self, card, pitch_totals):
        return pitch.determine_pitch_combination(card.cost, pitch_totals)

    def assure_consistency(self):
        if self.is_empty():
            return False
        # for link in self.chain.values():

        #     if self.chain[len(self.chain) - 1].play.card_type == CardType.non_attack_action:
        #         return False
        else:
            return True

    def get_cards_to_pitch(self, card):
        cards_to_pitch = []

        pitchable_cards = self.get_pitchable_cards(card)

        possible_pitch_combinations = get_combinations(pitchable_cards)

        pitch_totals = self.calc_pitch_totals(possible_pitch_combinations)

        cards_to_pitch = self.get_pitch_for_card(card, pitch_totals)

        return cards_to_pitch

    def calc_if_chain_link_is_viable(self, combination):
        is_viable = False
        initial_list = combination.copy()

        print("here")
        print([c.card_type.value for c in combination])
        print([c.card_type.value for c in combination] in valid_card_type_successions)
        print()

        virtual_chain_link = ChainLink()

        index = 0
        for card in initial_list:
            if card in self.playable_cards:
                self.current_card = card

                if card.cost > 0:
                    cards_to_pitch = self.get_cards_to_pitch(self.current_card)
                    if len(cards_to_pitch) == 0:
                        break
                    else:
                        virtual_chain_link.set_play(
                            index, self.current_card, cards_to_pitch
                        )
                        self.remove_pitch_from_card_lists(cards_to_pitch)
                        is_viable = True
                        self.action_point_manager.use_action_points()
                else:
                    virtual_chain_link.set_play(index, self.current_card)
                    is_viable = True
                    self.action_point_manager.use_action_points()

                self.action_point_manager.handle_keywords(
                    self.current_card, combat_chain=self
                )

                self.remove_current_card_from_lists()

                print(self.action_point_manager.has_action_points_left())

                if self.action_point_manager.has_action_points_left() == False:
                    break

                index += 1

            else:
                is_viable = False

        return is_viable, virtual_chain_link

    def calc_chain_link(self, combination):
        dummy_combat_chain = self.create_virtual_combat_chain()

        (
            link_is_viable,
            virtual_chain_link,
        ) = dummy_combat_chain.calc_if_chain_link_is_viable(combination)

        if link_is_viable == True:
            self = dummy_combat_chain

        return link_is_viable, virtual_chain_link

    def calc_combat_chain(self):
        random.shuffle(self.valid_combinations)
        for j, vc in enumerate(self.valid_combinations):
            link_is_viable, virtual_chain_link = self.calc_chain_link(vc)

            if link_is_viable == True:
                self.add_link(virtual_chain_link)

                print(self.action_point_manager.has_action_points_left())
                if self.action_point_manager.has_action_points_left() == False:
                    break

    def calc_combat_chains(self, n=1):
        calculated_chains = []

        for i in range(n):
            virtual_combat_chain = self.create_virtual_combat_chain()

            virtual_combat_chain.calc_combat_chain()

            if virtual_combat_chain.assure_consistency() == True:
                calculated_chains.append(virtual_combat_chain)

        return calculated_chains

    def update_combat_chain(self):
        self.move_reset()

        calculated_chains = self.calc_combat_chains(n=1)

        # print("here")
        # print(len(calculated_chains))
        for c in calculated_chains:
            if c.get_length() > 0:
                print(c.get_length())
        if len(calculated_chains) > 0:
            # print([c.calc_damage_output() for c in calculated_chains])

            # print(calculated_chains)
            damage_outputs = [c.calc_damage_output() for c in calculated_chains]
            best_chain_index = damage_outputs.index(max(damage_outputs))

            self.chain = calculated_chains[best_chain_index].chain
