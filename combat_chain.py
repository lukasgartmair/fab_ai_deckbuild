#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType
import numpy as np
from utils import shift_list, n_chance


class CombatChain:
    def __init__(self, enemy):
        self.enemy = enemy
        self.chain = {}
        self.iterator = 0

    def get_length(self):
        return len(self.chain)

    def reset(self):
        self.chain = {}
        self.iterator = 0

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

    def apply_class_specific_sorting_preferences(self, virtual_hand):
        if n_chance(p=1):
            virtual_hand = self.reorder_hand(virtual_hand)
        else:
            np.random.shuffle(virtual_hand)
        return virtual_hand

    def calc_combat_chain(self):
        index = 0

        not_pitchable_cards = self.enemy.arsenal + self.enemy.weapons

        virtual_hand = (
            [
                c
                for c in self.enemy.hand
                if c.card_type not in [CardType.defensive_reaction]
            ].copy()
            + self.enemy.arsenal
            + self.enemy.weapons
        )

        np.random.shuffle(virtual_hand)

        virtual_hand = self.apply_class_specific_sorting_preferences(virtual_hand)

        virtual_hand_tmp = virtual_hand.copy()
        for i in range(len(virtual_hand)):
            if len(virtual_hand_tmp) > 0:
                current_card = virtual_hand_tmp[0]

                possible_cards_to_pitch = self.enemy.pitch.get_combinations(
                    [v for v in virtual_hand_tmp if v not in not_pitchable_cards], 0
                )

                pitch_combinations = {}
                for j, pi in enumerate(possible_cards_to_pitch):
                    pitch_total = 0
                    for p in pi:
                        pitch_total += p.pitch

                    pitch_combinations[pi] = pitch_total

                if current_card.cost > 0:
                    cards_to_pitch = self.enemy.pitch.determine_pitch_combination(
                        current_card.cost, pitch_combinations
                    )

                    if len(cards_to_pitch) == 0:
                        virtual_hand = shift_list(virtual_hand_tmp)
                        continue
                    else:
                        self.chain[index] = {
                            "attack": current_card,
                            "pitch": cards_to_pitch,
                        }
                        index += 1

                        virtual_hand_tmp.remove(current_card)
                        for p in cards_to_pitch:
                            virtual_hand_tmp.remove(p)
                else:
                    self.chain[index] = {
                        "attack": current_card,
                        "pitch": [],
                    }
                    index += 1

                    virtual_hand_tmp.remove(current_card)
