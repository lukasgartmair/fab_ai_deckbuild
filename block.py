#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 19:54:38 2024

@author: lukasgartmair
"""

import numpy as np
from utils import n_chance, add_two_with_possible_none_type, get_combinations
from card import CardType
import itertools
from pitch import determine_arcane_defense_pitch_combination

DEFENSIVE_REACTION_THRESHOLD = 3


def calc_total_physical_block(physical_block_cards):
    if physical_block_cards is not None:
        sum_block = sum([p.defense for p in physical_block_cards])
        return sum_block if sum_block > 0 else None
    else:
        return None


def calc_total_arcane_block(arcane_block_cards):
    if arcane_block_cards is not None:
        sum_block = sum([p.arcane_barrier for p in arcane_block_cards])
        return sum_block if sum_block > 0 else None
    else:
        return None


def check_defensive_reaction_trigger(damage_step_value, already_blocked_with_cards):

    # if damage_step_value is not None:

    #     damage_left = damage_step_value - calc_total_physical_block(
    #         already_blocked_with_cards
    #     )
    #     return True if damage_left >= DEFENSIVE_REACTION_THRESHOLD else False
    # else:
    #     return False
    return True


class Block:
    def __init__(self, enemy):
        self.base_value_original = np.random.randint(2, 5)
        # self.base_value_original = 3
        self.base_value = self.base_value_original
        self.enemy = enemy

        self.defensive_hand = [
            c for c in self.enemy.hand if c.card_type != CardType.defensive_reaction
        ]

        self.defensive_cards = []

        self.physical_block_cards = []

        self.arcane_block_cards = []

        self.physical_block = 0
        self.arcane_block = 0

        self.turn_bans = []

    def update_defensive_hand(self):
        self.defensive_hand = [
            c for c in self.enemy.hand if c.card_type != CardType.defensive_reaction
        ]

    def calc_total_block(self):
        # print("total_arcane_block")
        # print(self.arcane_block)
        return add_two_with_possible_none_type(
            self.calc_total_physical_block(), self.arcane_block
        )

    def clear_physical_block_cards(self):
        self.physical_block_cards = []

    def increase_physical_block_balance(self, amount=1):
        self.physical_block += amount

    def increase_arcane_block_balance(self, amount=1):
        self.arcane_block += amount

    def preserve_good_chain(self):
        if n_chance(p=0.95) or len(self.enemy.combat_chain) > 3:
            self.base_value = self.base_value_original + 3

    def reset(self):
        self.base_value = self.base_value_original
        self.defensive_cards = []
        self.physical_block = 0
        self.arcane_block = 0
        self.physical_block_cards = []

    def turn_reset(self):
        self.reset()

        self.turn_bans = []

    def defend_physical(self, physical_damage):
        self.update_defensive_hand()
        if self.enemy.modifiers.modifier_dict["dominate"] == True:
            self.defensive_cards = self.defensive_hand.copy()[:1]
        else:
            self.defensive_cards = self.defensive_hand.copy()

        np.random.shuffle(self.defensive_cards)

        print("PLAYER ATTACJK OHYSICAL BLOCK")
        print(physical_damage)

        if physical_damage is not None:
            if self.enemy.survival_mode == False:
                match physical_damage:
                    case physical_damage if physical_damage in [
                        1,
                        2,
                    ]:
                        print("here eq")
                        if (
                            physical_damage == 2
                            and len(
                                self.enemy.equipment_suite.get_possible_blocking_pieces_in_play()
                            )
                            == 0
                        ):
                            print("here eq 1")
                            self.more_elaborate_block_with_unused_cards(physical_damage)
                        else:
                            print("here eq 2")
                            self.block_with_equipment_very_basic()

                    case physical_damage if physical_damage > 2:
                        if (
                            len(self.defensive_hand) == 0
                            and self.enemy.arsenal.is_empty()
                        ):
                            print("here")
                            self.block_with_equipment_very_basic()
                        elif (
                            len(self.defensive_hand) == 0
                            and self.enemy.arsenal.is_defensive_reaction() == True
                        ):
                            pass
                        elif (
                            len(self.defensive_hand) == 0
                            and self.enemy.arsenal.is_defensive_reaction() == False
                        ):
                            print("here2")
                            self.block_with_equipment_very_basic()
                        else:
                            print("here3")
                            self.more_elaborate_block_with_unused_cards(physical_damage)
                    case _:
                        print("here4")
                        self.more_elaborate_block_with_unused_cards(physical_damage)

            elif self.enemy.survival_mode == True:
                self.block_all_physical_damage(physical_damage)

        return self.physical_block_cards

    def placeholder_block(self):
        if len(self.defensive_cards) > 0:
            return self.defensive_cards[0]
        else:
            return None

    def block_with_equipment_very_basic(self):
        equipment_available_for_block = [
            e
            for e in self.enemy.equipment_suite.get_possible_blocking_pieces_in_play()
            if e.defense > 0
        ]

        if len(equipment_available_for_block) > 0:
            c = sorted(
                equipment_available_for_block,
                key=lambda x: x.defense,
                reverse=False,
            )[0]
            c.set_defending()
            self.physical_block_cards.append(c)

            for p in self.enemy.played_cards:
                print(p.name)

    def get_cards_not_intended_to_be_used_in_combat_chain(self):
        unused_cards = []
        if self.enemy.combat_chain.get_virtual_next_link() is not None:
            unused_cards = [
                c
                for c in self.defensive_cards
                if (
                    c
                    not in (
                        self.enemy.combat_chain.get_virtual_next_link().get_play_cards()
                        + self.enemy.combat_chain.get_virtual_next_link().get_pitch_cards()
                    )
                )
            ]

            # put defensive reactions in front
            unused_cards = sorted(
                unused_cards, key=lambda x: x.card_type.value, reverse=True
            )
        return unused_cards

    def set_defensive_reaction(self, defensive_reaction):

        self.physical_block_cards.append(defensive_reaction)

    def get_cards_to_pitch_arcane_defense(self, card, pitchable_cards):
        cards_to_pitch = []

        possible_pitch_combinations = get_combinations(pitchable_cards)

        pitch_totals = self.enemy.combat_chain.calc_pitch_totals(
            possible_pitch_combinations
        )

        cards_to_pitch = determine_arcane_defense_pitch_combination(
            card.arcane_barrier, pitch_totals
        )

        return cards_to_pitch

    def defend_arcane_with_equipment(self, arcane_damage):

        arcane_damage_temp = arcane_damage

        cards_to_pitch_arcane = []

        arcane_block_threshold = 0
        match arcane_damage:
            case arcane_damage if arcane_damage in [1 or 2]:
                arcane_block_threshold = 1
            case arcane_damage if arcane_damage > 2:
                arcane_block_threshold = 2

        print("BLOCKING ARCANE WITH EQ")
        available_arcane_barriers = (
            self.enemy.equipment_suite.get_all_arcane_barriers_in_play()
        )

        print(len(available_arcane_barriers))

        if len(available_arcane_barriers) > 0:
            diffs = [
                arcane_damage - ep.arcane_barrier for ep in available_arcane_barriers
            ]
            print(diffs)
            diff_indices = np.argsort(diffs)
            print(diff_indices)

            total_pitch_available = sum([c.pitch for c in self.enemy.hand])
            print(total_pitch_available)

            for index in diff_indices:
                cards_to_pitch = []
                if diffs[index] >= 0:
                    equpiment_piece = available_arcane_barriers[index]
                    if equpiment_piece.arcane_barrier <= total_pitch_available:
                        cards_to_pitch = self.get_cards_to_pitch_arcane_defense(
                            equpiment_piece, self.enemy.hand
                        )

                        if len(cards_to_pitch) > 0:

                            self.arcane_block_cards.append(equpiment_piece)
                            for c in cards_to_pitch:
                                self.arcane_procedure(equpiment_piece, c, arcane_damage)

                                cards_to_pitch_arcane += cards_to_pitch
                                total_pitch_available -= c.pitch

                            self.enemy.virtually_played_cards.append(equpiment_piece)
                            equpiment_piece.set_defending()

                            self.enemy.resource_manager.use_floating_resources(
                                equpiment_piece.arcane_barrier
                            )

                            arcane_damage_temp -= equpiment_piece.arcane_barrier

                            print("ARCANE RESULTS")
                            print(arcane_damage)
                            print(arcane_damage_temp)
                            if arcane_damage_temp <= arcane_block_threshold:
                                break

        return self.arcane_block_cards, cards_to_pitch_arcane

    def arcane_procedure(
        self,
        equipment_piece,
        card_to_pitch,
        arcane_damage,
    ):
        self.enemy.pitch_card(card_to_pitch)
        self.increase_arcane_block_balance(amount=equipment_piece.arcane_barrier)

    def get_combinations(self, array, r=0):
        combinations = []
        if len(array) > 0:
            for i in range(1, len(array) + 1):
                combinations.append([c for c in itertools.combinations(array, i)])
        print(combinations)
        combinations = [d[0] for d in combinations]
        return combinations

    def determine_physical_defense_combination(self, combinations, physical_damage):
        # number_of_cards_used = self.enemy.intellect
        best_defense = []
        block_precision = 100
        for v in combinations:
            # number_of_cards_used_temp = len(v)
            block_precision_temp = sum([d.defense for d in v]) - physical_damage

            # if number_of_cards_used_temp <= number_of_cards_used and
            if abs(block_precision_temp) < block_precision:
                #     number_of_cards_used = number_of_cards_used_temp
                block_precision = abs(block_precision_temp)
                best_defense = v
        return best_defense

    def block_all_physical_damage(self, physical_damage):
        if physical_damage is not None:
            combinations = self.get_combinations(self.defensive_hand)
            self.physical_block_cards = self.determine_physical_defense_combination(
                physical_damage, combinations
            )

    def more_elaborate_block_with_unused_cards(self, physical_damage):
        if physical_damage is not None:
            unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
            match physical_damage:
                case physical_damage if 0 <= physical_damage < self.base_value:
                    print("attack not blocked at all")
                    self.physical_block_cards = []
                case (
                    physical_damage
                ) if self.base_value <= physical_damage < self.base_value + 3:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:1])
                        )
                    )

                    if len(unused_cards) > 0:
                        self.physical_block_cards = unused_cards[:1]
                    else:
                        self.physical_block_cards = self.defensive_cards[:1]
                case (
                    physical_damage
                ) if self.base_value + 3 <= physical_damage < self.base_value + 7:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:2])
                        )
                    )
                    if len(unused_cards) == 1:
                        self.physical_block_cards = (
                            unused_cards
                            + [
                                c for c in self.defensive_cards if c not in unused_cards
                            ][:1]
                        )
                    elif len(unused_cards) == 2:
                        self.physical_block_cards = unused_cards
                    else:
                        self.physical_block_cards = self.defensive_cards[:2]
                case (
                    physical_damage
                ) if self.base_value + 7 <= physical_damage < self.base_value + 11:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:3])
                        )
                    )
                    if len(unused_cards) == 1:
                        self.physical_block_cards = (
                            unused_cards
                            + [
                                c for c in self.defensive_cards if c not in unused_cards
                            ][:1]
                        )

                    elif len(unused_cards) == 2:
                        self.physical_block_cards = (
                            unused_cards[:2]
                            + [
                                c for c in self.defensive_cards if c not in unused_cards
                            ][:1]
                        )
                    elif len(unused_cards) == 3:
                        self.physical_block_cards = unused_cards
                    else:
                        self.physical_block_cards = self.defensive_cards[:3]

                case physical_damage if self.base_value + 11 <= physical_damage:
                    print(
                        "attack blocked with {} cards".format(len(self.defensive_cards))
                    )
                    self.physical_block_cards = self.defensive_cards[:4]
                case _:
                    self.physical_block_cards = []
