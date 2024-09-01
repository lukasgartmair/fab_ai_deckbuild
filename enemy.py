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
from attack import Attack
from pitch import Pitch
from combat_chain import CombatChain
from lore import lore_dict
from modifiers import Modifiers
import image


class Stance(Enum):
    defend = 0
    attack = 1


class Enemy:
    playKey = None

    def __init__(self, player_class=PlayerClass.generic):
        self.player_class = player_class

        self.identity = FantasyIdentity(self.player_class)
        self.name = self.identity.name
        self.race = self.identity.race
        self.image_path = (
            "images/" + self.player_class.name + "/" + self.identity.image_number
        )
        self.image = image.load_image(self.image_path)

        if n_chance(p=0.5):
            self.stance = Stance.defend
        else:
            self.stance = Stance.attack

        self.intellect = 4
        self.talent = random.choice(list(Talent))
        self.starting_life = 20
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

        self.arsenal = []

        self.weapons = initialize_weapons(self.playstyle)

        self.equipment_suite = EquipmentSuite()

        self.further_attack_possible = True
        self.further_defense_possible = True

        self.floating_resources = 0

        self.pitched_cards = []
        self.played_cards = []

        self.combat_chain = CombatChain(self)
        self.block = Block(self)
        self.attack = Attack(self)
        self.pitch = Pitch(self)

        self.modifiers = Modifiers()

        self.ability = Ability()

        self.sound = Sound()

        self.life_counter = LifeCounter(self.starting_life, self.sound)

        if self.player_class.name in lore_dict:
            self.lore = random.choice(lore_dict[self.player_class.name])
        else:
            self.lore = ""
        self.lore = self.lore.replace("{}", self.name)

        self.action_points = 0

        self.survival_mode = False
        self.check_if_in_survival_mode()

    def check_if_in_survival_mode(self):
        if self.life_counter.life <= 5:
            self.survival_mode = True
        else:
            self.survival_mode = False

    def initialize_play(self):
        self.draw()
        if self.stance == Stance.attack:
            self.combat_chain.calc_combat_chain()
        self.reset_play()

    def reset_play(self):
        self.floating_resources = 0
        self.reset_action_points()
        self.further_attack_possible = True
        self.further_defense_possible = True

    def reset_action_points(self):
        self.action_points = 1

    def get_action_points(self, amount=1):
        self.action_points += amount

    def use_action_points(self, amount=1):
        if self.action_points >= amount:
            self.action_points -= amount
            return True
        else:
            return False

    def arsenal_empty(self):
        if len(self.arsenal) == 0:
            return True
        else:
            return False

    def fill_arsenal(self):
        if len(self.hand) > 0:
            c = self.hand[0]
            self.arsenal.append(c)
            self.hand.remove(c)

    def change_stance(self):
        if self.stance == Stance.defend:
            self.stance = Stance.attack
            self.combat_chain.calc_combat_chain()
            # print("combat_chain")
            # print(self.combat_chain)

            self.sound.play_change_stance_to_attack()

        elif self.stance == Stance.attack:
            if self.arsenal_empty():
                self.fill_arsenal()

            self.stance = Stance.defend
            self.check_if_in_survival_mode()
            self.draw()
            self.combat_chain.calc_combat_chain()

    def finish_move(self):
        pass

    def start_move(self):
        self.check_if_further_move_possible()

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

        self.combat_chain.reset()

        self.further_attack_possible = True
        self.further_defense_possible = True

        if "intimidated_cards" in self.banished_zone:
            self.hand += self.banished_zone["intimidated_cards"]

            self.banished_zone["intimidated_cards"] = []

        self.block.reset()

        self.change_stance()

    def check_if_further_move_possible(self):
        if self.stance == Stance.attack:
            self.check_if_further_attack_possible()
        elif self.stance == Stance.defend:
            self.check_if_further_defense_possible()

    def check_if_further_attack_possible(self):
        print(self.combat_chain.is_empty())
        print(self.combat_chain.end_reached())
        print(self.action_points == 0)
        if (
            self.combat_chain.is_empty()
            or self.combat_chain.end_reached()
            or self.action_points == 0
        ):
            self.further_attack_possible = False
        else:
            print("attack possible")

    def check_if_further_defense_possible(self):
        if (
            len(self.hand) == 0
            and len(self.equipment_suite.get_possible_blocking_pieces_in_play()) == 0
        ):
            if len(self.arsenal) == 0:
                self.further_defense_possible = False
            elif len(self.arsenal) == 1:
                if self.arsenal.card_type != CardType.defensive_reaction:
                    self.further_defense_possible = False

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

    def pitch_floating_resources(self, amount):
        self.floating_resources += amount

    def use_floating_resources(self, amount):
        self.floating_resources -= amount
        if self.floating_resources < 0:
            self.floating_resources = 0

    def remove_card_from_hand(self, card):
        if card in self.hand:
            self.hand.remove(card)

    def check_if_attack(self):
        if self.combat_chain.has_content():
            if self.combat_chain.iterator_in_chain():
                print(self.action_points)
                if self.action_points > 0:
                    return True
        else:
            return False

    def pitch_cards(self):
        for p in self.combat_chain.chain[self.combat_chain.iterator]["pitch"]:
            self.pitch_card(p)

    def remove_played_cards(self):
        for p in self.played_cards:
            if p in self.hand:
                self.remove_card_from_hand(p)
            if p in self.arsenal:
                self.arsenal.remove(p)

    def handle_go_again(self, c):
        if Keyword.go_again in c.keywords:
            self.get_action_points()

    def pitch_card(self, c):
        self.pitched_cards.append(c)
        self.pitch_floating_resources(c.pitch)
        self.hand.remove(c)

    def print_cards(self):
        print("HAND")
        for c in self.hand:
            print(c.name)

        print("ARSENAL")
        for c in self.arsenal:
            print(c.name)

    def defend(self, player_attack):
        self.combat_chain.calc_combat_chain()
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

            if bc in self.arsenal:
                self.arsenal.remove(bc)

        if len(self.block.physical_block_cards) > 0:
            self.sound.play_block()

        self.life_counter.calculate_life(player_attack, self.block)
        self.block.reset()

    def perform_attack(self):
        self.combat_chain.calc_combat_chain()

        print(self.combat_chain)
        if self.check_if_attack():
            c = self.attack.base_attack()

            self.combat_chain.increase_iterator()

        else:
            self.further_attack_possible = False
