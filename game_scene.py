#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
from engine import GameStateMachine
import scene_manager
from enemy import Stance
from playstyle import PlayerClass
from game import Game
from sound import Sound
from stance import StanceStateMachine


class GameScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        # print("Game Scene")

        self.pygamegame_sound = Sound()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                Game.quit_everything(self)

            for inp_box in self.renderer.input_boxes:
                inp_box.check_activation(event)
                if inp_box.active == True:
                    self.render_inputs()

            if event.type == pygame.MOUSEBUTTONUP:
                if self.renderer.button_up.isOver(pygame.mouse.get_pos()):
                    self.engine.enemy.life_counter.increase_life()
                elif self.renderer.button_down.isOver(pygame.mouse.get_pos()):
                    self.engine.enemy.life_counter.decrease_life()

                self.render()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for check_box in self.renderer.check_boxes:
                    if check_box.cb.isOver(pygame.mouse.get_pos()):
                        check_box.check_activation()
                        self.render()

            for check_box in self.renderer.check_boxes:
                if check_box.cb.isChecked() == True:
                    self.engine.enemy.modifiers.modifier_dict[check_box.name] = True
                else:
                    self.engine.enemy.modifiers.modifier_dict[check_box.name] = False

            if event.type == pygame.KEYDOWN:
                self.render_inputs()

                for inp_box in self.renderer.input_boxes:
                    inp_box.update(event=event)
                    if event.key == pygame.K_BACKSPACE:
                        self.render()

                if event.key == pygame.K_SPACE:
                    self.render()
                    print()
                    print("PLAYER ATTACK")
                    print(self.engine.player_attack)
                    print(self.engine.player_attack.physical)
                    print()
                    if (
                        self.engine.state_machine.current_state
                        == self.engine.state_machine.playing
                    ):
                        if self.engine.enemy.stance_state_machine.current_state in [
                            StanceStateMachine.defensive_reaction,
                            StanceStateMachine.defense,
                        ]:
                            for inp_box in self.renderer.input_boxes:
                                if inp_box.has_text():
                                    self.engine.player_attack.set_values(inp_box)

                            self.engine.play(self.engine.player_attack)

                            for inp_box in self.renderer.input_boxes:
                                inp_box.reset()

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
                        self.engine.trigger_stance_switch()

                        for inp_box in self.renderer.input_boxes:
                            inp_box.reset()

                        for check_box in self.renderer.check_boxes:
                            check_box.reset()

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

    def render_inputs(self):
        if self.engine.enemy.stance_state_machine.current_state in [
            StanceStateMachine.defensive_reaction,
            StanceStateMachine.defense,
        ]:
            for inp_box in self.renderer.input_boxes:
                inp_box.render()

            for check_box in self.renderer.check_boxes:
                check_box.cb.draw(self.renderer.window)

    def render(self):
        if self.is_active:
            self.renderer.render_background()

            self.renderer.render_turn_text()

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

            self.renderer.render_no_moves_left()

            self.renderer.render_equipment()

            self.renderer.render_combat_chain()

            self.renderer.render_floating_resources()

            self.render_inputs()

            self.renderer.render_log()

            # MECHANOLOGIST STUFF

            if self.engine.enemy.player_class == PlayerClass.mechanologist:
                self.renderer.render_boost_counter()
                self.renderer.render_boost()

            pygame.display.flip()
