#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import base_animation
from settings import font_card_title
import playmat

playmat_obj = playmat.Playmat()


class LifeCounterAnimation(base_animation.BaseAnimation):
    def __init__(
        self,
        animation_object=None,
        animation_end_mode=base_animation.AnimationEndMode.DURATION,
        mode="received",
    ):
        super().__init__()

        self.offset = 0
        self.animation_duration = 1500
        self.velocity = 2
        self.color = (0, 0, 0)
        self.string = ""
        self.mode = mode
        self.position = (0, 0)

    def animate(self):
        super().animate()

        if self.mode == "received":
            self.string = "+ {} HP"
            self.color = (0, 255, 0)

        elif self.mode == "lost":
            self.string = "- {} HP"
            self.color = (255, 0, 0)

        self.position = (
            playmat_obj.positions.life_counter.x,
            playmat_obj.positions.life_counter.y,
        )

        text = font_card_title.render(
            self.string.format(
                self.animation_object.current_amount,
            ),
            True,
            self.color,
        )
        self.screen.blit(
            text, (self.position[0] + self.offset, self.position[1] - self.offset)
        )
        self.offset += self.velocity
