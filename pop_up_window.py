#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 20:58:33 2024

@author: lukasgartmair
"""
import pygame
import pygame_menu


button_width = 300
button_height = 75


class PopUpWindow:
    def __init__(self, screen):
        self.screen = screen
        self.menu = self.create_menu()

        self.select_finish()

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Deciscion time", 400, 300, theme=pygame_menu.themes.THEME_DARK
        )
        menu.add.button(
            "Finish Your Attak", self.dummy, button_id="finish_combat_chain_button"
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

    def dummy(self):
        pass
