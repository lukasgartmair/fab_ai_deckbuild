#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:57:14 2024

@author: lukasgartmair
"""

import pygame
import pygame_menu
from settings import height, width
from utils import normalize_position
from colors import color_palette

theme = pygame_menu.themes.THEME_DARK


class BaseMenu:
    def __init__(self, screen=None, position=None, screen_dimension=(width, height)):
        self.screen = screen
        self.position = position
        if self.position is None:
            self.position = (width / 3, height / 3, False)

    def dummy(self):
        pass

    def get_absolute_rect(self, widget):
        # TODO find the originally impelmented version of this
        rect_temp = widget.get_rect()
        rect_temp.x += self.position[0]
        rect_temp.y += self.position[1]
        return rect_temp

    def reset(self):
        for w in self.menu.get_widgets():
            w.reset_value()


class ModifiersWindow(BaseMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu()

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Modifiers", 350, 200, position=self.position, theme=theme
        )
        menu.add.toggle_switch(
            "Dominate",
            button_id="toggleswitch_dominate",
            font="z003",
            is_selectable=False,
        )
        menu.add.toggle_switch(
            "Intimidate",
            button_id="toggleswitch_dominate",
            font="z003",
            is_selectable=False,
        )

        return menu

    def switch(self, widget):
        if widget.get_value() == 0:
            widget.set_value(1)
        elif widget.get_value() == 1:
            widget.set_value(0)

    def display(self) -> None:
        self.menu.enable()
        self.menu.draw(self.screen)


class PlayerAttackWindow(BaseMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu()

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Player Attack Input", 350, 200, position=self.position, theme=theme
        )

        menu.add.text_input(
            "Physical damage: ",
            textinput_id="physical_input",
            default="",
            font="z003",
            maxchar=2,
        )
        menu.add.text_input(
            "Arcane damage: ",
            textinput_id="damage_input",
            default="",
            font="z003",
            maxchar=2,
        )

        return menu

    def switch(self, widget):
        if widget.get_value() == 0:
            widget.set_value(1)
        elif widget.get_value() == 1:
            widget.set_value(0)

    def display(self) -> None:
        self.menu.enable()
        self.menu.draw(self.screen)


class ContinueCombatChainWindow(BaseMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu()
        self.select_finish()

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Decision time", 400, 300, position=self.position, theme=theme
        )
        menu.add.button(
            "Finish Your Attack", self.dummy, button_id="finish_combat_chain_button"
        )
        menu.add.button(
            "Continue Combat Chain",
            self.dummy,
            button_id="continue_combat_chain_button",
        )

        return menu

    def select_finish(self):
        self.menu.get_widget("finish_combat_chain_button").select(update_menu=True)

    def select_continue(self):
        self.menu.get_widget("continue_combat_chain_button").select(update_menu=True)

    def continue_is_selected(self):
        return self.menu.get_widget("continue_combat_chain_button").is_selected()

    def finish_is_selected(self):
        return self.menu.get_widget("finish_combat_chain_button").is_selected()

    def continue_combat_chain(self):
        return (
            True
            if self.menu.get_widget("continue_combat_chain_button").is_selected()
            else False
        )

    def display(self) -> None:
        self.menu.enable()
        self.menu.draw(self.screen)

    def motion(self, position: pygame.Vector2) -> None:
        self.menu_manager.motion(position)

    def move_on(self):
        self.continue_combat_chain = False

    def continue_chain(self):
        self.continue_combat_chain = True
