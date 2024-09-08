#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:07:15 2024

@author: lukasgartmair
"""

from enum import Enum
from utils import get_permutations
from action_point_manager import ActionPointManager
from pitch import determine_pitch_combination


class LinkType(Enum):
    attack = 0
    attack_reaction = 1


attack_action_succession = [[1], [2, 1], [2, 2, 1], [2, 2, 2, 1]]
weapon_succession = [[4], [2, 4], [2, 2, 4], [2, 2, 2, 4]]

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
    def apply_succesion_restrictions(self, playable_cards):
        permutations = get_permutations(playable_cards)
        valid_combinations = []
        for combo in permutations:
            # print([c.card_type.value for c in combo])
            if [c.card_type.value for c in combo] in valid_card_type_successions:
                valid_combinations.append(combo)

        return valid_combinations

    def get_pitch_for_card(self, card, pitch_totals):
        return determine_pitch_combination(card.cost, pitch_totals)

    def get_cards_to_pitch(self, card, pitchable_cards):
        cards_to_pitch = []

        possible_pitch_combinations = get_permutations(pitchable_cards)

        pitch_totals = self.calc_pitch_totals(possible_pitch_combinations)

        cards_to_pitch = self.get_pitch_for_card(card, pitch_totals)

        return cards_to_pitch

    def calc_pitch_totals(self, possible_pitch_combinations):
        pitch_totals = {}
        for j, pi in enumerate(possible_pitch_combinations):
            pitch_totals[pi] = sum([c.pitch for c in pi])
        return pitch_totals

    def calc_if_chain_link_is_viable(
        self, combination, playable_cards_pool, pitchable_cards_pool
    ):
        is_viable = False

        virtual_action_point_manager = ActionPointManager()

        print("here")
        print([c.card_type.value for c in combination])
        print([c.card_type.value for c in combination] in valid_card_type_successions)
        print()

        virtual_chain_link = ChainLink()

        index = 0
        for current_card in combination:
            cards_to_pitch = []
            if current_card in playable_cards_pool:
                if current_card.cost > 0:
                    cards_to_pitch = self.get_cards_to_pitch(
                        current_card, pitchable_cards_pool
                    )
                    if len(cards_to_pitch) == 0:
                        break
                    else:
                        virtual_chain_link.set_play(index, current_card, cards_to_pitch)
                        pitchable_cards_pool = [
                            c
                            for c in pitchable_cards_pool
                            if (
                                c not in cards_to_pitch
                                and c != current_card
                                and c.pitch > 0
                            )
                        ]
                        is_viable = True
                        virtual_action_point_manager.use_action_points()
                else:
                    virtual_chain_link.set_play(index, current_card)
                    is_viable = True
                    virtual_action_point_manager.use_action_points()

                virtual_action_point_manager.handle_keywords(current_card)

                playable_cards_pool = [
                    c
                    for c in playable_cards_pool
                    if (c != current_card and c not in cards_to_pitch)
                ]

                index += 1

                if virtual_action_point_manager.has_action_points_left() == False:
                    break

            else:
                is_viable = False

        return is_viable, virtual_chain_link
