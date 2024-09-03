#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:15:03 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import scene_manager
from game import Game
from colors import color_palette
from sound import Sound


class TitleScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        # print("Title Scene")
        self.skip = True

        self.game_sound = Sound()

        self.game_sound.play_intro_music()

    def process_input(self, events):
        if self.skip:
            self.switch_to_scene(
                scene_manager.get_game_scene(self.engine, self.renderer)
            )
            self.engine.state_machine.start_game()
            self.is_active = False

        for event in events:
            if event.type == pygame.QUIT:
                Game.quit_everything(self)
            if (
                self.engine.state_machine.current_state
                == self.engine.state_machine.starting
            ):
                if event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_RETURN or event.key == pygame.K_SPACE
                ):
                    self.game_sound.stop_intro_music()
                    self.switch_to_scene(
                        scene_manager.get_game_scene(self.engine, self.renderer)
                    )
                    self.engine.state_machine.start_game()
                    self.is_active = False

    def get_scene_data(self):
        pass

    def update(self):
        pass

    def render(self):
        if self.is_active:
            self.renderer.render_start_screen()

            self.renderer.render_enter_new_level()
            self.renderer.render_enemy(color=color_palette.black)
            self.renderer.render_lore()
