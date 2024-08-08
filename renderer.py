#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 19:03:39 2024

@author: lukasgartmair
"""

import pygame

from card import card_colors
from check_box import CheckBox
from enemy import Stance
from engine import GameState
from input_box import InputBox


from settings import (
    player_1_color,
    player_2_color,
    bounds,
    width_references,
    FPS,
    height_references,
    card_height,
    card_width,
    card_scale,
    font_card_title,
    font,
    text_color,
    text_offset_piles,
    arcane_offset,
)


class Renderer:
    def __init__(self, engine):
        self.window = pygame.display.set_mode(bounds)
        self.input_box_physical = InputBox(self.window, box_type="physical")
        self.input_box_arcane = InputBox(self.window, y=220, box_type="arcane")

        self.engine = engine

        self.background = pygame.image.load("images/background.png")
        self.background = pygame.transform.smoothscale(
            self.background, self.window.get_size()
        )

        self.enemy_image = pygame.image.load(
            "images/"
            + self.engine.enemy.player_class.name
            + "/"
            + self.engine.enemy.image
        )
        self.enemy_image = pygame.transform.scale(
            self.enemy_image,
            (int(card_height * 0.8 * card_scale), int(card_height * card_scale)),
        )

        self.check_box_dominate = CheckBox("dominate")

        self.check_box_intimidate = CheckBox("intimidate", y=120)

        self.check_boxes = [self.check_box_dominate, self.check_box_intimidate]

    def render_background(self):
        self.window.blit(self.background, (0, 0))

    def render_end_background(self):
        self.background_bw = pygame.image.load("images/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))

    def render_attack_value(self, player_attack_value):
        text = font.render(
            str(player_attack_value) + " attack value",
            True,
            text_color,
        )
        self.window.blit(
            text,
            (
                width_references["pitch"] - 25,
                height_references[0] + text_offset_piles * 2,
            ),
        )

    def render_floating_resources(self):
        text = font.render(
            str(self.engine.enemy.floating_resources) + " floating resources",
            True,
            text_color,
        )
        self.window.blit(
            text,
            (
                width_references["pitch"] - 25,
                height_references[0] + text_offset_piles * 2,
            ),
        )

    def render_deck_pile(self):
        if len(self.engine.enemy.deck) > 0:
            self.window.blit(
                self.enemy_image, (width_references["pile"], height_references[0])
            )

        text = font.render(str(len(self.engine.enemy.deck)) + " deck", True, "white")
        self.window.blit(
            text, (width_references["pile"], height_references[0] + text_offset_piles)
        )

    def render_hand(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " hand", True, "white")
        self.window.blit(
            text,
            (width_references["hand"], height_references[0] + text_offset_piles * 2),
        )

    def render_banished_zone(self):
        n_banished_cards = 0
        for k, v in self.engine.enemy.banished_zone.items():
            n_banished_cards += len(v)
        text = font.render(str(n_banished_cards) + " banished", True, "white")
        self.window.blit(text, (width_references["banished"], height_references[0] * 2))

    def render_pitch_pile(self):
        if len(self.engine.enemy.pitched_cards) > 0:
            for i, pc in enumerate(self.engine.enemy.pitched_cards):
                self.render_card("pitch", pc)

        text = font.render(
            str(len(self.engine.enemy.pitched_cards)) + " pitch",
            True,
            "white",
        )
        self.window.blit(
            text, (width_references["pitch"], height_references[0] + text_offset_piles)
        )

    def render_card(self, i, current_card):
        offset_factor = 1.35

        print(current_card)
        current_card.image = pygame.transform.scale(
            current_card.image,
            (int(card_width * card_scale), int(card_height * card_scale)),
        )
        self.window.blit(
            current_card.image, (width_references[str(i)], height_references[0])
        )

        # NAME
        self.rect = pygame.draw.rect(
            self.window,
            card_colors[current_card.color.name],
            (width_references[str(i)], height_references[0], card_width * 0.75, 25),
        )

        text = font_card_title.render(str(current_card.name), True, "black")

        self.window.blit(text, (width_references[str(i)], height_references[0]))

        # CLASS
        factor_keyword = 1.8
        self.rect = pygame.draw.rect(
            self.window,
            "blue",
            (
                width_references[str(i)],
                height_references[0] + card_height // factor_keyword,
                card_width * 0.75,
                25,
            ),
        )

        if current_card.card_class.name != "generic":
            text = font_card_title.render(
                str(current_card.card_class.name), True, "white"
            )

            self.window.blit(
                text,
                (
                    width_references[str(i)],
                    height_references[0] + card_height // factor_keyword,
                ),
            )

        # KEYWORDS
        factor_keyword = 1.6

        self.rect = pygame.draw.rect(
            self.window,
            "green",
            (
                width_references[str(i)],
                height_references[0] + card_height // factor_keyword,
                card_width * 0.75,
                25,
            ),
        )

        if current_card.keywords[0].name != "no_keyword":
            text = font_card_title.render(
                str(current_card.keywords[0].name), True, "black"
            )

            self.window.blit(
                text,
                (
                    width_references[str(i)],
                    height_references[0] + card_height // factor_keyword,
                ),
            )

        # TYPE
        self.rect = pygame.draw.rect(
            self.window,
            "white",
            (
                width_references[str(i)],
                height_references[0] + card_height // 1.475,
                card_width * 0.75,
                25,
            ),
        )

        text = font_card_title.render(str(current_card.card_type.name), True, "black")

        self.window.blit(
            text,
            (width_references[str(i)], height_references[0] + card_height // 1.475),
        )

        # POWER
        text = font.render(str(current_card.power), True, "yellow")

        self.window.blit(
            text,
            (
                width_references[str(i)],
                height_references[0] + (card_height // offset_factor),
            ),
        )

        # ARCANE POWER
        if current_card.arcane > 0:
            text = font.render("+{}".format(str(current_card.arcane)), True, "green")

            self.window.blit(
                text,
                (
                    width_references[str(i)] + arcane_offset,
                    height_references[0] + (card_height // offset_factor),
                ),
            )

        # DEFENSE
        text = font.render(str(current_card.defense), True, "black")

        self.window.blit(
            text,
            (
                width_references[str(i)] + card_width // 2,
                height_references[0] + (card_height // offset_factor),
            ),
        )

        # PITCH
        text = font.render(
            str(current_card.pitch), True, card_colors[current_card.color.name]
        )

        self.window.blit(
            text,
            (
                width_references[str(i)],
                height_references[0]
                - (card_height - card_height // offset_factor - 30),
            ),
        )

        # COST
        text = font.render(str(current_card.cost), True, "red")
        self.window.blit(
            text,
            (
                width_references[str(i)] + card_width // 2,
                height_references[0]
                - (card_height - card_height // offset_factor - 30),
            ),
        )

    def render_enemy_life(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " life", True, "white")
        self.window.blit(
            text,
            (width_references["hand"], height_references[0] + text_offset_piles * 2),
        )

    def render_enemy_play(self):
        for i, current_card in enumerate(self.engine.enemy.played_cards):
            self.render_card(i, current_card)

    def render_turn_text(self):
        if self.engine.state == GameState.playing:
            color = None

            if self.engine.enemy.stance == Stance.defend:
                color = player_2_color

            else:
                color = player_1_color

            text = font.render(
                "{}".format(self.engine.enemy.name)
                + " is "
                + (self.engine.enemy.stance.name + "ing").upper(),
                True,
                color,
            )

            self.window.blit(text, (20, 50))

    def render_win(self):
        self.render_end_background()

        message = "The " + self.engine.currentPlayer.name + " trancended!"
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))

    def render_start_screen(self):
        self.background_start = pygame.image.load("images/background_start.png")
        self.window.blit(self.background_start, (0, 0))

        message = "Enter the abyss.."
        text = font.render(message, True, (100, 0, 0))
        self.window.blit(text, (20, 50))
        pygame.display.update()

    def render(self):
        self.render_background()

        self.render_enemy_play()

        self.render_floating_resources()

        self.render_deck_pile()

        self.render_hand()

        self.render_banished_zone()

        self.render_pitch_pile()

        self.render_turn_text()

        if self.engine.state == GameState.ended:
            self.render_win()

        pygame.display.update()

    def render_initial_game_state(self):
        self.render_background()

        message = ""
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))

        self.input_box_physical.render()

        self.render()
