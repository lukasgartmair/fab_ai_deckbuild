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

delay = 1


class EndScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        # print("End Scene")

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                Game.quit_everything(self)

            if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_RETURN or event.key == pygame.K_SPACE
            ):
                if (
                    self.engine.state_machine.current_state
                    == self.engine.state_machine.ended
                ):
                    self.renderer.render_create_deck_message()
                    self.engine.advance_level()

                    pygame.display.flip()
                    self.switch_to_scene(
                        scene_manager.get_title_scene(self.engine, self.renderer)
                    )
                    self.is_active = False

    def update(self):
        pass

    def render(self):
        if self.is_active:
            self.renderer.render_win()
