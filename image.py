#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 12:55:38 2024

@author: lukasgartmair
"""

import pygame
from settings import card_height, card_scale


def load_image(img_path):
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(
        img,
        (int(card_height * 0.8 * card_scale), int(card_height * card_scale)),
    )

    return img
