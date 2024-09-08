#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 12:55:38 2024

@author: lukasgartmair
"""
import os
import pygame
from settings import card_width, card_height

image_library = {}


def get_image(path):
    img = load_image(path)
    img = pygame.transform.scale(
        img,
        (int(card_width), int(card_height)),
    )
    return img


def load_image(path):
    image = image_library.get(path)
    if image == None:
        canonicalized_path = os.getcwd() + "/images/" + path
        image = pygame.image.load(canonicalized_path)
        image_library[path] = image
    return image


def img_to_surfarray(img):
    return pygame.transform.scale(
        pygame.surfarray.make_surface(img),
        (int(card_width), int(card_height)),
    )
