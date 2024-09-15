#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import base_animation
from settings import font_header2
import playmat

playmat_obj = playmat.Playmat()


class LifeCounterAnimation(base_animation.BaseAnimation):
    def __init__(
        self,
        object_to_be_animated=None,
        animation_end_mode=base_animation.AnimationEndMode.DURATION,
    ):
        super().__init__()
        print(self.object_to_be_animated)
        self.object_to_be_animated = object_to_be_animated

        self.offset = 0
        self.animation_duration = 2000
        self.velocity = 3
        self.color = (0, 0, 0)
        self.string = ""
        self.position = (0, 0)

    def animate(self):
        super().animate()

        if self.object_to_be_animated.current_amount > 0:
            self.string = "+ {} HP"
            self.color = (0, 255, 0)

            self.position = (
                playmat_obj.positions.life_counter.x,
                playmat_obj.positions.life_counter.y,
            )

        elif self.object_to_be_animated.current_amount < 0:
            self.string = "- {} HP"
            self.color = (255, 0, 0)

            self.position = (
                playmat_obj.positions.life_counter.x,
                playmat_obj.positions.life_counter.y,
            )

        text = font_header2.render(
            self.string.format(
                self.object_to_be_animated.current_amount,
            ),
            True,
            self.color,
        )
        self.screen.blit(
            text, (self.position[0] + self.offset, self.position[1] - self.offset)
        )
        if self.object_to_be_animated.current_amount > 0:
            self.offset += self.velocity
        elif self.object_to_be_animated.current_amount < 0:
            self.offset -= self.velocity
