#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 19:54:38 2024

@author: lukasgartmair
"""

import numpy as np
from utils import n_chance


class EnemyBlock:
    def __init__(self, enemy_hand, combat_chain):
        self.base_value_original = np.random.randint(3, 5)
        self.base_value = self.base_value_original
        self.enemy_hand = enemy_hand
        self.combat_chain = combat_chain

    def preserve_good_chain(self):
        if n_chance(p=0.95) or len(self.combat_chain) > 3:
            self.base_value = self.base_value_original + 3

    def reset(self):
        self.base_value = self.base_value_original

    def defend_physical(self, player_attack):
        return self.more_elaborate_block_with_unused_cards(player_attack)

    def placeholder_block(self):
        if len(self.enemy_hand) > 0:
            return self.enemy_hand[0]
        else:
            return None

    def get_cards_not_intended_to_be_used_in_combat_chain(self):
        unused_cards = [
            c
            for c in self.enemy_hand
            if (
                c not in [cp["attack"] for cp in self.combat_chain.values()]
                and c not in [cp["pitch"] for cp in self.combat_chain.values()]
            )
        ]

        # put defensive reactions in front
        unused_cards = sorted(
            unused_cards, key=lambda x: x.card_type.value, reverse=True
        )
        return unused_cards

    def more_elaborate_block_with_unused_cards(self, player_attack):
        if player_attack.physical is not None:
            unused_cards = self.get_cards_not_intended_to_be_used_in_combat_chain()
            match player_attack.physical:
                case player_attack.physical if 0 <= player_attack.physical < self.base_value:
                    print("attack not blocked at all")
                    return []
                case player_attack.physical if self.base_value <= player_attack.physical < self.base_value + 3:
                    print(
                        "attack blocked with {} cards".format(len(self.enemy_hand[:1]))
                    )

                    if len(unused_cards) > 0:
                        return unused_cards[:1]
                    else:
                        return self.enemy_hand[:1]
                case player_attack.physical if self.base_value + 3 <= player_attack.physical < self.base_value + 7:
                    print(
                        "attack blocked with {} cards".format(len(self.enemy_hand[:2]))
                    )
                    if len(unused_cards) == 1:
                        return (
                            unused_cards
                            + [c for c in self.enemy_hand if c != unused_cards[0]][:1]
                        )
                    elif len(unused_cards) == 2:
                        return unused_cards
                    else:
                        return self.enemy_hand[:2]
                case player_attack.physical if self.base_value + 7 <= player_attack.physical < self.base_value + 11:
                    print(
                        "attack blocked with {} cards".format(len(self.enemy_hand[:3]))
                    )
                    if len(unused_cards) == 1:
                        return (
                            unused_cards
                            + [c for c in self.enemy_hand if c != unused_cards[0]][:1]
                        )
                    elif len(unused_cards) == 2:
                        return (
                            unused_cards[:2]
                            + [c for c in self.enemy_hand if c != unused_cards[0]][:1]
                        )
                    elif len(unused_cards) == 3:
                        return unused_cards
                    else:
                        return self.enemy_hand[:3]

                case player_attack.physical if self.base_value + 11 <= player_attack.physical:
                    print("attack blocked with {} cards".format(len(self.enemy_hand)))
                    return self.enemy_hand[:4]
                case _:
                    return []
        else:
            return []