#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:55:49 2024

@author: lukasgartmair
"""

import numpy as np
import itertools
from deck import Deck
from pile import Pile
from enum import Enum
from playstyle import Keyword, PlayerClass, Talent, CardType, get_playstyle
from equipment import EquipmentSuite
from weapon import initialize_weapons
import random
from fantasynames.fantasy_identity import FantasyIdentity
from block import Block
from utils import n_chance, shift_list
from ability import Ability
from life_counter import LifeCounter
import pygame
from sound import Sound
from combat_chain import CombatChain
from lore import lore_dict
from modifiers import Modifiers
import image
from action_point_manager import ActionPointManager
from resource_manager import ResourceManager
from arsenal import Arsenal
from stance import StanceStateMachine, Stance


class Enemy:
    playKey = None

    def __init__(self, player_class=PlayerClass.generic):
        self.player_class = player_class

        self.identity = FantasyIdentity(self.player_class)
        self.name = self.identity.name
        self.race = self.identity.race
        self.image_path = self.player_class.name + "/" + self.identity.image_number
        self.image = image.get_image(self.image_path)

        # if n_chance(p=0.5):
        #     self.stance = Stance.defend
        # else:
        #     self.stance = Stance.attack
        self.stance_state_machine = StanceStateMachine()

        self.intellect = 4
        self.talent = random.choice(list(Talent))
        self.starting_life = random.randint(20, 41)
        self.hand = []
        self.pile = Pile()
        self.play_key = pygame.K_SPACE

        self.soul = []

        self.playstyle = get_playstyle(self.player_class)
        self.original_deck = Deck(self.player_class, self.playstyle)

        self.deck = self.original_deck

        self.graveyard = []
        self.banished_zone = {}
        self.banished_zone["intimidated_cards"] = []

        self.arsenal = Arsenal()

        self.weapons = initialize_weapons(self.playstyle)

        self.equipment_suite = EquipmentSuite()

        self.resource_manager = ResourceManager()

        self.pitched_cards = []
        self.played_cards = []

        self.action_point_manager = ActionPointManager()

        self.combat_chain = CombatChain(
            self.hand,
            arsenal=self.arsenal,
            weapons=self.weapons,
        )
        self.block = Block(self)
        self.modifiers = Modifiers()

        self.ability = Ability()

        self.sound = Sound()

        self.life_counter = LifeCounter(self.starting_life, self.sound)

        if self.player_class.name in lore_dict:
            self.lore = random.choice(lore_dict[self.player_class.name])
        else:
            self.lore = ""
        self.lore = self.lore.replace("{}", self.name)

        self.survival_mode = False
        self.check_if_in_survival_mode()

    def check_if_in_survival_mode(self):
        if self.life_counter.life <= 5:
            self.survival_mode = True
        else:
            self.survival_mode = False

    def initialize_play(self):
        self.draw()
        self.reset_play()

    def reset_play(self):
        self.combat_chain.turn_reset()
        self.resource_manager.reset()
        self.action_point_manager.reset()

    def fill_arsenal(self):
        if len(self.hand) > 0:
            c = self.hand[0]
            self.arsenal.fill(c)
            self.hand.remove(c)

    def switch_to_defense(self):
        if self.arsenal.is_empty():
            self.fill_arsenal()
        self.check_if_in_survival_mode()
        self.draw()

    def start_move(self):
        # self.combat_chain.update_combat_chain()
        pass

    def finish_move(self):
        pass

    def start_turn(self):
        self.combat_chain.update_combat_chain()

    def finish_turn(self):
        self.reset_play()

        for card in self.played_cards:
            if card.card_type not in [CardType.weapon, CardType.equipment]:
                self.graveyard.append(card)

            elif card.card_type == CardType.equipment:
                card.finish_defensive_turn()
                if card.destroyed == True:
                    self.graveyard.append(card)

        for pc in self.pitched_cards:
            self.deck.put_to_bottom(pc)

        self.played_cards = []
        self.pitched_cards = []

        if "intimidated_cards" in self.banished_zone:
            self.hand += self.banished_zone["intimidated_cards"]

            self.banished_zone["intimidated_cards"] = []

        self.block.reset()

        self.stance_state_machine.change_stance()

        if self.stance_state_machine.stance == StanceStateMachine.defense:
            self.switch_to_defense()

        if self.stance_state_machine.stance == StanceStateMachine.attack:
            self.combat_chain.update_combat_chain()

    def check_if_further_attack_reaction_possible(self):
        if any(
            [True for c in self.hand if c.card_type == CardType.attack_reaction]
            + [self.arsenal.is_attack_reaction()]
        ):
            return True

    def check_if_further_attack_possible(self):
        self.combat_chain.print_combat_chain()
        if (
            self.combat_chain.is_empty()
            or self.combat_chain.end_reached()
            or self.action_point_manager.has_action_points_left() == False
        ):
            # print("NO attack possible")
            return False

        else:
            # print("attack possible")
            return True

    def check_if_further_defensive_reaction_possible(self):
        if any(
            [True for c in self.hand if c.card_type == CardType.defensive_reaction]
            + [self.arsenal.is_defensive_reaction()]
        ):
            return True

    def check_if_further_defense_possible(self):
        if (
            len(self.hand) == 0
            and len(self.equipment_suite.get_possible_blocking_pieces_in_play()) == 0
        ):
            if self.arsenal.is_empty():
                return False
            elif self.arsenal.is_empty() == False:
                if self.arsenal[0].card_type != CardType.defensive_reaction:
                    return True
            else:
                return True

    def draw(self):
        print("enemy is drawing")
        if self.deck.get_length() > 0:
            n_cards_to_draw = self.intellect - len(self.hand)
            if n_cards_to_draw > 0:
                if self.deck.get_length() < n_cards_to_draw:
                    n_cards_to_draw = self.deck.get_length()

                drawn_cards = self.deck.draw_top_cards(n=n_cards_to_draw)

                if type(drawn_cards) is list:
                    self.hand += drawn_cards

                self.sound.play_draw_cards(n_cards=len(drawn_cards))

        else:
            print("can't draw anymore, deck fatigued")

    def remove_card_from_hand(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def pitch_cards(self):
        print("-----------------")
        print("hand")
        for h in self.hand:
            print(h.name)
        print("pitch")
        for k, p in self.combat_chain.chain[self.combat_chain.iterator].pitch.items():
            for v in p:
                print(v.name)
                self.pitch_card(v)
        print()

    def remove_played_cards(self):
        for p in self.played_cards:
            if p in self.hand:
                self.remove_card_from_hand(p)
            if self.arsenal.is_in_arsenal(p):
                self.arsenal.remove_card(p)

    def pitch_card(self, c):
        self.pitched_cards.append(c)
        self.resource_manager.pitch_floating_resources(c.pitch)
        # self.hand.remove(c)

    def print_cards(self):
        print("HAND")
        for c in self.hand:
            print(c.name)

        print("ARSENAL")
        for c in self.arsenal.arsenal:
            print(c.name)

    def defend(self, player_attack):
        self.combat_chain.update_combat_chain()
        if len(self.hand) > 0:
            if self.modifiers.modifier_dict["intimidate"] == True:
                random_banished_card = random.choice(self.hand)

                self.banished_zone["intimidated_cards"].append(random_banished_card)
                self.hand.remove(random_banished_card)

        # TODO arcane or physical first?
        if n_chance(p=0.5):
            if player_attack.arcane is not None:
                self.block.defend_arcane(player_attack)
            self.block.defend_physical(player_attack)
        else:
            self.block.defend_physical(player_attack)
            if player_attack.arcane is not None:
                self.sound.play_flip_card()
                self.block.defend_arcane(player_attack)

        for bc in self.block.physical_block_cards:
            # print(bc)
            self.played_cards.append(bc)
            # print("enemy defends with")
            # print(bc.name)
            # print("defense: {}".format(bc.defense))
            if bc in self.hand:
                self.hand.remove(bc)

            if bc in self.arsenal.arsenal:
                self.arsenal.remove_card(bc)

        if len(self.block.physical_block_cards) > 0:
            self.sound.play_block()

        self.life_counter.calculate_life(player_attack, self.block)
        self.block.reset()

    def perform_defensive_reaction(self):
        print("defensive_reaction")

    def perform_attack_reaction(self):
        print("attack reaction")

    def base_attack(self):
        chain_link = self.combat_chain.get_next_link()

        # self.combat_chain.print_combat_chain()
        for k, c in chain_link.play.items():
            self.played_cards.append(c)
            self.pitch_cards()
            self.remove_played_cards()
            self.resource_manager.use_floating_resources(c.cost)
            self.action_point_manager.use_action_points()
            self.action_point_manager.handle_keywords(c)

        self.sound.play_attack(c)

        return c

    def class_specific_helper_1(self, card):
        pass

    def perform_attack(self):
        if self.check_if_further_attack_possible() == True:
            c = self.base_attack()
            # TODO find a cleaner implementation for this in te action point manager
            self.class_specific_helper_1(c)

            self.combat_chain.increase_iterator()
