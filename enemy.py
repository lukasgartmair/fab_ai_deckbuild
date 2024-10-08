#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:55:49 2024

@author: lukasgartmair
"""

from deck import Deck
from pile import Pile
from playstyle import PlayerClass, Talent, CardType, get_playstyle
from equipment import EquipmentSuite
from weapon import initialize_weapons
import random
from fantasynames.fantasy_identity import FantasyIdentity
from block import Block
from utils import n_chance
from ability import Ability
from life_counter import LifeCounter
import pygame
from sound import Sound
from combat_chain import CombatChain, StepType
from lore import lore_dict
from modifiers import Modifiers
import image
from action_point_manager import ActionPointManager
from resource_manager import ResourceManager
from arsenal import Arsenal
from stance import StanceStateMachine


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

        self.intellect = 4
        self.talent = random.choice(list(Talent))
        # self.starting_life = random.randint(20, 41)
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

        self.arsenal = Arsenal()

        self.weapons = initialize_weapons(self.playstyle)

        self.equipment_suite = EquipmentSuite()

        self.resource_manager = ResourceManager()

        self.pitched_cards = []
        self.played_cards = []

        self.virtually_played_cards = []

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

        self.survival_mode = True
        self.check_if_in_survival_mode()

        self.stance_state_machine = StanceStateMachine(self)

        self.start_turn()

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

    def initial_switch_to_offense(self):

        self.finish_turn()

        self.played_cards = []

        self.virtually_played_cards = []

        self.pitched_cards = []

        self.block.turn_reset()

        for i in range(25):
            self.combat_chain.update_combat_chain()
            if self.combat_chain.is_empty() == False:
                break

    def handle_equipment_counters(self):
        for card in [c for c in self.played_cards if c.card_type == CardType.equipment]:
            card.finish_defensive_move()
            if card.destroyed == True:
                self.graveyard.append(card)

    def start_move(self):
        pass

    def finish_move(self):
        self.block.clear_physical_block_cards()

    def start_turn(self):
        print("started turn")
        self.combat_chain.update_combat_chain()

    def finish_turn(self):
        self.reset_play()

        for card in self.played_cards:
            if card.card_type not in [CardType.weapon, CardType.equipment]:
                self.graveyard.append(card)

        for pc in self.pitched_cards:
            self.deck.put_to_bottom(pc)

        self.played_cards = []

        self.virtually_played_cards = []

        self.pitched_cards = []

        if "intimidated_cards" in self.banished_zone:
            self.hand += self.banished_zone["intimidated_cards"]

            self.banished_zone["intimidated_cards"] = []

        self.block.reset()

        self.switch_to_defense()

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
            or self.combat_chain.get_current_link().go_to_reaction_step() == True
        ):
            print("NO attack possible")
            return False

        else:
            # print("attack possible")
            return True

    def check_if_further_attack_reaction_planned(self, link):
        if link is not None:
            return True if link.has_attack_reactions_left() == True else False
        else:
            return False

    def check_if_further_defense_possible(self):
        if (
            len([c for c in self.hand if c.card_type != CardType.defensive_reaction])
            == 0
            and len(self.equipment_suite.get_possible_blocking_pieces_in_play()) == 0
        ):
            print("no further defense possible")
            return False
        else:
            return True

    def check_if_further_defensive_reaction_possible(self):
        if any(
            [True for c in self.hand if c.card_type == CardType.defensive_reaction]
            + [self.arsenal.is_defensive_reaction()]
        ):
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

    def print_cards(self, c):
        print("-----------------")
        print("hand")
        for h in self.hand:
            print(h.name)
        print("pitch")
        for p in self.pitch_cards:
            print(p.name)
        print()

    def remove_played_cards(self):
        for p in self.played_cards:
            self.remove_card_from_hand(p)
            if self.arsenal.is_in_arsenal(p):
                self.arsenal.remove_card(p)

    def pitch_card(self, c):
        self.pitched_cards.append(c)
        self.resource_manager.pitch_floating_resources(c.pitch)
        try:
            self.hand.remove(c)

        except:
            print()
            print(c.name)
            self.print_cards()

    def print_cards(self):
        print("HAND")
        for c in self.hand:
            print(c.name)

        print("ARSENAL")
        for c in self.arsenal.arsenal:
            print(c.name)

    def defend(self, player_attack):
        if len(self.hand) > 0:
            if self.modifiers.modifier_dict["intimidate"] == True:
                random_banished_card = random.choice(self.hand)

                self.banished_zone["intimidated_cards"].append(random_banished_card)
                self.hand.remove(random_banished_card)

        # TODO arcane or physical first?

        physical_damage = player_attack.physical.get_latest_step_value()
        arcane_damage = player_attack.arcane.get_latest_step_value()

        if player_attack.physical.has_to_be_defended():
            physical_blocking_cards = self.block.defend_physical(physical_damage)
            player_attack.physical.set_block(physical_blocking_cards)

        if player_attack.arcane.has_to_be_defended():
            arcane_block_cards, arcane_pitch = self.block.defend_arcane_with_equipment(
                arcane_damage
            )
            player_attack.arcane.set_block(
                arcane_block_cards, arcane_pitch=arcane_pitch
            )
            self.sound.play_flip_card()

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
        else:
            self.sound.play_not_possible()

    def perform_defensive_reaction(self, player_attack):

        if player_attack.physical.still_has_to_be_defended_with_reaction() == True:
            defensive_reaction = None
            affordable = False
            max_def_react_cost = 3
            defensive_reactions = [
                c
                for c in self.hand + self.arsenal.get_arsenal()
                if (
                    c.card_type == CardType.defensive_reaction
                    and c.cost <= max_def_react_cost
                )
            ]

            if len(defensive_reactions) > 0:

                defensive_reaction = random.choice(defensive_reactions)

                if defensive_reaction.cost > 0:
                    cards_to_pitch = self.combat_chain.get_cards_to_pitch(
                        defensive_reaction,
                        [c for c in self.hand if c != defensive_reaction],
                    )

                    if len(cards_to_pitch) > 0:
                        affordable = True

                        for c in cards_to_pitch:
                            self.pitch_card(c)

                        self.resource_manager.use_floating_resources(
                            defensive_reaction.cost
                        )

                    else:
                        affordable = False
                        self.sound.play_not_possible()

                elif defensive_reaction.cost == 0:
                    affordable = True

                if affordable == True:
                    self.played_cards.append(defensive_reaction)
                    player_attack.physical.set_block([defensive_reaction])

                    if defensive_reaction in self.hand:
                        self.hand.remove(defensive_reaction)

                    if defensive_reaction in self.arsenal.arsenal:
                        self.arsenal.remove_card(defensive_reaction)

                    self.block.set_defensive_reaction(defensive_reaction)

            else:
                self.sound.play_not_possible()
        else:
            self.sound.play_not_possible()

    def base_attack(self, chain_link, reaction=False):
        virtual_next_step_type = chain_link.get_virtual_next_step()

        if virtual_next_step_type is not None:
            if (
                reaction == False
                and virtual_next_step_type.step_type == StepType.attack_reaction
            ):
                self.sound.play_not_possible()
                return
            if reaction == True and virtual_next_step_type.step_type == StepType.attack:
                self.sound.play_not_possible()
                return

            c = chain_link.get_next_step()

            self.played_cards.append(c.play)

            for p in c.pitch:
                self.pitch_card(p)

            print("NOT ENOUGH RESOURCES")

            print(self.resource_manager.floating_resources)
            print(c.play.cost)

            self.resource_manager.use_floating_resources(c.play.cost)

            # TODO
            if reaction == False:
                self.action_point_manager.handle_keywords(c.play)

            self.sound.play_attack(c.play)

            if reaction == False:

                self.action_point_manager.use_action_points()

            self.print_cards()
            self.remove_played_cards()

            c.mark_done()

            chain_link.check_if_end_reached()
            if chain_link.end_reached == True:
                self.combat_chain.increase_iterator()

            # TODO find a cleaner implementation for this in te action point manager
            self.class_specific_helper_1(c)

    def class_specific_helper_1(self, card):
        pass

    def get_chain_link(self):
        chain_link = self.combat_chain.get_current_link()
        if chain_link is not None:
            chain_link.check_if_end_reached()
            if chain_link.end_reached == True:
                chain_link = self.combat_chain.get_next_link()
        return chain_link

    def perform_attack(self, reaction=False):
        chain_link = self.get_chain_link()

        if reaction == False:
            if self.check_if_further_attack_possible() == True:
                self.base_attack(chain_link, reaction=False)
        else:
            if self.check_if_further_attack_reaction_planned(chain_link) == True:
                self.base_attack(chain_link, reaction=True)
