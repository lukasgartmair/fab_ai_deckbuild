#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 17:07:15 2024

@author: lukasgartmair
"""

from enum import Enum
from utils import get_permutations, map_permutations_to_original
from action_point_manager import ActionPointManager
from pitch import determine_pitch_combination
import random
import numpy as np
from playstyle import CardType
from arsenal import Arsenal


class LinkType(Enum):
    attack = 0
    attack_reaction = 1


attack_action_succession = [[1], [0, 1], [0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0, 1]]
weapon_succession = [[4], [0, 4], [0, 0, 4], [0, 0, 0, 4], [0, 0, 0, 0, 4]]

valid_card_type_successions = attack_action_succession + weapon_succession


class ChainLinkStep:
    def __init__(self, index, play=None, pitch=[]):
        self.index = index
        self.play = play
        self.pitch = pitch


class ChainLink:
    def __init__(self, link_type=LinkType.attack):
        self.steps = {}
        self.link_type = link_type

    def is_empty(self):
        return True if len(self.play) == 0 else False

    def set_play(self, index, card, pitch=[]):
        self.steps[index] = ChainLinkStep(index, card, pitch)

    def get_play_cards(self):
        cards = []
        for k, v in self.steps.items():
            cards.append(v.play)
        return cards

    def get_pitch_cards(self):
        cards = []
        for k, v in self.steps.items():
            for c in v.pitch:
                cards.append(c.pitch)
        return cards


class CombatChain:
    def __init__(
        self,
        hand,
        arsenal=Arsenal(),
        weapons=[],
    ):
        self.hand = hand
        self.arsenal = arsenal
        self.weapons = weapons
        self.chain = {}
        self.iterator = 0

        self.turn_bans = []

    def get_length(self):
        return len(self.chain)

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

    def iterator_in_chain(self):
        if self.iterator in self.chain:
            return True
        else:
            return False

    def increase_iterator(self):
        self.iterator += 1

    def clear_chain(self):
        self.chain = {}

    def apply_card_type_succesion_restrictions(self, playable_cards):
        permutations = get_permutations(playable_cards)
        valid_combinations = []
        for combo in permutations:
            # print([c.card_type.value for c in combo])
            if [c.card_type.value for c in combo] in valid_card_type_successions:
                valid_combinations.append(combo)

        return valid_combinations

    def add_link(self, index, link):
        self.chain[index] = link

    def turn_reset(self):
        self.move_reset()
        self.turn_bans = []

    def move_reset(self):
        self.clear_chain()
        self.iterator = 0
        self.playable_cards = []
        self.pitch_bans = []

    def get_playable_cards(self):
        return [
            c
            for c in self.hand + self.arsenal.get_arsenal() + self.weapons
            if c.card_type in [CardType.attack_action, CardType.non_attack_action]
            and c not in self.turn_bans
        ]

    def get_pitchable_cards(self):
        return [c for c in self.hand if c.pitch > 0]

    def get_next_link(self):
        if self.is_empty() == False:
            return self.chain[self.iterator]
        else:
            return None

    def get_pitch_for_card(self, card, pitch_totals):
        return determine_pitch_combination(card.cost, pitch_totals)

    def get_cards_to_pitch(self, card, pitchable_cards):
        cards_to_pitch = []

        possible_pitch_combinations = get_permutations(pitchable_cards)

        pitch_totals = self.calc_pitch_totals(possible_pitch_combinations)

        cards_to_pitch = self.get_pitch_for_card(card, pitch_totals)

        return cards_to_pitch

    def calc_damage_output(self, chain):
        return sum(
            [
                sum([c.physical for c in link_dict["chain_link"].get_play_cards()])
                + sum([c.arcane for c in link_dict["chain_link"].get_play_cards()])
                for link_dict in chain
            ]
        )

    def print_combat_chain(self):
        print("COMBAT CHAIN")
        print(self.chain)
        print("------------")
        for key, link in self.chain.items():
            print()
            print(key)

            for k, p in link.steps.items():
                print("play")

                print(p.play.name)
                print("pitch")
                for pj in p.pitch:
                    print(pj.name)

            print("current_iterator")
            print(self.iterator)

    def calc_pitch_totals(self, possible_pitch_combinations):
        pitch_totals = {}
        for j, pi in enumerate(possible_pitch_combinations):
            pitch_totals[pi] = sum([c.pitch for c in pi])
        return pitch_totals

    def calc_chain_link(self, combination, playable_cards_pool, pitchable_cards_pool):
        is_viable = False
        has_action_point_left = False

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
                        current_card,
                        [p for p in pitchable_cards_pool if p != current_card],
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

        has_action_point_left = virtual_action_point_manager.has_action_points_left()

        return (
            is_viable,
            has_action_point_left,
            virtual_chain_link,
            playable_cards_pool,
            pitchable_cards_pool,
        )

    def calc_chain_links(
        self, valid_combinations, playable_cards_pool, pitchable_cards_pool
    ):
        possible_chain_links = {}
        print("before")
        n_rnd_subsets = 5
        print(len(valid_combinations))
        if len(valid_combinations) > 0:
            rnd_subset = random.choices(
                valid_combinations, k=(min(len(valid_combinations), n_rnd_subsets))
            )
            print("after")
            print(len(rnd_subset))
            for i, vc in enumerate(rnd_subset):
                (
                    is_viable,
                    has_action_point_left,
                    chain_link,
                    playable_cards_pool,
                    pitchable_cards_pool,
                ) = self.calc_chain_link(vc, playable_cards_pool, pitchable_cards_pool)

                if is_viable == True:
                    possible_chain_links[i] = {}
                    possible_chain_links[i]["is_viable"] = is_viable
                    possible_chain_links[i][
                        "has_action_point_left"
                    ] = has_action_point_left
                    possible_chain_links[i]["chain_link"] = chain_link
                    possible_chain_links[i]["playable_cards_pool"] = playable_cards_pool
                    possible_chain_links[i][
                        "pitchable_cards_pool"
                    ] = pitchable_cards_pool

        return possible_chain_links

    def succession_is_interrupted(self, action_point_left_list):
        action_point_left_array = np.array(action_point_left_list)
        is_interrupted = True
        if action_point_left_array.sum() == len(action_point_left_array):
            is_interrupted = False
        elif (
            action_point_left_array.sum() == len(action_point_left_array) - 1
            and action_point_left_array[-1] == 0
        ):
            is_interrupted = False
        else:
            pass

        return is_interrupted

    def apply_action_point_succesion_restrictions(self, possible_chain_links):
        chain_link_permutations = get_permutations(possible_chain_links, max_length=5)
        possible_link_successions = map_permutations_to_original(
            possible_chain_links, chain_link_permutations
        )

        link_successions = []
        for link_succession in possible_link_successions:
            if len(link_succession) > 1:
                action_point_left_list = [
                    link["has_action_point_left"] for link in link_succession
                ]
                if self.succession_is_interrupted(action_point_left_list) == False:
                    link_successions.append(link_succession)
            else:
                link_successions.append(link_succession)

        return link_successions

    def check_if_link_cards_are_still_available(
        self, link_dict, virtual_playable_cards_pool, virtual_pitchable_cards_pool
    ):
        link_cards_still_available = False

        if set(link_dict["chain_link"].get_play_cards()).issubset(
            virtual_playable_cards_pool
        ) and set(link_dict["chain_link"].get_pitch_cards()).issubset(
            virtual_pitchable_cards_pool
        ):
            link_cards_still_available = True

        return link_cards_still_available

    def calc_combat_chains(self, playable_cards_pool, pitchable_cards_pool):
        valid_combinations = self.apply_card_type_succesion_restrictions(
            playable_cards_pool
        )

        possible_chain_links = self.calc_chain_links(
            valid_combinations, playable_cards_pool, pitchable_cards_pool
        )

        possible_chain_links = self.apply_action_point_succesion_restrictions(
            possible_chain_links
        )
        calculated_chains = []

        for pcl_dict in possible_chain_links:
            pcl_dict = pcl_dict[0]

            print(pcl_dict)

            virtual_playable_cards_pool = playable_cards_pool.copy()
            virtual_pitchable_cards_pool = pitchable_cards_pool.copy()

            virtual_chain = []
            virtual_chain.append(pcl_dict)

            virtual_playable_cards_pool = [
                c
                for c in virtual_playable_cards_pool
                if c not in pcl_dict["chain_link"].get_play_cards()
            ]
            virtual_pitchable_cards_pool = [
                c
                for c in virtual_pitchable_cards_pool
                if c not in pcl_dict["chain_link"].get_pitch_cards()
            ]

            for pcl_2_dict in possible_chain_links:
                if pcl_dict != pcl_2_dict:
                    if (
                        self.check_if_link_cards_are_still_available(
                            pcl_dict,
                            virtual_playable_cards_pool,
                            virtual_pitchable_cards_pool,
                        )
                        == True
                    ):
                        virtual_chain.append(pcl_2_dict)
                        virtual_playable_cards_pool = [
                            c
                            for c in virtual_playable_cards_pool
                            if c not in pcl_2_dict["chain_link"].get_play_cards()
                        ]
                        virtual_pitchable_cards_pool = [
                            c
                            for c in virtual_pitchable_cards_pool
                            if c not in pcl_2_dict["chain_link"].get_pitch_cards
                        ]

            calculated_chains.append(virtual_chain)

        return calculated_chains

    def update_combat_chain(self):
        self.move_reset()

        calculated_chains = self.calc_combat_chains(
            self.get_playable_cards(), self.get_pitchable_cards()
        )

        # print("here")
        # print(len(calculated_chains))
        for c in calculated_chains:
            if len(c) > 0:
                print(len(c))
        if len(calculated_chains) > 0:
            # print([c.calc_damage_output() for c in calculated_chains])

            # print(calculated_chains)
            damage_outputs = [self.calc_damage_output(c) for c in calculated_chains]
            best_chain_index = damage_outputs.index(max(damage_outputs))

            for i, ci in enumerate(calculated_chains[best_chain_index]):
                self.add_link(i, ci["chain_link"])
