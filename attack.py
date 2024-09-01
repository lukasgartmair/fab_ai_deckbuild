#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 13:51:34 2024

@author: lukasgartmair
"""


from utils import n_chance, shift_list
import numpy as np
from playstyle import CardType


class Attack:
    def __init__(self, enemy):
        self.enemy = enemy

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
        combat_chain_index = 0

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
                        self.enemy.combat_chain[combat_chain_index] = {
                            "attack": current_card,
                            "pitch": cards_to_pitch,
                        }
                        combat_chain_index += 1

                        virtual_hand_tmp.remove(current_card)
                        for p in cards_to_pitch:
                            virtual_hand_tmp.remove(p)
                else:
                    self.enemy.combat_chain[combat_chain_index] = {
                        "attack": current_card,
                        "pitch": [],
                    }
                    combat_chain_index += 1

                    virtual_hand_tmp.remove(current_card)

    def get_next_attacking_card(self):
        c = self.enemy.combat_chain[self.enemy.combat_chain_iterator]["attack"]
        self.enemy.played_cards.append(c)
        return c

    def base_attack(self):
        c = self.get_next_attacking_card()

        self.enemy.pitch_cards()
        self.enemy.remove_played_cards()
        self.enemy.use_floating_resources(c.cost)
        self.enemy.use_action_points()
        self.enemy.handle_go_again(c)

        self.enemy.sound.play_attack(c)

        return c
