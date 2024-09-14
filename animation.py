#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import colors
import base_animation
from settings import width, height, font_card_title
import playmat


class LifeCounterAnimation(base_animation.BaseAnimation):
    global window

    def __init__(
        self,
        animation_end_mode=base_animation.AnimationEndMode.DURATION,
        mode="received",
    ):
        super().__init__()
        self.screen = window
        self.offset = 0
        self.animation_duration = 1500
        self.velocity = 2
        self.color = (0, 0, 0)
        self.string = ""
        self.mode = mode
        self.position = (0, 0)

    def animate(self, animation_object):
        super().animate(animation_object)

        if self.mode == "received":
            self.string = "+ {} HP"
            self.color = (0, 255, 0)

        elif self.mode == "lost":
            self.string = "- {} HP"
            self.color = (255, 0, 0)

        self.position = (
            self.playmat.positions.life_counter.x,
            self.playmat.positions.life_counter.y,
        )

        text = font_card_title.render(
            self.string.format(
                animation_object.current_amount,
            ),
            True,
            self.color,
        )
        self.screen.blit(
            text, (self.position[0] + self.offset, self.position[1] - self.offset)
        )
        self.offset += self.velocity
