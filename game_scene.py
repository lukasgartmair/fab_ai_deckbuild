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
import animation
import base_animation
import custom_events


class GameScene(SceneBase):
    waiting_for_user_input = False

    def __init__(self, *args):
        super().__init__(*args)

        custom_events.CUSTOM_EVENT = custom_events.register_custom_event()
        self.pygamegame_sound = Sound()

    def process_input(self, events):

        pygame.time.wait(50)

        for event in events:

            if event.type == pygame.QUIT:
                Game.quit_everything(self)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.renderer.button_up.isOver(pygame.mouse.get_pos()):
                    self.engine.enemy.life_counter.increase_life()
                if self.renderer.button_down.isOver(pygame.mouse.get_pos()):
                    self.engine.enemy.life_counter.decrease_life()

                self.render()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_modifiers(event)
                self.handle_player_attack_input(event)

            if event.type == pygame.KEYDOWN:
                self.render_inputs()

                self.update_player_attack_input(event)

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

                            self.set_player_attack_input()

                            self.engine.play(self.engine.player_attack)

                            self.renderer.player_attack_window.reset()
                            self.engine.enemy.modifiers.reset()

                        else:
                            self.engine.play()
                            self.renderer.player_attack_window.reset()
                            self.renderer.player_attack_window.display()

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
        menu_widgets = self.renderer.modifiers_window.menu.get_widgets()
        for w in menu_widgets:
            abs_rect = self.renderer.modifiers_window.get_absolute_rect(w)
            if (abs_rect.collidepoint(event.pos)) == True:
                w.change()

                self.engine.enemy.modifiers.modifier_dict[w.get_title().lower()] = (
                    w.get_value()
                )

    def handle_player_attack_input(self, event):
        menu_widgets = self.renderer.player_attack_window.menu.get_widgets()
        for w in menu_widgets:
            abs_rect = self.renderer.player_attack_window.get_absolute_rect(w)
            if (abs_rect.collidepoint(event.pos)) == True:
                w.select(update_menu=True)

    def update_player_attack_input(self, event):

        w = self.renderer.player_attack_window.menu.get_widget("physical_input")
        has_changed = self.renderer.player_attack_window.custom_update(w, event)

        w2 = self.renderer.player_attack_window.menu.get_widget("arcane_input")
        has_changed2 = self.renderer.player_attack_window.custom_update(w2, event)

        if any([has_changed, has_changed2]):
            self.renderer.player_attack_window.display()

    def set_player_attack_input(self):
        w_physical = self.renderer.player_attack_window.menu.get_widget(
            "physical_input"
        )
        if self.renderer.player_attack_window.has_text(w_physical) == True:
            self.engine.player_attack.set_value_physical(w_physical.get_value())

        w_arcane = self.renderer.player_attack_window.menu.get_widget("arcane_input")
        if self.renderer.player_attack_window.has_text(w_arcane) == True:
            self.engine.player_attack.set_value_arcane(w_arcane.get_value())

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

            self.renderer.player_attack_window.display()

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

                # self.renderer.render_log()

            pygame.display.flip()
