#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType, Keyword
import numpy as np
from utils import shift_list, n_chance
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
        print("COMBAT CHAIN")
        print("------------")
        for k, v in self.chain.items():
            print()
            print(k)
            print("attack")
            print(v["attack"].name)
            print("pitch")
            for vi in v["pitch"]:
                print(vi.name)

            print("current_iterator")
            print(self.iterator)

    def get_next_attacking_card(self):
        c = self.chain[self.iterator]["attack"]
        return c

    def calc_combat_chain(self):
        self.clear_chain()

        index = 0

        pitch_bans = self.get_pitch_bans()

        playable_cards = self.get_playable_cards()

        playable_cards = self.apply_class_specific_sorting_preferences(playable_cards)

        virtual_hand = self.hand.copy()

        virtual_action_point_manager = ActionPointManager(
            action_points=self.action_point_manager.action_points
        )

        playable_cards_tmp = playable_cards.copy()

        for i in range(len(playable_cards)):
            if len(playable_cards_tmp) > 0:
                if virtual_action_point_manager.has_action_points_left():
                    current_card = playable_cards_tmp[0]

                    if current_card.cost > 0:
                        pitchable_cards = [
                            c
                            for c in virtual_hand
                            if (c != current_card and c not in pitch_bans)
                        ]
                        possible_combinations = pitch.get_combinations(pitchable_cards)

                        pitch_combinations = {}
                        for j, pi in enumerate(possible_combinations):
                            pitch_total = 0
                            pitch_total = sum([c.pitch for c in pi])
                            pitch_combinations[pi] = pitch_total

                        cards_to_pitch = pitch.determine_pitch_combination(
                            current_card.cost, pitch_combinations
                        )

                        if len(cards_to_pitch) == 0:
                            playable_cards_tmp = shift_list(playable_cards_tmp)
                            continue
                        else:
                            self.chain[index] = {
                                "attack": current_card,
                                "pitch": cards_to_pitch,
                            }

                            for p in cards_to_pitch:
                                playable_cards_tmp = [
                                    pc for pc in playable_cards_tmp if pc != p
                                ]

                            virtual_hand = [
                                vh
                                for vh in virtual_hand
                                if vh != p and vh != current_card
                            ]

                    else:
                        self.chain[index] = {
                            "attack": current_card,
                            "pitch": [],
                        }

                    index += 1

                    if current_card.once_per_turn == False:
                        playable_cards_tmp = [
                            pc for pc in playable_cards_tmp if pc != current_card
                        ]

                    virtual_action_point_manager.handle_go_again(current_card)
