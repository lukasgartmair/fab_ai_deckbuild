#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:42:52 2024

@author: lukasgartmair
"""

import pygame
import colors
import base_animation
from settings import width, height


animation_queue = base_animation.AnimationQueue()


class LifeCounterAnimation(base_animation.BaseAnimation):
    def __init__(
        self,
        animation_object,
        animation_end_mode=base_animation.AnimationEndMode.N_TRIGGERS,
    ):
        super().__init__(camera)

        self.animation_object = animation_object
