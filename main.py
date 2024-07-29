#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
"""

import sys
import traceback
import pygame

from enemy import Stance
from engine import GameState, GameEngine

from renderer import Renderer

from settings import FPS


class Game:
    def __init__(self):
        self.engine = GameEngine()
        pygame.display.set_caption("Flesh and Blood AI enemy")

        self.renderer = Renderer(self.engine)

    @staticmethod
    def quit_everything(active_scene=None):
        if active_scene:
            active_scene.terminate()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def run(self):
        run = True

        clock = pygame.time.Clock()

        self.renderer.render_initial_game_state()

        self.renderer.input_box.player_attack_value = None

        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                self.renderer.input_box.check_activation(event)

                if event.type == pygame.KEYDOWN:
                    self.renderer.input_box.update(event=event)

                    if event.key == pygame.K_SPACE:
                        self.renderer.render()

                        if self.engine.state == GameState.playing:
                            if self.engine.enemy.stance == Stance.defend:
                                if self.renderer.input_box.active:
                                    self.renderer.input_box.player_attack_value = (
                                        self.renderer.input_box.send_input()
                                    )
                                    if (
                                        self.renderer.input_box.player_attack_value
                                        is not None
                                    ):
                                        self.renderer.input_box.player_attack_value = int(
                                            self.renderer.input_box.player_attack_value
                                        )

                                        print(
                                            self.renderer.input_box.player_attack_value
                                        )
                                        self.engine.play(
                                            self.renderer.input_box.player_attack_value
                                        )
                                        self.renderer.input_box.reset()

                            else:
                                self.engine.play(
                                    self.renderer.input_box.player_attack_value
                                )

                        self.renderer.render_background()
                        self.renderer.render()

                    if event.key == pygame.K_RETURN:
                        if self.renderer.input_box.active:
                            self.renderer.input_box.player_attack_value = (
                                self.renderer.input_box.send_input()
                            )
                            if self.renderer.input_box.player_attack_value is not None:
                                self.renderer.input_box.player_attack_value = int(
                                    self.renderer.input_box.player_attack_value
                                )

                                print(self.renderer.input_box.player_attack_value)
                                self.engine.play(
                                    self.renderer.input_box.player_attack_value
                                )
                                self.renderer.input_box.reset()

                        else:
                            self.engine.enemy.finish_phase()
                            self.renderer.render_background()

                        self.renderer.render_background()
                        self.renderer.render()

            if self.engine.enemy.stance == Stance.defend:
                if self.renderer.input_box.player_attack_value is not None:
                    self.renderer.input_box.color = "blue"
                self.renderer.input_box.render()

            self.renderer.render_floating_resources()

            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    # unittest.main()
    game = Game()

    tb = None

    try:
        game.run()
    except:
        tb = traceback.format_exc()
        print(tb)
        Game.quit_everything()
