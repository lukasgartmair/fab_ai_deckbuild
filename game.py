#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 08:41:26 2024

@author: lukasgartmair
"""

import sys
import pygame
from renderer import Renderer
from engine import GameEngine
from settings import FPS


class Game:
    def __init__(self):
        self.engine = GameEngine()
        self.renderer = Renderer(self.engine)

    @staticmethod
    def quit_everything(active_scene=None):
        if active_scene:
            active_scene.terminate()
        pygame.display.quit()
        pygame.quit()

        sys.exit()

    def run(self, starting_scene):
        clock = pygame.time.Clock()

        active_scene = starting_scene

        while active_scene is not None:
            events = pygame.event.get()

            active_scene.process_input(events)
            active_scene.update()
            active_scene.render()

            active_scene = active_scene.next

            pygame.display.flip()
            clock.tick(FPS)
