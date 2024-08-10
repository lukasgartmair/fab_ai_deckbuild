#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 19:54:38 2024

@author: lukasgartmair
"""

import numpy as np
from utils import n_chance, add_two_with_possible_none_type
from card import CardType


class Block:
    def __init__(self, enemy):
        # self.base_value_original = np.random.randint(3, 5)
        self.base_value_original = 3
        self.base_value = self.base_value_original
        self.enemy = enemy
        self.defensive_cards = []

        self.physical_block_cards = []

        self.physical_block = 0
        self.arcane_block = 0

    def calc_total_block(self):
        print("total_arcane_block")
        print(self.arcane_block)
        return add_two_with_possible_none_type(
            self.calc_total_physical_block(), self.arcane_block
        )

    def calc_total_physical_block(self):
        print("total_physical_block")
        print(sum([p.defense for p in self.physical_block_cards]))
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
        self.defensive_cards = self.enemy.hand.copy() + [
            d
            for d in self.enemy.arsenal.copy()
            if d.card_type == CardType.defensive_reaction
        ]

        np.random.shuffle(self.defensive_cards)

        self.more_elaborate_block_with_unused_cards(player_attack)
        self.calc_total_physical_block()

    def placeholder_block(self):
        if len(self.defensive_cards) > 0:
            return self.defensive_cards[0]
        else:
            return None

    def get_cards_not_intended_to_be_used_in_combat_chain(self):
        unused_cards = [
            c
            for c in self.defensive_cards
            if (
                c not in [cp["attack"] for cp in self.enemy.combat_chain.values()]
                and c not in [cp["pitch"] for cp in self.enemy.combat_chain.values()]
            )
        ]

        # put defensive reactions in front
        unused_cards = sorted(
            unused_cards, key=lambda x: x.card_type.value, reverse=True
        )
        return unused_cards

    def defend_arcane(self, player_attack):
        print("DEFENDING ARCANE")

        unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
        print(self.enemy.combat_chain)
        print(unused_cards)

        unused_cards_sorted_by_pitch_asc = sorted(
            unused_cards, key=lambda x: x.pitch, reverse=False
        )

        # TODO INCLUDE ABS FROM EQUIPMENT

        match player_attack.arcane:
            case player_attack.arcane if player_attack.arcane == 1 or 2:
                print("defending one arcane attack")
                if self.enemy.floating_resources > 0:
                    self.enemy.use_floating_resources(player_attack.arcane)
                    self.increase_arcane_block_balance(amount=player_attack.arcane)
                else:
                    print("pitch something here")
                    if len(self.enemy.hand) > 0:
                        sorted_hand = sorted(
                            self.enemy.hand, key=lambda x: x.pitch, reverse=False
                        )
                        pitch_value = sorted_hand[0].pitch
                        self.enemy.pitch_card(sorted_hand[0])
                        self.enemy.use_floating_resources(player_attack.arcane)
                        self.increase_arcane_block_balance(amount=pitch_value)

            case player_attack.arcane if player_attack.arcane == 3 or 4:
                print("defending one arcane attack")
                if self.enemy.floating_resources > 0:
                    self.enemy.use_floating_resources(player_attack.arcane)
                    self.increase_arcane_block_balance(amount=player_attack.arcane)
                else:
                    print("pitch something here")
                    if len(self.enemy.hand) > 0:
                        sorted_hand = sorted(
                            self.enemy.hand, key=lambda x: x.pitch, reverse=True
                        )
                        pitch_value = sorted_hand[0].pitch
                        self.enemy.pitch_card(sorted_hand[0])
                        self.enemy.use_floating_resources(player_attack.arcane)
                        self.increase_arcane_block_balance(amount=pitch_value)

    def more_elaborate_block_with_unused_cards(self, player_attack):
        if player_attack.physical is not None:
            unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
            match player_attack.physical:
                case player_attack.physical if 0 <= player_attack.physical < self.base_value:
                    print("attack not blocked at all")
                    return []
                case player_attack.physical if self.base_value <= player_attack.physical < self.base_value + 3:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:1])
                        )
                    )

                    if len(unused_cards) > 0:
                        return unused_cards[:1]
                    else:
                        self.physical_block_cards = self.defensive_cards[:1]
                case player_attack.physical if self.base_value + 3 <= player_attack.physical < self.base_value + 7:
                    print(
                        "attack blocked with {} cards".format(
                            len(self.defensive_cards[:2])
                        )
                    )
                    if len(unused_cards) == 1:
                        return (
                            unused_cards
                            + [
                                c for c in self.defensive_cards if c not in unused_cards
                            ][:1]
                        )
                    elif len(unused_cards) == 2:
                        return unused_cards
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
        else:
            self.physical_block_cards = []
