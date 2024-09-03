#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType
import numpy as np
from utils import shift_list, n_chance, get_combinations
import pitch
from action_point_manager import ActionPointManager


class CombatChain:
    def __init__(self, hand, action_point_manager, arsenal, weapons):
        self.hand = hand
        self.arsenal = arsenal
        self.weapons = weapons
        self.action_point_manager = action_point_manager
        self.chain = {}
        self.iterator = 0

    def get_length(self):
        return len(self.chain)

    def reset(self):
        self.chain = {}
        self.iterator = 0

    def clear_chain(self):
        self.chain = {}

    def iterator_in_chain(self):
        # print(self.iterator)
        # print(self.chain)
        if self.iterator in self.chain:
            return True
        else:
            return False

    def has_content(self):
        if self.get_length() > 0:
            return True
        else:
            return False

    def is_last_link(self, card):
        for k, v in self.chain.items():
            if card == v["play"]:
                if k == len(self.chain):
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

    def reorder_hand(self, hand):
        hand = sorted(
            hand, key=lambda x: (x.physical * -1, x.keywords[0].value), reverse=False
        )
        self.print_reordered_hand(hand)
        return hand

    def print_reordered_hand(self, hand):
        print([h.physical for h in hand])
        print([h.card_type.name for h in hand])

    def apply_class_specific_sorting_preferences(self, playable_cards):
        if n_chance(p=1):
            playable_cards = self.reorder_hand(playable_cards)
        else:
            np.random.shuffle(playable_cards)
        return playable_cards

    def get_pitch_bans(self):
        return self.arsenal + self.weapons

    def get_playable_cards(self):
        return [
            c
            for c in self.hand.copy() + self.arsenal + self.weapons
            if c.card_type not in [CardType.defensive_reaction]
        ]

    def print_combat_chain(self):
        pass
        # print("COMBAT CHAIN")
        # print("------------")
        # for k, v in self.chain.items():
        #     print()
        #     print(k)
        #     print("play")
        #     print(v["play"].name)
        #     print("pitch")
        #     for vi in v["pitch"]:
        #         print(vi.name)

        #     print("current_iterator")
        #     print(self.iterator)

    def get_next_attacking_card(self):
        c = self.chain[self.iterator]["play"]
        return c

    def rearrange_chain(self):
        if any(
            [
                True if v["play"].card_type == CardType.non_attack_action else False
                for v in self.chain.values()
            ]
        ):
            print("here")

    def update_playable_cards(self, playable_cards_tmp, cards_to_pitch):
        for p in cards_to_pitch:
            playable_cards_tmp = [pc for pc in playable_cards_tmp if pc != p]
        return playable_cards_tmp

    def update_virtual_hand(self, current_card, virtual_hand, cards_to_pitch):
        virtual_hand = [
            vh for vh in virtual_hand if vh != current_card and vh not in cards_to_pitch
        ]
        return virtual_hand

    def set_play(self, index, card, pitch=[]):
        self.chain[index] = {
            "play": card,
            "pitch": pitch,
        }

    def calc_damage_output(self):
        return sum([v["play"].physical + v["play"].arcane for v in self.chain.values()])

    def apply_chain_restriction(self, combinations):
        valid_combinations = combinations
        for combo in combinations:
            if [p.card_type for p in combo][-1] == CardType.non_attack_action:
                valid_combinations.remove(combo)
        return valid_combinations

    def get_playable_chains(self, playable_cards):
        combinations = get_combinations(playable_cards)
        print("len(combinations)")
        print(len(combinations))

        valid_combinations = self.apply_chain_restriction(combinations)

        print("len(valid_combinations)")
        print(len(valid_combinations))

        return valid_combinations

    def calc_combat_chain(self):
        self.clear_chain()

        pitch_bans = self.get_pitch_bans()

        playable_cards = self.get_playable_cards()

        playable_cards = self.apply_class_specific_sorting_preferences(playable_cards)

        valid_combinations = self.get_playable_chains(playable_cards)

        calculated_chains = []

        for j, vc in enumerate(valid_combinations):
            virtual_hand = self.hand.copy()

            virtual_action_point_manager = ActionPointManager(
                action_points=self.action_point_manager.action_points
            )

            virtual_combat_chain = CombatChain(
                virtual_hand, virtual_action_point_manager, self.arsenal, self.weapons
            )

            playable_cards_tmp = list(vc).copy()

            index = 0

            for i in range(len(vc)):
                if len(playable_cards_tmp) > 0:
                    if virtual_action_point_manager.has_action_points_left():
                        current_card = playable_cards_tmp[0]
                        cards_to_pitch = []

                        if current_card.cost > 0:
                            pitchable_cards = [
                                c
                                for c in virtual_hand
                                if (c != current_card and c not in pitch_bans)
                            ]
                            possible_combinations = get_combinations(pitchable_cards)

                            pitch_combinations = {}
                            for j, pi in enumerate(possible_combinations):
                                pitch_total = 0
                                pitch_total = sum([c.pitch for c in pi])
                                pitch_combinations[pi] = pitch_total

                            cards_to_pitch = pitch.determine_pitch_combination(
                                current_card.cost, pitch_combinations
                            )

                            if len(cards_to_pitch) == 0:
                                calculated_chains.append(virtual_combat_chain)
                                break

                            else:
                                virtual_combat_chain.set_play(
                                    index, current_card, pitch=cards_to_pitch
                                )

                                virtual_hand = self.update_virtual_hand(
                                    current_card, virtual_hand, cards_to_pitch
                                )

                        else:
                            virtual_combat_chain.set_play(index, current_card)

                        index += 1

                        if current_card.once_per_turn == False:
                            playable_cards = self.update_playable_cards(
                                playable_cards_tmp, cards_to_pitch
                            )

                        virtual_action_point_manager.handle_go_again(current_card)
                        if (
                            virtual_action_point_manager.has_action_points_left()
                            == False
                        ):
                            calculated_chains.append(virtual_combat_chain)
                            break

            else:
                calculated_chains.append(virtual_combat_chain)
                continue

            calculated_chains.append(virtual_combat_chain)

        print([c.calc_damage_output() for c in calculated_chains])

        print(calculated_chains)
        damage_outputs = [c.calc_damage_output() for c in calculated_chains]
        damage_outputs = [c.calc_damage_output() for c in calculated_chains]
        best_chain_index = damage_outputs.index(max(damage_outputs))

        self.chain = calculated_chains[best_chain_index].chain
