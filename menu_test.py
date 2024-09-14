#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:03:42 2024

@author: lukasgartmair
"""
import sys
from widgets import ModifiersWindow
import pygame_menu
import traceback
import pygame


def quit_everything(active_scene=None):
    pygame.display.quit()
    pygame.quit()

    sys.exit()


width = 500
height = 500

import pygame


theme = pygame_menu.themes.THEME_DARK


class ModifiersWindow:
    def __init__(self, screen=None, position=None):
        self.screen = screen
        self.position = position
        if self.position is None:
            self.position = (40, 40, False)

        self.menu = self.create_menu()

    def dummy(self):
        pass

    def create_menu(self):
        menu = pygame_menu.Menu(
            "Modifiers", 350, 300, position=self.position, theme=theme
        )
        menu.add.toggle_switch(
            "Dominate",
            toggleswitch_id="toggleswitch_dominate",
            font="z003",
            onchange=self.switch,
            kwargs={"toggleswitch_id": "toggleswitch_dominate"},
        )
        menu.add.toggle_switch(
            "Intimidate",
            toggleswitch_id="toggleswitch_intimidate",
            font="z003",
            onchange=self.switch,
            kwargs={"toggleswitch_id": "toggleswitch_intimidate"},
        )

        menu.add.text_input(
            "Last name: ",
            default="",
            textinput_id="text",
            maxchar=3,
            input_underline="_",
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
        self.menu.draw(self.screen)

    def get_absolute_rect(self, widget):
        # TODO find the originally impelmented version of this
        rect_temp = widget.get_rect()
        rect_temp.x += self.position[0]
        rect_temp.y += self.position[1]
        return rect_temp

    def custom_update(self, widget, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                widget.set_value(widget.get_value()[:-1])
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
                    widget.set_value(widget.get_value() + event.unicode)
                    if len(widget.get_value()) > 2:
                        widget.set_value(widget.get_value()[:2])


def main_local():

    tb = None

    try:
        pygame.init()
        screen = pygame.display.set_mode([width, height])
        running = True

        test_window = ModifiersWindow(screen=screen)

        while running == True:

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONUP:
                    print(event.pos)
                    menu_widgets = test_window.menu.get_widgets()
                    mouseover_widget = test_window.menu.get_mouseover_widget()
                    print(mouseover_widget)
                    print(menu_widgets)

                    for w in menu_widgets:
                        print(event.pos)
                        print(w.get_rect(to_absolute_position=True).x)
                        print(w.get_rect(to_absolute_position=True).y)
                        print(w.get_rect(to_real_position=True).collidepoint(event.pos))
                        abs_rect = test_window.get_absolute_rect(w)
                        if (abs_rect.collidepoint(event.pos)) == True:
                            w.change()
                            test_window.display()

                if event.type == pygame.KEYDOWN:

                    w = test_window.menu.get_widget("text")
                    test_window.custom_update(w, event)

                if event.type == pygame.QUIT:

                    running = False
                    quit_everything()

            test_window.display()

            pygame.display.flip()

    except:
        tb = traceback.format_exc()
        print(tb)
        quit_everything()


if __name__ == "__main__":
    main_local()
