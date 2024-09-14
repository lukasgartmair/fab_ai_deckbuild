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
            pass


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
            toggleswitch_id="toggleswitch_dominate",
            font="z003",
            is_selectable=False,
            onchange=self.switch,
            selection_effect=None,
            kwargs={"toggleswitch_id": "toggleswitch_dominate"},
        )
        menu.add.toggle_switch(
            "Intimidate",
            toggleswitch_id="toggleswitch_intimidate",
            font="z003",
            is_selectable=False,
            onchange=self.switch,
            selection_effect=None,
            kwargs={"toggleswitch_id": "toggleswitch_intimidate"},
        )

        return menu

    def switch(self, current_value, *args, **kwargs):
        if current_value == False:
            w = self.menu.get_widget(kwargs["kwargs"]["toggleswitch_id"])
            w.set_value(True)
        elif current_value == True:
            w = self.menu.get_widget(kwargs["kwargs"]["toggleswitch_id"])
            w.set_value(False)

    def display(self) -> None:
        self.menu.enable()
        self.menu.draw(self.screen)

    def reset(self):
        for w in self.menu.get_widgets():
            w.reset_value()


class PlayerAttackWindow(BaseMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.create_menu()

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Player Attack", 350, 200, position=self.position, theme=theme
        )

        menu.add.text_input(
            "Physical: ",
            textinput_id="physical_input",
            default="",
            font="z003",
            maxchar=2,
            input_underline="_",
        )
        menu.add.text_input(
            "Arcane: ",
            textinput_id="arcane_input",
            default="",
            font="z003",
            maxchar=2,
            input_underline="_",
        )

        return menu

    def has_text(self, widget):
        return True if len(widget.get_value()) > 0 else False

    def custom_update(self, widget, event):
        has_changed = False
        if widget.is_selected() == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    widget.set_value(widget.get_value()[:-1])
                    has_changed = True
                else:
                    if event.key in [
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ]:
                        if len(widget.get_value()) > 2:
                            widget.set_value(widget.get_value()[:2])
                        else:
                            widget.set_value(widget.get_value() + event.unicode)
                            has_changed = True
        return has_changed

    def reset(self):
        for w in self.menu.get_widgets():
            w.clear()
            w.set_value("")

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
