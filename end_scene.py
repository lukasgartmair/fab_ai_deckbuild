#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:18:06 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import scene_manager
from game import Game
from colors import color_palette
from settings import grid

import PygameUtils as pu

button_size_x = 100
button_size_y = 500


class EndScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        # print("End Scene")

        self.restart_button = pu.button(
            pygame.Color(color_palette.color3),
            grid.left_point(6),
            grid.top_point(6),
            button_size_y,
            button_size_x,
            font="z003",
            text="Face the truth!".upper(),
        )

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                Game.quit_everything(self)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.restart_button.isOver(pygame.mouse.get_pos()):
                    self.switch_to_scene(
                        scene_manager.get_title_scene(self.engine, self.renderer)
                    )
                    self.is_active = False
                    self.engine.advance_level()

                    self.render()

    def update(self):
        pass

    def render(self):
        if self.is_active:
            self.renderer.render_win()
            self.restart_button.draw(self.renderer.window)
