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
from playstyle import PlayerClass, Talent
import PygameUtils as pu
from playmat import Playmat
from equipment import EquipmentType

from settings import (
    playmat_grid as grid,
    bounds,
    FPS,
    card_height,
    card_width,
    card_scale,
    font_card_title,
    font,
    text_color,
    arcane_offset,
    rect_height,
    font_lore,
    font_header,
    font_header2,
    font_playmat,
)

y_index = 0
button_size = 25
alpha = 0.7
enemy_message_x = grid.left_point(1)
enemy_message_y = grid.top_point(1)
combat_chain_spacing = 10
hp_height_index = 0.5
arcane_offset = arcane_offset


class Renderer:
    def __init__(self, engine):
        self.window = pygame.display.set_mode(bounds)
        self.engine = engine
        self.playmat = Playmat()

        pygame.display.set_caption("There will be Flesh and Blood")

        self.input_box_physical = InputBox(
            self.window,
            x=self.playmat.positions.inputs.x,
            y=self.playmat.positions.inputs.y,
            box_type="physical",
        )
        self.input_box_arcane = InputBox(
            self.window,
            x=self.playmat.positions.inputs.x,
            y=self.playmat.positions.inputs.y
            + self.playmat.get_vertical_spacing() * 1.5,
            box_type="arcane",
        )

        self.input_boxes = [
            self.input_box_physical,
            self.input_box_arcane,
        ]

        self.background = None
        self.load_background()

        self.card_back = pygame.image.load("images/card_backs/card_back.png")
        self.card_back = pygame.transform.scale(
            self.card_back,
            (int(card_width), int(card_height)),
        )

        self.check_box_dominate = CheckBox(
            "dominate",
            x=self.playmat.positions.check_boxes.x,
            y=self.playmat.positions.check_boxes.y,
        )

        self.check_box_intimidate = CheckBox(
            "intimidate",
            x=self.playmat.positions.check_boxes.x,
            y=self.playmat.positions.check_boxes.y
            + self.playmat.get_vertical_spacing() * 1.5,
        )

        self.check_boxes = [self.check_box_dominate, self.check_box_intimidate]

        self.button_up = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(hp_height_index),
            button_size,
            button_size,
        )
        self.button_down = pu.button(
            pygame.Color(color_palette.color2),
            grid.left_point(13),
            grid.top_point(hp_height_index) + button_size + 5,
            button_size,
            button_size,
        )

    def load_background(self):
        self.background = pygame.image.load("images/backgrounds/background.png")
        self.background = pygame.transform.smoothscale(
            self.background, self.window.get_size()
        )

    def render_text(self, text, x, y, font=font, color=color_palette.text_color):
        text = font.render(
            text,
            True,
            pygame.Color(color),
        )
        self.window.blit(
            text,
            (x, y),
        )

    def render_playmat_card_spot(self, playmat_position_obj):
        pygame.draw.rect(
            self.window,
            color_palette.white,
            pygame.Rect(
                playmat_position_obj.x,
                playmat_position_obj.y,
                card_width,
                card_height,
            ),
            width=2,
        )
        self.render_text(
            playmat_position_obj.name,
            playmat_position_obj.x + self.playmat.field_text_offset_x,
            playmat_position_obj.y + self.playmat.field_text_offset_y,
            font=font_playmat,
        )

    def render_background(self):
        self.window.blit(self.background, (0, 0))

    def render_end_background(self):
        self.background_bw = pygame.image.load("images/backgrounds/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))

    def render_floating_resources(self):
        self.render_text(
            str(self.engine.enemy.resource_manager.floating_resources)
            + " res. floating",
            grid.left_point(15),
            grid.top_point(0),
        )

    def render_enemy(self, color=color_palette.white):
        self.window.blit(
            self.engine.enemy.image,
            (self.playmat.positions.enemy.x, self.playmat.positions.enemy.y),
        ),

        self.render_text(
            str(self.engine.enemy.name),
            self.playmat.positions.enemy.x,
            self.playmat.positions.enemy.y,
            font=font_card_title,
        )

        if self.engine.enemy.talent != Talent.no_talent:
            self.render_text(
                "# "
                + str(self.engine.level_manager.current_level)
                + " - "
                + str(self.engine.enemy.talent.name).upper(),
                self.playmat.positions.enemy.x + self.playmat.field_text_offset_x,
                self.playmat.positions.enemy.y + card_height,
                font=font_card_title,
            )

        self.render_text(
            str(self.engine.enemy.player_class.name).upper(),
            self.playmat.positions.enemy.x + self.playmat.field_text_offset_x,
            self.playmat.positions.enemy.y + card_height * 1.1,
            font=font_card_title,
        )

    def render_enter_new_level(self):
        self.render_text(
            "This is room #" + str(self.engine.level_manager.current_level).upper(),
            grid.left_point(5),
            grid.top_point(3),
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
        self.render_text(
            "Opening door to the next room...",
            grid.left_point(6),
            grid.top_point(6),
            color=color_palette.white,
            font=font_header2,
        )

    def render_lore(self):
        blit_text(
            self.window,
            self.engine.enemy.lore,
            (grid.left_point(5), grid.top_point(4)),
            font_lore,
        )

    def render_weapons(self):
        if len((self.engine.enemy.weapons)) == 1:
            self.render_playmat_card_spot(self.playmat.positions.weapon_1)

        for i, w in enumerate(self.engine.enemy.weapons):
            if w not in self.engine.enemy.played_cards:
                if w.weapon_id == 0:
                    self.render_card(
                        w,
                        self.playmat.positions.weapon_0.x,
                        self.playmat.positions.weapon_0.y,
                    )

                elif w.weapon_id == 1:
                    self.render_card(
                        w,
                        self.playmat.positions.weapon_1.x,
                        self.playmat.positions.weapon_1.y,
                    )
            else:
                playmat_object = None
                match w.weapon_id:
                    case w.weapon_id if w.weapon_id == 0:
                        playmat_object = self.playmat.positions.weapon_0
                    case w.weapon_id if w.weapon_id == 1:
                        playmat_object = self.playmat.positions.weapon_1

                self.render_playmat_card_spot(playmat_object)

    def render_no_moves_left(self):
        pass

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

        for i, m in enumerate(message.split(" ")):
            self.render_text(m, grid.left_point(4), grid.top_point(13 + i))

    def render_deck(self):
        if self.engine.enemy.deck.get_length() > 0:
            self.window.blit(
                self.card_back,
                (self.playmat.positions.deck.x, self.playmat.positions.deck.y),
            )
            self.render_text(
                str(self.engine.enemy.deck.get_length()),
                self.playmat.positions.deck.x,
                self.playmat.positions.deck.y,
            )
        else:
            self.render_playmat_card_spot(self.playmat.positions.deck)

    def render_arsenal(self):
        if self.engine.enemy.arsenal.is_empty() == False:
            if (
                self.engine.enemy.arsenal.state_machine.current_state
                == self.engine.enemy.arsenal.state_machine.face_down
            ):
                self.window.blit(
                    self.card_back,
                    (
                        self.playmat.positions.arsenal.x,
                        self.playmat.positions.arsenal.y,
                    ),
                )
            elif (
                self.engine.enemy.arsenal.state_machine.current_state
                == self.engine.enemy.arsenal.state_machine.face_up
            ):
                self.render_card(
                    self.engine.enemy.arsenal.get_arsenaled_card(),
                    self.playmat.positions.arsenal.x,
                    self.playmat.positions.arsenal.y,
                )

            self.render_text(
                str(self.engine.enemy.arsenal.get_length()),
                self.playmat.positions.arsenal.x,
                self.playmat.positions.arsenal.y,
            )

        elif self.engine.enemy.arsenal.is_empty() == True:
            self.render_playmat_card_spot(self.playmat.positions.arsenal)

    def render_hand(self):
        if (
            self.engine.enemy.stance == Stance.attack
            and (
                self.engine.enemy.combat_chain.is_empty()
                and self.engine.level_manager.move_index == 0
            )
            or (
                len(self.engine.enemy.hand) == 0
                and self.engine.enemy.arsenal.is_empty()
            )
        ):
            color = color_palette.color3
        else:
            color = color_palette.text_color
        self.render_text(
            str(len(self.engine.enemy.hand)) + " in hand",
            grid.left_point(15),
            grid.top_point(2),
            color=color,
        )

    def render_banished_zone(self):
        n_banished_cards = 0
        for k, v in self.engine.enemy.banished_zone.items():
            n_banished_cards += len(v)

        if n_banished_cards > 0:
            self.window.blit(
                self.card_back,
                (
                    self.playmat.positions.banished_zone.x,
                    self.playmat.positions.banished_zone.y,
                ),
            )
            self.render_text(
                str(len(self.engine.enemy.banished_zone)),
                self.playmat.positions.banished_zone.x,
                self.playmat.positions.banished_zone.y,
            )
        else:
            self.render_playmat_card_spot(self.playmat.positions.banished_zone)

    def render_pitch(self):
        if len(self.engine.enemy.pitched_cards) > 0:
            for i, pc in enumerate(self.engine.enemy.pitched_cards):
                self.render_card(
                    pc,
                    self.playmat.positions.pitch.x + i * 7,
                    self.playmat.positions.pitch.y + i * 7,
                )
            self.render_text(
                str(len(self.engine.enemy.pitched_cards)),
                self.playmat.positions.pitch.x,
                self.playmat.positions.pitch.y + rect_height,
            )

        else:
            self.render_playmat_card_spot(self.playmat.positions.pitch)

    def render_graveyard(self):
        if len(self.engine.enemy.graveyard) > 0:
            self.engine.enemy.graveyard[-1].x = self.playmat.positions.graveyard.x
            self.engine.enemy.graveyard[-1].y = self.playmat.positions.graveyard.y
            self.render_card_image(self.engine.enemy.graveyard[-1])
            self.render_card_name(self.engine.enemy.graveyard[-1])
            self.render_card_type(self.engine.enemy.graveyard[-1])
            self.render_text(
                str(len(self.engine.enemy.graveyard)),
                self.playmat.positions.graveyard.x,
                self.playmat.positions.graveyard.y + rect_height,
            )

        else:
            self.render_playmat_card_spot(self.playmat.positions.arsenal)

    def render_combat_chain(self):
        playmat_position_obj = self.playmat.positions.combat_chain

        pygame.draw.rect(
            self.window,
            color_palette.white,
            pygame.Rect(
                playmat_position_obj.x,
                playmat_position_obj.y,
                card_width * 7,
                card_height,
            ),
            width=2,
        )

        if len(self.engine.enemy.played_cards) > 0:
            for i, card in enumerate(self.engine.enemy.played_cards):
                self.render_card(
                    card,
                    playmat_position_obj.x
                    + self.playmat.get_horizontal_spacing() * 2 * i,
                    playmat_position_obj.y,
                    i=i,
                )

        else:
            self.render_text(
                playmat_position_obj.name,
                playmat_position_obj.x + self.playmat.field_text_offset_x,
                playmat_position_obj.y + self.playmat.field_text_offset_y,
                font=font_playmat,
            )

    def render_end_of_chain_link(self):
        playmat_position_obj = self.playmat.positions.combat_chain
        pygame.draw.rect(
            self.window,
            color_palette.black,
            pygame.Rect(
                playmat_position_obj.x
                + self.playmat.get_horizontal_spacing()
                + card_width // 2,
                playmat_position_obj.y - 25,
                5,
                card_height + 50,
            ),
            width=0,
        )

    def render_equipment(self):
        playmat_position_obj = None
        for i, eq in enumerate(self.engine.enemy.equipment_suite.get_pieces_in_play()):
            match eq.equipment_type:
                case eq.equipment_type if eq.equipment_type == EquipmentType.head:
                    playmat_position_obj = self.playmat.positions.head
                case eq.equipment_type if eq.equipment_type == EquipmentType.chest:
                    playmat_position_obj = self.playmat.positions.chest
                case eq.equipment_type if eq.equipment_type == EquipmentType.arms:
                    playmat_position_obj = self.playmat.positions.arms
                case eq.equipment_type if eq.equipment_type == EquipmentType.legs:
                    playmat_position_obj = self.playmat.positions.legs

            if eq not in self.engine.enemy.played_cards:
                self.render_card(eq, playmat_position_obj.x, playmat_position_obj.y)
            else:
                self.render_playmat_card_spot(playmat_position_obj)

    def render_boost_counter(self):
        # print(self.engine.enemy.boost_counter)
        if self.engine.enemy.player_class == PlayerClass.mechanologist:
            if self.engine.enemy.stance == Stance.attack:
                self.render_text(
                    str(self.engine.enemy.boost.counter) + " boost counter",
                    grid.left_point(11),
                    grid.top_point(13),
                )

    def render_action_points(self):
        if self.engine.enemy.action_point_manager.has_action_points_left():
            color = color_palette.text_color
        else:
            color = color_palette.color3
        self.render_text(
            str(self.engine.enemy.action_point_manager.action_points) + " action pts.",
            grid.left_point(15),
            grid.top_point(1),
            color=color,
        )

    def render_card_image(self, card):
        self.window.blit(card.image, (card.x, card.y))

    def render_card_name(self, card):
        self.rect = pygame.draw.rect(
            self.window,
            card_colors[card.color.name],
            (card.x, card.y, card_width, 25),
        )

        if card.color == CardColor.yellow:
            self.render_text(
                str(card.name),
                card.x,
                card.y,
                color=color_palette.black,
                font=font_card_title,
            )
        else:
            self.render_text(
                str(card.name),
                card.x,
                card.y,
                color=color_palette.white,
                font=font_card_title,
            )

    def render_card_class(self, card):
        index = 3
        self.rect = pygame.draw.rect(
            self.window,
            color_palette.color3,
            (
                card.x,
                card.y + card_height / 2 + rect_height * index,
                card_width,
                rect_height,
            ),
        )

        text = ""
        if card.once_per_turn == True:
            text = card.card_class.name + " - once per turn"
        else:
            text = str(card.card_class.name)

        if card.card_class.name != "generic":
            self.render_text(
                text,
                card.x,
                card.y + card_height / 2 + rect_height * index,
                font=font_card_title,
            )

    def render_card_keywords(self, card):
        index = 2
        self.rect = pygame.draw.rect(
            self.window,
            pygame.Color(color_palette.color1),
            (
                card.x,
                card.y + card_height / 2 + rect_height * index,
                card_width,
                rect_height,
            ),
        )

        text = ""
        xy = card.x
        kwds = [c for c in card.keywords if c != Keyword.no_keyword]
        for i, kws in enumerate(kwds):
            if i > 0:
                xy = xy + 45 * index

            if i == 0 and len(kwds) == 2:
                text = kws.name + "/"
            else:
                text = kws.name

            self.render_text(
                text,
                xy,
                card.y + card_height / 2 + rect_height * index,
                font=font_card_title,
            )

    def render_card_type(self, card):
        index = 1
        self.rect = pygame.draw.rect(
            self.window,
            pygame.Color(color_palette.white),
            (
                card.x,
                card.y + card_height / 2 + rect_height * index,
                card_width,
                rect_height,
            ),
        )

        text = card.card_type.name

        self.render_text(
            text,
            card.x,
            card.y + card_height / 2 + rect_height * index,
            font=font_card_title,
            color=color_palette.black,
        )

    def render_power(self, card):
        text = ""
        color = color_palette.white
        if card.card_type in [
            CardType.attack_action,
            CardType.attack_reaction,
            CardType.weapon,
        ]:
            text = str(card.physical)
            color = color = color_palette.white

        # TODO hack for now dont render the plus if last link
        elif card.card_type in [CardType.non_attack_action, CardType.attack_reaction]:
            # if self.engine.enemy.combat_chain.is_last_link(card):
            #     text = str(card.physical)
            # else:
            text = "+" + str(card.physical)

        self.render_text(text, card.x, card.y + card_height, color=color)

    def render_arcane_power(self, card):
        if card.arcane > 0:
            if card.physical > 9 and card.card_type == CardType.non_attack_action:
                offset = arcane_offset + 55
            elif card.physical > 9:
                offset = arcane_offset + 20
            elif card.card_type == CardType.non_attack_action:
                offset = arcane_offset + 35

            elif card.physical > 9 and card.card_type == CardType.non_attack_action:
                offset = arcane_offset + 20
            else:
                offset = arcane_offset

            self.render_text(
                "/{}".format(str(card.arcane)),
                card.x + offset,
                card.y + card_height,
                color=color_palette.green,
            )

    def render_defense(self, card):
        self.render_text(
            str(card.defense),
            card.x + card_width * 0.8,
            card.y + card_height,
            color=color_palette.black,
        )

    def render_card_pitch(self, card):
        self.render_text(
            str(card.pitch),
            card.x,
            card.y - rect_height * 2,
            color=card_colors[card.color.name],
        )

    def render_arcane_barrier(self, card):
        if card.arcane_barrier > 0:
            self.render_text(
                "Arcane Barrier " + str(card.arcane_barrier),
                card.x,
                card.y - rect_height,
                color=color_palette.white,
                font=font_card_title,
            )

    def render_cost(self, card):
        self.render_text(
            str(card.cost),
            card.x + card_width * 0.8,
            card.y - rect_height * 2,
            color=color_palette.color2,
        )

    def render_card(self, card, x=None, y=None, i=0):
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

        self.render_text(
            "HP : " + str(self.engine.enemy.life_counter.life),
            grid.left_point(11),
            grid.top_point(hp_height_index),
        )

    def render_turn_text(self):
        color = None

        if self.engine.enemy.stance == Stance.defend:
            color = pygame.Color(color_palette.white)

        else:
            color = pygame.Color(color_palette.color2)

        self.render_text(
            "{}".format(self.engine.enemy.name)
            + " is "
            + (self.engine.enemy.stance.name + "ing").upper(),
            grid.left_point(1),
            grid.top_point(0),
            font=font,
            color=color,
        )

    def render_win(self):
        self.bg = pygame.image.load("images/backgrounds/background3.png")
        self.bg = pygame.transform.smoothscale(self.bg, self.window.get_size())
        self.window.blit(self.bg, (0, 0))

        self.render_text(
            "You won...but what...",
            grid.left_point(5),
            grid.top_point(5),
            color=color_palette.color3,
        )

        self.render_text(
            "The " + self.engine.win_condition.name.replace("_", " ") + "...",
            grid.left_point(8),
            grid.top_point(3),
            color=color_palette.color3,
        )

        self.render_enemy_life_counter()
        self.render_enemy()

    def render_start_screen(self):
        self.bg = pygame.image.load("images/backgrounds/background2.png")
        self.bg = pygame.transform.smoothscale(self.bg, self.window.get_size())
        self.window.blit(self.bg, (0, 0))

        self.render_text(
            "Enter the abyss..",
            grid.left_point(1),
            grid.top_point(1),
            color=color_palette.color3,
        )

    def update_display(self):
        pygame.display.flip()
