#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import scene_manager
from playstyle import PlayerClass
from game import Game
from sound import Sound
from stance import StanceStateMachine
from utils import normalize_position


class GameScene(SceneBase):
    waiting_for_user_input = False

    def __init__(self, *args):
        super().__init__(*args)
        # print("Game Scene")

        self.pygamegame_sound = Sound()

    def process_input(self, events):

        # pygame.time.wait(100)

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
                if self.renderer.button_down.isOver(pygame.mouse.get_pos()):
                    self.engine.enemy.life_counter.decrease_life()

                self.render()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_modifiers(event)

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
                    print(self.engine.player_attack.physical.get_latest_step_value())
                    print()
                    if (
                        self.engine.state_machine.current_state
                        == self.engine.state_machine.playing
                    ):
                        if self.engine.enemy.stance_state_machine.current_state in [
                            StanceStateMachine.defensive_reaction,
                            StanceStateMachine.defense,
                        ]:

                            if all(
                                [
                                    True
                                    for inp_box in self.renderer.input_boxes
                                    if inp_box.has_text()
                                ]
                            ):
                                for inp_box in self.renderer.input_boxes:
                                    self.engine.player_attack.set_values(
                                        inp_box, all_attacks=True
                                    )

                            elif any(
                                [
                                    True
                                    for inp_box in self.renderer.input_boxes
                                    if inp_box.has_text()
                                ]
                            ):

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

                if (
                    self.engine.state_machine.current_state
                    == self.engine.state_machine.playing
                ):
                    if (
                        self.engine.enemy.stance_state_machine.current_state
                        == StanceStateMachine.defensive_reaction
                    ):
                        self.switch_continue_combat_chain_window(event)

                if event.key == pygame.K_RETURN:
                    if (
                        self.engine.state_machine.current_state
                        == self.engine.state_machine.playing
                    ):
                        print("HERE  xhhxhx")
                        if (
                            self.engine.enemy.stance_state_machine.current_state
                            == StanceStateMachine.defensive_reaction
                        ):
                            if self.waiting_for_user_input == False:
                                self.waiting_for_user_input = True
                                self.renderer.render_continue_combat_chain_window()
                                break
                            else:
                                # TODO why dont unless and cond for the state machine not work properly here
                                if (
                                    self.renderer.continue_combat_chain_window.menu.is_enabled()
                                ):
                                    print("HERERE ENABLED")
                                    print(
                                        self.renderer.continue_combat_chain_window.continue_combat_chain()
                                    )
                                    if (
                                        self.renderer.continue_combat_chain_window.continue_combat_chain()
                                        == True
                                    ):
                                        self.engine.enemy.stance_state_machine.continue_combat_chain = (
                                            True
                                        )
                                    self.engine.trigger_stance_switch()

                                    self.waiting_for_user_input = False
                                    self.renderer.continue_combat_chain_window.select_finish()
                        else:
                            self.engine.trigger_stance_switch()

                        for inp_box in self.renderer.input_boxes:
                            inp_box.reset()

                        self.renderer.modifiers_window.reset()

                        self.engine.enemy.modifiers.reset()

                        self.render()

                        if self.engine.check_fatigue_condition() == True:
                            self.switch_to_scene(
                                scene_manager.get_end_scene(self.engine, self.renderer)
                            )
                            self.is_active = False

    def switch_continue_combat_chain_window(self, event):
        if self.waiting_for_user_input == True:
            if (
                event.key == pygame.K_DOWN
                and self.renderer.continue_combat_chain_window.finish_is_selected()
                == True
            ):
                self.renderer.continue_combat_chain_window.select_continue()
                self.renderer.render_continue_combat_chain_window()
            if (
                event.key == pygame.K_UP
                and self.renderer.continue_combat_chain_window.continue_is_selected()
                == True
            ):
                self.renderer.continue_combat_chain_window.select_finish()
                self.renderer.render_continue_combat_chain_window()

    def handle_modifiers(self, event):
        print(event.pos)
        menu_widgets = self.renderer.modifiers_window.menu.get_widgets()
        for w in menu_widgets:
            print(event.pos)
            print(w.get_rect(to_absolute_position=True).x)
            print(w.get_rect(to_absolute_position=True).y)
            print(w.get_rect(to_real_position=True).collidepoint(event.pos))
            abs_rect = self.renderer.modifiers_window.get_absolute_rect(w)
            if (abs_rect.collidepoint(event.pos)) == True:
                self.renderer.modifiers_window.switch(w)

                if w.get_value() == 1:
                    self.engine.enemy.modifiers.modifier_dict[w.get_title().lower()] = (
                        True
                    )
                elif w.get_value() == 0:
                    self.engine.enemy.modifiers.modifier_dict[w.get_title().lower()] = (
                        False
                    )

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

            self.renderer.render_modifiers_window()

            for inp_box in self.renderer.input_boxes:
                inp_box.render()

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

            # MECHANOLOGIST STUFF

            if self.engine.enemy.player_class == PlayerClass.mechanologist:
                self.renderer.render_boost_counter()
                self.renderer.render_boost()

            if self.engine.enemy.stance_state_machine.current_state in [
                StanceStateMachine.defense,
                StanceStateMachine.defensive_reaction,
            ]:

                self.renderer.render_log()

            if self.waiting_for_user_input == True:
                print("RENDERING POP UP")
                self.renderer.render_pop_up_window()

            pygame.display.flip()
