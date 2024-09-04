#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 19:54:38 2024

@author: lukasgartmair
"""

import numpy as np
from utils import n_chance, add_two_with_possible_none_type
from card import CardType
import itertools


class Block:
    def __init__(self, enemy):
        self.base_value_original = np.random.randint(2, 5)
        # self.base_value_original = 3
        self.base_value = self.base_value_original
        self.enemy = enemy
        self.defensive_cards = []

        self.physical_block_cards = []

        self.arcane_block_cards = []

        self.physical_block = 0
        self.arcane_block = 0

    def calc_total_block(self):
        # print("total_arcane_block")
        # print(self.arcane_block)
        return add_two_with_possible_none_type(
            self.calc_total_physical_block(), self.arcane_block
        )

    def calc_total_physical_block(self):
        # print("total_physical_block")
        # print(sum([p.defense for p in self.physical_block_cards]))
        return sum([p.defense for p in self.physical_block_cards])

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

    def defend_physical(self, player_attack):
        if self.enemy.modifiers.modifier_dict["dominate"] == True:
            self.defensive_cards = self.enemy.hand.copy()[:1] + [
                d
                for d in self.enemy.arsenal.get_arsenal().copy()
                if d.card_type == CardType.defensive_reaction
            ]
        else:
            self.defensive_cards = self.enemy.hand.copy() + [
                d
                for d in self.enemy.arsenal.get_arsenal().copy()
                if d.card_type == CardType.defensive_reaction
            ]

        np.random.shuffle(self.defensive_cards)

        if player_attack.physical is not None:
            if self.enemy.survival_mode == False:
                match player_attack.physical:
                    case player_attack.physical if player_attack.physical in [1, 2]:
                        print("here eq")
                        if (
                            player_attack.physical == 2
                            and len(
                                self.enemy.equipment_suite.get_possible_blocking_pieces_in_play()
                            )
                            == 0
                        ):
                            print("here eq 1")
                            self.more_elaborate_block_with_unused_cards(player_attack)
                        else:
                            print("here eq 2")
                            self.block_with_equipment_very_basic()

                    case player_attack.physical if player_attack.physical > 2:
                        if len(self.enemy.hand) == 0 and self.enemy.arsenal.is_empty():
                            print("here")
                            self.block_with_equipment_very_basic()
                        elif (
                            len(self.enemy.hand) == 0
                            and (self.enemy.arsenal.is_empty() == False)
                            and self.enemy.arsenal.get_arsenaled_card.card_type
                            != CardType.defensive_reaction
                        ):
                            print("here2")
                            self.block_with_equipment_very_basic()
                        else:
                            print("here3")
                            self.more_elaborate_block_with_unused_cards(player_attack)
                    case _:
                        print("here4")
                        self.more_elaborate_block_with_unused_cards(player_attack)

            elif self.enemy.survival_mode == True:
                self.block_all_physical_damage(player_attack)

            self.calc_total_physical_block()

    def placeholder_block(self):
        if len(self.defensive_cards) > 0:
            return self.defensive_cards[0]
        else:
            return None

    def block_with_equipment_very_basic(self):
        if len(self.enemy.equipment_suite.get_possible_blocking_pieces_in_play()) > 0:
            c = sorted(
                self.enemy.equipment_suite.get_possible_blocking_pieces_in_play(),
                key=lambda x: x.defense,
                reverse=False,
            )[0]
            c.set_defending()
            self.physical_block_cards.append(c)

    def get_cards_not_intended_to_be_used_in_combat_chain(self):
        unused_cards = [
            c
            for c in self.defensive_cards
            if (
                c not in [cp.play for cp in self.enemy.combat_chain.chain.values()]
                and c not in [cp.pitch for cp in self.enemy.combat_chain.chain.values()]
            )
        ]

        # put defensive reactions in front
        unused_cards = sorted(
            unused_cards, key=lambda x: x.card_type.value, reverse=True
        )
        return unused_cards

    # def defend_arcane_with_equipment(self, player_attack):
    #     print("DEFENDING ARCANE")

    #     unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()

    #     available_arcane_barriers = [
    #         ep
    #         for ep in self.enemy.equipment_suite.get_pieces_in_play()
    #         if ep.arcane_barrier > 0
    #     ]

    #     match player_attack.arcane:
    #         case player_attack.arcane if player_attack.arcane == 1:
    #             matching_barriers = [a for a in available_arcane_barriers if a.arcane_barrier == 1]
    #             if len(matching_barriers) > 0:
    #                 self.arcane_block_cards.append()

    #     diffs = [
    #         abs(player_attack.arcane - ab.arcane_barrier) for ab in available_arcane_barriers
    #     ]

    #     min_index = diffs.index(min(diffs))

    #     self.arcane_block_cards

    #     # TODO
    #     pass

    def arcane_procedure(self, card, player_attack, pitch_value):
        self.enemy.pitch_card(card)
        self.enemy.resource_manager.use_floating_resources(player_attack.arcane)
        self.increase_arcane_block_balance(amount=pitch_value)

    def defend_arcane(self, player_attack):
        print("DEFENDING ARCANE")

        unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
        # print(self.enemy.combat_chain)
        # print(unused_cards)

        match player_attack.arcane:
            case player_attack.arcane if player_attack.arcane == 1 or 2:
                print("defending one arcane attack")
                if self.enemy.resource_manager.floating_resources > 0:
                    self.enemy.resource_manager.use_floating_resources(
                        player_attack.arcane
                    )
                    self.increase_arcane_block_balance(amount=player_attack.arcane)
                else:
                    if len(unused_cards) > 0:
                        unused_cards = sorted(
                            unused_cards, key=lambda x: x.pitch, reverse=False
                        )
                        card = unused_cards[0]
                        pitch_value = card.pitch

                        self.arcane_procedure(card, player_attack, pitch_value)

                    elif len(self.enemy.hand) > 0:
                        sorted_hand = sorted(
                            self.enemy.hand, key=lambda x: x.pitch, reverse=False
                        )

                        card = sorted_hand[0]
                        pitch_value = card.pitch

                        self.arcane_procedure(card, player_attack, pitch_value)

            case player_attack.arcane if player_attack.arcane == 3 or 4:
                print("defending one arcane attack")
                if self.enemy.resource_manager.floating_resources > 0:
                    self.enemy.resource_manager.use_floating_resources(
                        player_attack.arcane
                    )
                    self.increase_arcane_block_balance(amount=player_attack.arcane)
                else:
                    if len(unused_cards) > 0:
                        unused_cards = sorted(
                            unused_cards, key=lambda x: x.pitch, reverse=True
                        )
                        card = unused_cards[0]
                        pitch_value = card.pitch

                    elif len(self.enemy.hand) > 0:
                        sorted_hand = sorted(
                            self.enemy.hand, key=lambda x: x.pitch, reverse=True
                        )

                        card = sorted_hand[0]
                        pitch_value = card.pitch

                    self.enemy.pitch_card(card)
                    self.enemy.resource_manager.use_floating_resources(
                        player_attack.arcane
                    )
                    self.increase_arcane_block_balance(amount=pitch_value)

    def get_combinations(self, array, r=0):
        combinations = []
        if len(array) > 0:
            for i in range(1, len(array) + 1):
                combinations.append([c for c in itertools.combinations(array, i)])
        combinations = [d[0] for d in combinations]
        return combinations

    def determine_physical_defense_combination(self, player_attack, combinations):
        # number_of_cards_used = self.enemy.intellect
        best_defense = []
        block_precision = 100
        for v in combinations:
            # number_of_cards_used_temp = len(v)
            block_precision_temp = sum([d.defense for d in v]) - player_attack.physical

            # if number_of_cards_used_temp <= number_of_cards_used and
            if abs(block_precision_temp) < block_precision:
                #     number_of_cards_used = number_of_cards_used_temp
                block_precision = abs(block_precision_temp)
                best_defense = v
        return best_defense

    def block_all_physical_damage(self, player_attack):
        if player_attack.physical is not None:
            combinations = self.get_combinations(self.enemy.hand)
            self.physical_block_cards = self.determine_physical_defense_combination(
                player_attack, combinations
            )

    def more_elaborate_block_with_unused_cards(self, player_attack):
        if player_attack.physical is not None:
            unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
            match player_attack.physical:
                case player_attack.physical if 0 <= player_attack.physical < self.base_value:
                    print("attack not blocked at all")
                    self.physical_block_cards = []
                case player_attack.physical if self.base_value <= player_attack.physical < self.base_value + 3:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:1])
                        )
                    )

                    if len(unused_cards) > 0:
                        self.physical_block_cards = unused_cards[:1]
                    else:
                        self.physical_block_cards = self.defensive_cards[:1]
                case player_attack.physical if self.base_value + 3 <= player_attack.physical < self.base_value + 7:
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
                case player_attack.physical if self.base_value + 7 <= player_attack.physical < self.base_value + 11:
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

                case player_attack.physical if self.base_value + 11 <= player_attack.physical:
                    print(
                        "attack blocked with {} cards".format(len(self.defensive_cards))
                    )
                    self.physical_block_cards = self.defensive_cards[:4]
                case _:
                    self.physical_block_cards = []
