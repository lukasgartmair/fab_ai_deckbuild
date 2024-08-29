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
from input_box import InputBox
from playstyle import Keyword, CardType
from colors import color_palette
from card import CardColor
from utils import blit_text
import image
from playstyle import PlayerClass, Talent
import PygameUtils as pu
import random

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
    font_lore,
    font_header,
    font_header2,
)

y_index = 0

button_size = 25

enemy_message_x = grid.left_point(1)
enemy_message_y = grid.top_point(1)


class Renderer:
    def __init__(self, engine):
        self.window = pygame.display.set_mode(bounds)

        pygame.display.set_caption("There will be Flesh and Blood")

        self.input_box_physical = InputBox(self.window, y=170, box_type="physical")
        self.input_box_arcane = InputBox(self.window, y=250, box_type="arcane")

        self.engine = engine

        self.background = pygame.image.load("images/backgrounds/background4.png")
        self.background = pygame.transform.smoothscale(
            self.background, self.window.get_size()
        )

        self.check_box_dominate = CheckBox("dominate", y=250)

        self.check_box_intimidate = CheckBox("intimidate", y=170)

        self.check_boxes = [self.check_box_dominate, self.check_box_intimidate]

        self.button_up = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(0),
            button_size,
            button_size,
        )
        self.button_down = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(0) + button_size + 5,
            button_size,
            button_size,
        )

    def render_background(self):
        self.window.blit(self.background, (0, 0))

    def render_end_background(self):
        self.background_bw = pygame.image.load("images/backgrounds/background_bw.png")
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

    def render_enemy(self, color=color_palette.white):
        self.window.blit(
            self.engine.enemy.image,
            (grid.left_point(grid_width // 2 - 1), enemy_top_edge),
        ),

        text = font_card_title.render(str(self.engine.enemy.name), True, color)

        self.window.blit(
            text,
            (grid.left_point(grid_width // 2 - 1), enemy_top_edge - 25),
        )

        if self.engine.enemy.talent != Talent.no_talent:
            text = font_card_title.render(
                "# "
                + str(self.engine.level_manager.current_level)
                + " - "
                + str(self.engine.enemy.talent.name).upper(),
                True,
                color,
            )

            self.window.blit(
                text,
                (
                    grid.left_point(grid_width // 2 - 1),
                    enemy_top_edge + card_height * 0.76,
                ),
            )

        text = font_card_title.render(
            "     " + str(self.engine.enemy.player_class.name).upper(),
            True,
            color,
        )

        self.window.blit(
            text,
            (grid.left_point(grid_width // 2 - 1), enemy_top_edge + card_height * 0.84),
        )

    def render_enter_new_level(self):
        text = font_header2.render(
            "This is room #" + str(self.engine.level_manager.current_level).upper(),
            True,
            pygame.Color(color_palette.white),
        )

        self.window.blit(
            text,
            (grid.left_point(7), grid.top_point(3)),
        )

    def render_enter_next_level(self):
        text = font.render(
            "Enter room #" + str(self.engine.level_manager.current_level).upper(),
            True,
            pygame.Color(color_palette.white),
        )

        self.window.blit(
            text,
            (grid.left_point(7), grid.top_point(3)),
        )

    def render_create_deck_message(self):
        text = font_header2.render(
            "Opening door to the next room...",
            True,
            pygame.Color(color_palette.white),
        )

        self.window.blit(
            text,
            (grid.left_point(6), grid.top_point(6)),
        )

    def render_lore(self):
        blit_text(
            self.window,
            self.engine.enemy.lore,
            (grid.left_point(5), grid.top_point(5)),
            font_lore,
        )

    def render_weapons(self):
        for i, w in enumerate(self.engine.enemy.weapons):
            if w not in self.engine.enemy.played_cards:
                if w.weapon_id == 0:
                    self.render_card(
                        w,
                        x=grid.left_point(grid_width // 2 - 1) - card_width,
                        y=grid.top_point(grid_height * 0.65),
                    )
                else:
                    self.render_card(
                        w,
                        x=grid.left_point(grid_width // 2 - 1) + card_width,
                        y=grid.top_point(grid_height * 0.65),
                    )

    def render_no_moves_left(self):
        message = ""
        if (
            self.engine.enemy.stance == Stance.attack
            and self.engine.enemy.further_attack_possible == False
        ):
            message = "'I wont't further attack you - Let me defend now!'"
        elif (
            self.engine.enemy.stance == Stance.defend
            and self.engine.enemy.further_defense_possible == False
        ):
            message = "'You broke my defense - Hit me again or change my stance'"

        text = font.render(
            message,
            True,
            pygame.Color(color_palette.color3),
        )
        self.window.blit(
            text,
            (enemy_message_x, enemy_message_y),
        )

    def render_boost(self):
        message = ""
        if (
            self.engine.enemy.player_class == PlayerClass.mechanologist
            and self.engine.enemy.stance == Stance.attack
        ):
            if self.engine.enemy.boost.activated == True:
                message = "'BOOOOOST mechanic activated!'"
            elif self.engine.enemy.boost.failed == True:
                message = "'boost FAILED!'"

        text = font.render(
            message,
            True,
            pygame.Color(color_palette.color3),
        )
        self.window.blit(
            text,
            (enemy_message_x, grid.top_point(3)),
        )

    def render_deck(self):
        text = font.render(
            str(self.engine.enemy.deck.get_length()) + " deck",
            True,
            pygame.Color(color_palette.text_color),
        )
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 1),
            ),
        )

    def render_arsenal(self):
        text = font.render(
            str(len(self.engine.enemy.arsenal)) + " arsenal",
            True,
            pygame.Color(color_palette.text_color),
        )
        self.window.blit(
            text,
            (
                grid.left_point(grid_width // 2 - 1),
                grid.top_point(grid_height * 0.94),
            ),
        )

    def render_hand(self):
        text = font.render(
            str(len(self.engine.enemy.hand)) + " hand",
            True,
            pygame.Color(color_palette.text_color),
        )
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
        text = font.render(
            str(n_banished_cards) + " banished",
            True,
            pygame.Color(color_palette.text_color),
        )
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 14),
            ),
        )

    def render_pitch(self):
        if len(self.engine.enemy.pitched_cards) > 0:
            for i, pc in enumerate(self.engine.enemy.pitched_cards):
                self.render_card(pc, x=right_edge)

        text = font.render(
            str(len(self.engine.enemy.pitched_cards)) + " pitch",
            True,
            pygame.Color(color_palette.white),
        )
        i = 5
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 4),
            ),
        )

    def render_graveyard(self):
        text = font.render(
            str(len(self.engine.enemy.graveyard)) + " graveyard",
            True,
            pygame.Color(color_palette.text_color),
        )
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 13),
            ),
        )

    def render_equipment(self):
        for i, eq in enumerate(self.engine.enemy.equipment_suite.get_pieces_in_play()):
            if eq not in self.engine.enemy.played_cards:
                self.render_card(
                    eq,
                    x=grid.left_point(eq.equipment_type.value)
                    + eq.equipment_type.value * 2,
                    y=grid.top_point(12),
                )

    def render_boost_counter(self):
        # print(self.engine.enemy.boost_counter)
        if self.engine.enemy.player_class == PlayerClass.mechanologist:
            text = font.render(
                str(self.engine.enemy.boost.counter) + " boost counter",
                True,
                pygame.Color(color_palette.text_color),
            )
            self.window.blit(
                text,
                (
                    right_edge,
                    grid.top_point(y_index + 15),
                ),
            )

    def render_action_points(self):
        text = font.render(
            str(self.engine.enemy.action_points) + " action pts.",
            True,
            pygame.Color(color_palette.text_color),
        )
        self.window.blit(
            text,
            (
                right_edge,
                grid.top_point(y_index + 3),
            ),
        )

    def render_card_image(self, card):
        card.image = pygame.transform.scale(
            card.image,
            (int(card_width * card_scale), int(card_height * card_scale)),
        )

        self.window.blit(card.image, (card.x, card.y))

    def render_card_name(self, card):
        self.rect = pygame.draw.rect(
            self.window,
            card_colors[card.color.name],
            (card.x, card.y, card_width * 0.75, 25),
        )

        if card.color == CardColor.yellow:
            text = font_card_title.render(
                str(card.name), True, pygame.Color(color_palette.black)
            )
        else:
            text = font_card_title.render(
                str(card.name), True, pygame.Color(color_palette.white)
            )

        self.window.blit(text, (card.x, card.y))

    def render_card_class(self, card):
        self.rect = pygame.draw.rect(
            self.window,
            "blue",
            (
                card.x,
                card.y + card_height // 2 + rect_height,
                card_width * 0.75,
                rect_height,
            ),
        )

        if card.card_class.name != "generic":
            text = font_card_title.render(
                str(card.card_class.name),
                True,
                pygame.Color(color_palette.white),
            )

            self.window.blit(
                text,
                (
                    card.x,
                    card.y + card_height // 2 + rect_height,
                ),
            )

    def render_card_keywords(self, card):
        self.rect = pygame.draw.rect(
            self.window,
            pygame.Color(color_palette.green),
            (
                card.x,
                card.y + card_height // 2 + rect_height * 2,
                card_width * 0.75,
                rect_height,
            ),
        )

        if card.keywords[0] != Keyword.no_keyword:
            text = font_card_title.render(
                str(card.keywords[0].name),
                True,
                pygame.Color(color_palette.white),
            )

            self.window.blit(
                text,
                (
                    card.x,
                    card.y + card_height // 2 + rect_height * 2,
                ),
            )

    def render_card_type(self, card):
        self.rect = pygame.draw.rect(
            self.window,
            pygame.Color(color_palette.white),
            (
                card.x,
                card.y + card_height // 2 + rect_height * 3,
                card_width * 0.75,
                rect_height,
            ),
        )

        text = font_card_title.render(
            str(card.card_type.name), True, pygame.Color(color_palette.black)
        )

        self.window.blit(
            text,
            (
                card.x,
                card.y + card_height // 2 + rect_height * 3,
            ),
        )

    def render_power(self, card):
        text = font.render(str(card.physical), True, pygame.Color(color_palette.white))

        self.window.blit(
            text,
            (
                card.x,
                card.y + card_height // 2 + rect_height * 4,
            ),
        )

    def render_arcane_power(self, card):
        if card.arcane > 0:
            text = font.render(
                "+{}".format(str(card.arcane)),
                True,
                pygame.Color(color_palette.green),
            )

            self.window.blit(
                text,
                (
                    card.x + arcane_offset,
                    card.y + card_height // 2 + rect_height * 4,
                ),
            )

    def render_defense(self, card):
        text = font.render(str(card.defense), True, pygame.Color(color_palette.black))

        self.window.blit(
            text,
            (
                card.x + card_width // 1.7,
                card.y + card_height // 2 + rect_height * 4,
            ),
        )

    def render_card_pitch(self, card):
        text = font.render(str(card.pitch), True, card_colors[card.color.name])

        self.window.blit(
            text,
            (
                card.x,
                card.y - rect_height * 2,
            ),
        )

    def render_arcane_barrier(self, card):
        if card.arcane_barrier > 0:
            text = font_card_title.render(
                "Arcane Barrier " + str(card.arcane_barrier),
                True,
                color_palette.black,
            )

            self.window.blit(
                text,
                (
                    card.x,
                    card.y - rect_height * 2,
                ),
            )

    def render_cost(self, card):
        text = font.render(str(card.cost), True, pygame.Color(color_palette.color2))
        self.window.blit(
            text,
            (
                card.x + card_width // 1.7,
                card.y - rect_height * 2,
            ),
        )

    def render_card(self, card, i=0, x=None, y=None):
        if y is None:
            vert_card_grid_point = grid.top_point(6)
            card.y = vert_card_grid_point
        else:
            card.y = y

        if x is None:
            hor_card_grid_point = 1 + int(i) * 2.5
            card.x = grid.left_point(hor_card_grid_point)
        else:
            card.x = x

        self.render_card_image(card)

        self.render_card_name(card)

        self.render_card_class(card)

        self.render_card_keywords(card)

        self.render_card_type(card)

        if card.card_type not in [CardType.equipment]:
            self.render_power(card)

        self.render_arcane_power(card)

        if card.card_type not in [CardType.weapon]:
            self.render_defense(card)
        if card.card_type not in [CardType.equipment]:
            self.render_card_pitch(card)

        if card.card_type not in [CardType.weapon, CardType.equipment]:
            self.render_card_pitch(card)

        if card.card_type in [CardType.equipment]:
            self.render_arcane_barrier(card)

        if card.card_type not in [CardType.equipment]:
            self.render_cost(card)

    def render_enemy_life_counter(self):
        if self.engine.state_machine.current_state == self.engine.state_machine.playing:
            self.button_up.draw(self.window)
            self.button_down.draw(self.window)

        text = font.render(
            "HP : " + str(self.engine.enemy.life_counter.life),
            True,
            pygame.Color(color_palette.white),
        )
        self.window.blit(
            text,
            (
                grid.left_point(11),
                grid.top_point(0),
            ),
        )

    def render_enemy_play(self):
        for i, card in enumerate(self.engine.enemy.played_cards):
            self.render_card(card, i=i)

    def render_turn_text(self):
        if self.engine.state_machine.current_state == self.engine.state_machine.playing:
            color = None

            if self.engine.enemy.stance == Stance.defend:
                color = pygame.Color(color_palette.white)

            else:
                color = pygame.Color(color_palette.color2)

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
                    grid.top_point(0),
                ),
            )

    def render_win(self):
        self.bg = pygame.image.load("images/backgrounds/background3.png")
        self.bg = pygame.transform.smoothscale(self.bg, self.window.get_size())
        self.window.blit(self.bg, (0, 0))

        message = "You won...but what..."
        text = font.render(message, True, color_palette.color3)
        self.window.blit(text, (grid.left_point(5), grid.top_point(5)))

        msg = "The " + self.engine.win_condition.name.replace("_", " ") + "..."
        text = font.render(msg, True, color_palette.color3)
        self.window.blit(text, (grid.left_point(8), grid.top_point(3)))

        self.render_enemy_life_counter()
        self.render_enemy()

    def render_start_screen(self):
        self.bg = pygame.image.load("images/backgrounds/background2.png")
        self.bg = pygame.transform.smoothscale(self.bg, self.window.get_size())
        self.window.blit(self.bg, (0, 0))

        message = "Enter the abyss.."
        text = font_header.render(message, True, color_palette.color3)
        self.window.blit(text, (grid.left_point(1), grid.top_point(1)))

    def update_display(self):
        pygame.display.flip()
