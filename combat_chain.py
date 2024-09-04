#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType
import numpy as np
from utils import n_chance, get_combinations
import pitch
from arsenal import Arsenal
from action_point_manager import ActionPointManager


class ChainLink:
    def __init__(self, play=[], reaction=[], pitch=[]):
        self.play = play
        self.reaction = reaction
        self.pitch = pitch


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
        self.pitch_bans = []
        self.turn_bans = []

        self.valid_combinations = []

        self.current_card = None

        self.update_card_lists()

    def get_length(self):
        return len(self.chain)

    def move_reset(self):
        self.clear_chain()
        self.current_card = None
        self.iterator = 0
        self.playable_cards = []
        self.pitch_bans = []
        self.valid_combinations = []
        self.update_card_lists()

    def turn_reset(self):
        self.move_reset()
        self.turn_bans = []

    def update_card_lists(self):
        self.pitch_bans = self.get_pitch_bans()
        self.playable_cards = self.get_playable_cards()

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
            if card in link.play:
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

    def get_pitch_bans(self):
        return self.arsenal.get_arsenal() + self.weapons

    def get_playable_cards(self):
        return [
            c
            for c in self.hand.copy() + self.arsenal.get_arsenal() + self.weapons
            if c.card_type not in [CardType.defensive_reaction]
        ]

    def print_combat_chain(self):
        print("COMBAT CHAIN")
        print("------------")
        for key, link in self.chain.items():
            print()
            print(key)
            print("play")
            for p in link.play:
                print(p.name)
            print("pitch")
            for p in link.pitch:
                print(p.name)

            print("current_iterator")
            print(self.iterator)

    def get_next_link(self):
        return self.chain[self.iterator]

    def update_playable_cards(self, cards_to_pitch):
        self.playable_cards = [
            pc
            for pc in self.playable_cards
            if (pc not in cards_to_pitch and pc not in self.turn_bans)
        ]

    def update_hand(self, cards_to_pitch):
        self.hand = [
            vh
            for vh in self.hand
            if vh != self.current_card and vh not in cards_to_pitch
        ]

    def get_pitchable_cards(self):
        return [
            c
            for c in self.hand
            if (c != self.current_card and c not in self.pitch_bans)
        ]

    def set_play(self, index, pitch=[]):
        self.chain[index] = ChainLink(play=[self.current_card], pitch=pitch)
        if self.current_card.once_per_turn == True:
            self.turn_bans.append(self.current_card)

    def calc_damage_output(self):
        return sum(
            [
                sum([c.physical for c in link.play])
                + sum([c.arcane for c in link.play])
                for link in self.chain.values()
            ]
        )

    def apply_chain_restriction(self, combinations):
        valid_combinations = combinations
        for combo in combinations:
            if [p.card_type for p in combo][-1] == CardType.non_attack_action:
                valid_combinations.remove(combo)

            if [p.card_type for p in combo][0] == CardType.attack_reaction:
                valid_combinations.remove(combo)

        return valid_combinations

    def get_valid_chains(self, playable_cards):
        combinations = get_combinations(playable_cards)

        valid_combinations = self.apply_chain_restriction(combinations)

        self.valid_combinations = valid_combinations

    def create_virtual_combat_chain(self, valid_combination):
        virtual_combat_chain = CombatChain(
            self.hand.copy(),
            action_point_manager=ActionPointManager(
                action_points=self.action_point_manager.action_points
            ),
            arsenal=self.arsenal,
            weapons=self.weapons,
        )

        virtual_combat_chain.playable_cards = list(valid_combination).copy()

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

    def get_pitch_for_link(self, pitch_totals):
        return pitch.determine_pitch_combination(self.current_card.cost, pitch_totals)

    def assure_consistency(self):
        # if self.is_empty():
        #     return False
        # if self.chain[len(self.chain) - 1].play.card_type == CardType.non_attack_action:
        #     return False

        # if all(
        #     [
        #         True
        #         if link.play.card_type
        #         in [CardType.non_attack_action, CardType.attack_reaction]
        #         else False
        #         for link in self.chain.values()
        #     ]
        # ):
        #     return False

        # else:
        #     return True
        return True

    def calc_combat_chain(self):
        initial_length = len(self.playable_cards)

        index = 0
        for i in range(initial_length):
            if self.has_another_link():
                self.current_card = self.get_current_card()

                cards_to_pitch = []

                if self.current_card.cost > 0:
                    pitchable_cards = self.get_pitchable_cards()

                    possible_pitch_combinations = get_combinations(pitchable_cards)

                    pitch_totals = self.calc_pitch_totals(possible_pitch_combinations)

                    cards_to_pitch = self.get_pitch_for_link(pitch_totals)

                    if len(cards_to_pitch) == 0:
                        return

                    else:
                        self.set_play(index, pitch=cards_to_pitch)

                else:
                    self.set_play(index)

                self.update_hand(cards_to_pitch)
                self.update_playable_cards(cards_to_pitch)

                self.action_point_manager.handle_keywords(
                    self.current_card, combat_chain=self
                )
                if self.action_point_manager.has_action_points_left() == False:
                    return

                index += 1

    def update_combat_chain(self):
        self.move_reset()

        self.get_valid_chains(self.playable_cards)

        calculated_chains = []

        for j, vc in enumerate(self.valid_combinations):
            virtual_combat_chain = self.create_virtual_combat_chain(vc)

            virtual_combat_chain.calc_combat_chain()

            if virtual_combat_chain.assure_consistency() == True:
                calculated_chains.append(virtual_combat_chain)

        if len(calculated_chains) > 0:
            # print([c.calc_damage_output() for c in calculated_chains])

            # print(calculated_chains)
            lengths = [len(c.chain) for c in calculated_chains]
            damage_outputs = [c.calc_damage_output() for c in calculated_chains]
            best_chain_index = damage_outputs.index(max(damage_outputs))

            self.chain = calculated_chains[best_chain_index].chain
