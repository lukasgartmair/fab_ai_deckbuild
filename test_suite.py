#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:13:25 2023

@author: lukasgartmair
"""

from playstyle import CardType
import unittest
from engine import GameEngine, GameStateMachine
import numpy as np
from enemy import Stance, Enemy
import random
from modifiers import Modifiers
from deck import Deck
from card import Card
from utils import get_combinations
import pygame
from combat_chain import CombatChain

n_runs = 10
n_turns = 5
n_iterations = 4


class TestMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_combat_chain(self):
        n_hand = 4
        test_hand = Deck(deck_size=n_hand).cards
        for t in test_hand:
            t.card_type = CardType.attack_action

        test_combat_chain = CombatChain(test_hand)

        counter = 0
        for t in test_hand:
            test_cards_to_pitch = test_combat_chain.get_cards_to_pitch(t)
            counter += len(test_cards_to_pitch)
            print(test_cards_to_pitch)
            test_combat_chain.remove_pitch_from_card_lists(test_cards_to_pitch)
        self.assertTrue(counter <= n_hand)

        test_combat_chain = CombatChain(test_hand)

        test_combat_chain = CombatChain(test_hand)
        test_combat_chain.get_valid_combinations(test_combat_chain.playable_cards)
        self.assertTrue(len(test_combat_chain.valid_combinations) > 0)

        test_combo = test_combat_chain.valid_combinations[0]
        test_chain_link = test_combat_chain.calc_chain_link(test_combo)

        test_combat_chain.add_link(test_chain_link)
        self.assertTrue(test_combat_chain.is_empty() == False)
        self.assertTrue(test_combat_chain.chain[0].play == test_chain_link.play)

        test_combat_chain = CombatChain(test_hand)
        test_combat_chain.calc_combat_chains(n=10)

        print()
        print(test_combat_chain.get_length())

    # def test_get_pitch_combinations(self):
    #     test_array = [1, 2, 3, 4]

    #     combinations = get_combinations(test_array)

    #     self.assertEqual(len(combinations), 15)

    #     test_array = [1]

    #     combinations = get_combinations(test_array)

    #     self.assertEqual(len(combinations), 1)

    #     test_array = []

    #     combinations = get_combinations(test_array)

    #     self.assertEqual(len(combinations), 0)

    # def test_deck_draw_mechanics(self):
    #     pygame.mixer.pause()
    #     deck_size = 5
    #     test_deck = Deck(deck_size=deck_size)

    #     ref_cards = test_deck.cards[-3:1]

    #     for i, tc in enumerate(test_deck.cards):
    #         pass
    #         # print(i)
    #         # print(tc.name)

    #     # print()
    #     test_card = Card()
    #     # print("test card name")
    #     # print(test_card.name)

    #     test_deck.put_to_bottom(test_card)
    #     # print()
    #     # print("after insertion to bottom")

    #     for i, tc in enumerate(test_deck.cards):
    #         pass
    #         # print(i)
    #         # print(tc.name)

    #     self.assertEqual(test_deck.cards[0], test_card)
    #     self.assertEqual(len(test_deck.cards), deck_size + 1)
    #     # print()
    #     top_card = test_deck.draw_top_card()
    #     # print(test_card.name)
    #     # print(top_card.name)
    #     self.assertTrue(test_card.name != top_card.name)
    #     self.assertEqual(test_deck.get_length(), deck_size)

    #     # print()
    #     # print("after drawing")
    #     for i, tc in enumerate(test_deck.cards):
    #         pass
    #         # print(i)
    #         # print(tc.name)

    #     self.assertTrue(top_card not in test_deck.cards)

    #     top_cards_drawn = test_deck.draw_top_cards(n=2)
    #     # print()
    #     for i, l in enumerate(ref_cards):
    #         self.assertTrue(ref_cards[i] == top_cards_drawn[i])

    # def test_deckbuilding(self):
    #     for i in range(1):
    #         self.engine = GameEngine()
    #         # print(self.engine.enemy.player_class)

    # # # def test_test(self):
    # # #     pass

    # def test_gameplay(self):
    #     self.engine = GameEngine()
    #     pygame.mixer.pause()

    #     for n in range(n_runs):
    #         if n != 0:
    #             self.engine.advance_level()

    #         if self.engine.state_machine.current_state == GameStateMachine.starting:
    #             self.engine.state_machine.start_game()

    #         # print(self.engine.level_manager.current_level)

    #         # print(self.engine.state_machine.current_state)
    #         while self.engine.state_machine.current_state == GameStateMachine.playing:
    #             # print("--------------------")
    #             # print("TURN")
    #             # print(self.engine.level_manager.turn_index)

    #             if self.engine.enemy.stance == Stance.defend:
    #                 for j in range(random.randint(1, n_iterations + 1)):
    #                     # print("MOVE")
    #                     # print(self.engine.level_manager.move_index)

    #                     pyhsical = np.random.randint(0, 6)
    #                     arcane = np.random.randint(0, 3)
    #                     self.engine.player_attack.set_values(
    #                         inp_box=None, physical=pyhsical, arcane=arcane
    #                     )
    #                     self.engine.play(self.engine.player_attack)

    #                     self.engine.player_attack.reset()

    #                     # print("enemy life:")
    #                     # print(self.engine.enemy.life_counter.life)
    #                     # print()

    #                     self.engine.check_win_condition()
    #                     if (
    #                         self.engine.state_machine.current_state
    #                         == GameStateMachine.ended
    #                     ):
    #                         break
    #                     else:
    #                         continue  # only executed if the inner loop did NOT break
    #                     break  # only executed if the inner loop DID break

    #                 self.engine.enemy.finish_turn()
    #                 self.engine.finish_turn()

    #             elif self.engine.enemy.stance == Stance.attack:
    #                 # print("MOVE")
    #                 # print(self.engine.level_manager.move_index)

    #                 for j in range(n_iterations):
    #                     if self.engine.enemy.check_if_further_attack_possible() == True:
    #                         self.engine.play()

    #                         # print("enemy life:")
    #                         # print(self.engine.enemy.life_counter.life)

    #                         self.engine.check_win_condition()
    #                         if (
    #                             self.engine.state_machine.current_state
    #                             == GameStateMachine.ended
    #                         ):
    #                             break

    #                     else:
    #                         continue  # only executed if the inner loop did NOT break
    #                     break  # only executed if the inner loop DID break

    #                 self.engine.enemy.finish_turn()
    #                 self.engine.finish_turn()

    # self.engine.analyzer.analyze_game_data()


if __name__ == "__main__":
    unittest.main()
