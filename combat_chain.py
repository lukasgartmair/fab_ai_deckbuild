#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:23:09 2024

@author: lukasgartmair
"""
from playstyle import CardType
import numpy as np
from utils import shift_list, n_chance
import pitch


class CombatChain:
    def __init__(self, hand, arsenal, weapons):
        self.hand = hand
        self.arsenal = arsenal
        self.weapons = weapons
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

    def calc_combat_chain(self):
        index = 0

        pitch_bans = self.get_pitch_bans()

        playable_cards = self.get_playable_cards()

        playable_cards = self.apply_class_specific_sorting_preferences(playable_cards)

        virtual_hand = self.hand.copy()

        playable_cards_tmp = playable_cards.copy()

        for i in range(len(playable_cards)):
            if len(playable_cards_tmp) > 0:
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
                        index += 1

                    for p in cards_to_pitch:
                        playable_cards_tmp = [
                            pc for pc in playable_cards_tmp if pc != p
                        ]
                        virtual_hand = [vh for vh in virtual_hand if vh != p]
                else:
                    self.chain[index] = {
                        "attack": current_card,
                        "pitch": [],
                    }
                    index += 1

                playable_cards_tmp = [
                    p for p in playable_cards_tmp if p != current_card
                ]
