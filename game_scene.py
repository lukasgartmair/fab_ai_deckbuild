#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
from engine import GameState
import scene_manager
from enemy import Stance

from game import Game


class GameScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        # print("Game Scene")

        self.input_boxes = [
            self.renderer.input_box_physical,
            self.renderer.input_box_arcane,
        ]

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                Game.quit_everything(self)

            for inp_box in self.input_boxes:
                inp_box.check_activation(event)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.engine.enemy.life_counter.button_up.isOver(
                    pygame.mouse.get_pos()
                ):
                    self.engine.enemy.life_counter.increase_life()
                elif self.engine.enemy.life_counter.button_down.isOver(
                    pygame.mouse.get_pos()
                ):
                    self.engine.enemy.life_counter.decrease_life()

                self.render()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for check_box in self.renderer.check_boxes:
                    if check_box.cb.isOver(pygame.mouse.get_pos()):
                        check_box.check_activation()
                        self.render()

            for check_box in self.renderer.check_boxes:
                if check_box.cb.isChecked() == True:
                    self.engine.modifiers.modifier_dict[check_box.name] = True
                else:
                    self.engine.enemy.modifiers.modifier_dict[check_box.name] = False

            if event.type == pygame.KEYDOWN:
                for inp_box in self.input_boxes:
                    inp_box.update(event=event)
                    if event.key == pygame.K_BACKSPACE:
                        self.render()

                if event.key == pygame.K_SPACE:
                    self.render()

                    if (
                        self.engine.state_machine.current_state
                        == self.engine.state_machine.playing
                    ):
                        if self.engine.enemy.stance == Stance.defend:
                            for inp_box in self.input_boxes:
                                if inp_box.has_text():
                                    self.engine.attack.set_values(inp_box)

                            self.engine.play(self.engine.attack)

                            for inp_box in self.input_boxes:
                                inp_box.reset()
                                self.engine.attack.reset()
                            for check_box in self.renderer.check_boxes:
                                check_box.reset()

                            self.engine.enemy.modifiers.reset()

                        else:
                            self.engine.play()

                        self.render()

                if event.key == pygame.K_RETURN:
                    if (
                        self.engine.state_machine.current_state
                        == self.engine.state_machine.playing
                    ):
                        self.engine.enemy.finish_phase()

                        for inp_box in self.input_boxes:
                            inp_box.reset()
                            self.engine.attack.reset()

                        for check_box in self.renderer.check_boxes:
                            check_box.reset()

                        self.engine.attack.reset()

                        self.engine.enemy.modifiers.reset()

                        self.render()

                        if self.engine.check_fatigue_condition() == True:
                            self.switch_to_scene(
                                scene_manager.get_end_scene(self.engine, self.renderer)
                            )
                            self.is_active = False

    def update(self):
        if self.engine.state_machine.current_state == self.engine.state_machine.playing:
            self.engine.check_win_condition()
            if (
                self.engine.state_machine.current_state
                == self.engine.state_machine.ended
            ):
                if (
                    self.engine.state_machine.current_state
                    == self.engine.state_machine.ended
                ):
                    self.switch_to_scene(
                        scene_manager.get_end_scene(self.engine, self.renderer)
                    )
                    self.is_active = False

    def render(self):
        if self.is_active:
            self.renderer.render_background()

            self.renderer.render_enemy_play()

            self.renderer.render_floating_resources()

            self.renderer.render_enemy_life_counter()

            self.renderer.render_weapons()

            self.renderer.render_arsenal()

            self.renderer.render_deck()

            self.renderer.render_enemy()

            self.renderer.render_hand()

            self.renderer.render_banished_zone()

            self.renderer.render_pitch()

            self.renderer.render_graveyard()

            self.renderer.render_action_points()

            self.renderer.render_turn_text()

            if self.engine.enemy.stance == Stance.defend:
                for inp_box in self.input_boxes:
                    inp_box.render()

                for check_box in self.renderer.check_boxes:
                    check_box.cb.draw(self.renderer.window)

            self.renderer.render_floating_resources()

            pygame.display.flip()