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
from input_box import Attack

from settings import FPS


class Game:
    def __init__(self):
        self.engine = GameEngine()
        pygame.display.set_caption(
            "Fight against the {} '{}'".format(
                self.engine.enemy.race, self.engine.enemy.name
            )
        )

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

        self.attack = Attack()

        self.input_boxes = [
            self.renderer.input_box_physical,
            self.renderer.input_box_arcane,
        ]

        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                for inp_box in self.input_boxes:
                    inp_box.check_activation(event)

                if event.type == pygame.KEYDOWN:
                    for inp_box in self.input_boxes:
                        inp_box.update(event=event)

                    if event.key == pygame.K_SPACE:
                        self.renderer.render()

                        if self.engine.state == GameState.playing:
                            if self.engine.enemy.stance == Stance.defend:
                                for inp_box in self.input_boxes:
                                    if inp_box.active:
                                        self.attack.set_values(inp_box)

                                self.engine.play(self.attack)

                                for inp_box in self.input_boxes:
                                    inp_box.reset()

                            else:
                                self.engine.play(self.attack)

                        self.renderer.render_background()
                        self.renderer.render()

                    if event.key == pygame.K_RETURN:
                        self.renderer.render()

                        if self.engine.state == GameState.playing:
                            self.engine.enemy.finish_phase()
                            self.renderer.render_background()

                            self.renderer.render_background()
                            self.renderer.render()

                if self.engine.enemy.stance == Stance.defend:
                    for inp_box in self.input_boxes:
                        inp_box.render()

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
