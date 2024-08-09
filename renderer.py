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
    grid,
    grid_width,
    grid_height,
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
    rect_height,
    right_edge,
    enemy_top_edge,
)

y_index = 0


class Renderer:
    def __init__(self, engine):
        self.window = pygame.display.set_mode(bounds)
        self.input_box_physical = InputBox(self.window, y=170, box_type="physical")
        self.input_box_arcane = InputBox(self.window, y=250, box_type="arcane")

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

        self.check_box_dominate = CheckBox("dominate", y=250)

        self.check_box_intimidate = CheckBox("intimidate", y=170)

        self.check_boxes = [self.check_box_dominate, self.check_box_intimidate]

    def render_background(self):
        self.window.blit(self.background, (0, 0))

    def render_end_background(self):
        self.background_bw = pygame.image.load("images/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))

    def render_floating_resources(self):
        text = font.render(
            str(self.engine.enemy.floating_resources) + " floating",
            True,
            text_color,
        )
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index),
            ),
        )

    def render_enemy(self):
        if len(self.engine.enemy.deck) > 0:
            self.window.blit(
                self.enemy_image,
                (grid.left_point(grid_width // 2 - 1), enemy_top_edge),
            ),

        # self.rect = pygame.draw.rect(
        #     self.window,
        #     "white",
        #     (
        #         grid.left_point(grid_width // 2 - 1),
        #         grid.top_point(grid_height * 0.65),
        #         card_width*card_scale+10,
        #         rect_height,
        #     ),
        # )

        text = font_card_title.render(str(self.engine.enemy.name), True, "yellow")

        self.window.blit(
            text,
            (grid.left_point(grid_width // 2 - 1), enemy_top_edge),
        )

    def render_weapons(self):
        weapons_to_render = [
            w
            for w in self.engine.enemy.weapons
            if w not in self.engine.enemy.played_cards
        ]
        for i, w in enumerate(weapons_to_render):
            if w.weapon_id == 0:
                self.render_card(w, i=1.5, y=grid.top_point(grid_height * 0.65))
            else:
                self.render_card(w, i=4, y=grid.top_point(grid_height * 0.65))

    def render_deck(self):
        text = font.render(str(len(self.engine.enemy.deck)) + " deck", True, "white")
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 1),
            ),
        )

    def render_arsenal(self):
        text = font.render(
            str(len(self.engine.enemy.arsenal)) + " arsenal", True, "white"
        )
        self.window.blit(
            text,
            (
                grid.left_point(grid_width // 2 - 1),
                grid.top_point(grid_height * 0.9),
            ),
        )

    def render_hand(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " hand", True, "white")
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 2),
            ),
        )

    def render_banished_zone(self):
        n_banished_cards = 0
        for k, v in self.engine.enemy.banished_zone.items():
            n_banished_cards += len(v)
        text = font.render(str(n_banished_cards) + " banished", True, "white")
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 3),
            ),
        )

    def render_pitch(self):
        if len(self.engine.enemy.pitched_cards) > 0:
            for i, pc in enumerate(self.engine.enemy.pitched_cards):
                self.render_card(pc, x=right_edge)

        text = font.render(
            str(len(self.engine.enemy.pitched_cards)) + " pitch",
            True,
            "white",
        )
        i = 5
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 4),
            ),
        )

    def render_card(self, current_card, i=0, x=None, y=None):
        # offset_factor = 10*i if i != 0 else 0

        if y is None:
            vert_card_grid_point = grid.top_point(6)
            vert_pos = vert_card_grid_point
        else:
            vert_pos = y

        if x is None:
            hor_card_grid_point = 1 + int(i) * 2.5
            hor_pos = grid.left_point(hor_card_grid_point)
        else:
            hor_pos = x

        print(current_card)
        current_card.image = pygame.transform.scale(
            current_card.image,
            (int(card_width * card_scale), int(card_height * card_scale)),
        )
        self.window.blit(current_card.image, (hor_pos, vert_pos))

        # NAME
        self.rect = pygame.draw.rect(
            self.window,
            card_colors[current_card.color.name],
            (hor_pos, vert_pos, card_width * 0.75, 25),
        )

        text = font_card_title.render(str(current_card.name), True, "black")

        self.window.blit(text, (hor_pos, vert_pos))

        # CLASS
        factor_keyword = 1.8
        self.rect = pygame.draw.rect(
            self.window,
            "blue",
            (
                hor_pos,
                vert_pos + card_height // 2 + rect_height,
                card_width * 0.75,
                rect_height,
            ),
        )

        if current_card.card_class.name != "generic":
            text = font_card_title.render(
                str(current_card.card_class.name), True, "white"
            )

            self.window.blit(
                text,
                (
                    hor_pos,
                    vert_pos + card_height // 2 + rect_height,
                ),
            )

        # KEYWORDS

        self.rect = pygame.draw.rect(
            self.window,
            "green",
            (
                hor_pos,
                vert_pos + card_height // 2 + rect_height * 2,
                card_width * 0.75,
                rect_height,
            ),
        )

        if current_card.keywords[0].name != "no_keyword":
            text = font_card_title.render(
                str(current_card.keywords[0].name), True, "black"
            )

            self.window.blit(
                text,
                (
                    hor_pos,
                    vert_pos + card_height // 2 + rect_height * 2,
                ),
            )

        # TYPE
        self.rect = pygame.draw.rect(
            self.window,
            "white",
            (
                hor_pos,
                vert_pos + card_height // 2 + rect_height * 3,
                card_width * 0.75,
                rect_height,
            ),
        )

        text = font_card_title.render(str(current_card.card_type.name), True, "black")

        self.window.blit(
            text,
            (
                hor_pos,
                vert_pos + card_height // 2 + rect_height * 3,
            ),
        )

        # POWER
        text = font.render(str(current_card.physical), True, "yellow")

        self.window.blit(
            text,
            (
                hor_pos,
                vert_pos + card_height // 2 + rect_height * 4,
            ),
        )

        # ARCANE POWER
        if current_card.arcane > 0:
            text = font.render("+{}".format(str(current_card.arcane)), True, "green")

            self.window.blit(
                text,
                (
                    hor_pos + arcane_offset,
                    vert_pos + card_height // 2 + rect_height * 4,
                ),
            )

        # DEFENSE
        text = font.render(str(current_card.defense), True, "black")

        self.window.blit(
            text,
            (
                hor_pos + card_width // 1.7,
                vert_pos + card_height // 2 + rect_height * 4,
            ),
        )

        # PITCH
        text = font.render(
            str(current_card.pitch), True, card_colors[current_card.color.name]
        )

        self.window.blit(
            text,
            (
                hor_pos,
                vert_pos - rect_height * 2,
            ),
        )

        # COST
        text = font.render(str(current_card.cost), True, "red")
        self.window.blit(
            text,
            (
                hor_pos + card_width // 1.7,
                vert_pos - rect_height * 2,
            ),
        )

    def render_enemy_life(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " life", True, "white")
        self.window.blit(
            text,
            (
                grid.left_point(7),
                grid.top_point(2),
            ),
        )

    def render_enemy_play(self):
        for i, current_card in enumerate(self.engine.enemy.played_cards):
            self.render_card(current_card, i=i)

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

            self.window.blit(
                text,
                (
                    grid.left_point(1),
                    grid.top_point(1),
                ),
            )

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

        self.render_weapons()

        self.render_arsenal()

        self.render_deck()

        self.render_enemy()

        self.render_hand()

        self.render_banished_zone()

        self.render_pitch()

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
