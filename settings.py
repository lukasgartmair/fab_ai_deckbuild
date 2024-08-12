#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:22:55 2024

@author: lukasgartmair
"""

import pygame
import random
from pygame_gridcalculator import GridCalculator


class DisplayMode:
    light = 0
    dark = 1


display_mode = DisplayMode.dark

FPS = 5

RND_SEED = random.randint(0, 100)

CARD_RESOLUTION = 50
DECK_SIZE = 60

width = 1920
height = 1080
bounds = (width, height)

grid_width = 18

grid_height = 18

grid = GridCalculator(width, height, grid_width, grid_height)


right_edge = grid.left_point(grid_width * 0.8)
enemy_top_edge = grid.top_point(grid_height * 0.65)

pygame.font.init()

font_size = 65
font_style = pygame.font.match_font("z003")
font = pygame.font.Font(font_style, font_size)
font.set_bold(False)
text_color = (28, 0, 46)

font_size = 25
font_card_title = pygame.font.Font(font_style, font_size)

font_size = 30
font_lore = pygame.font.Font(font_style, font_size)

font_size = 70
font_header2 = pygame.font.Font(font_style, font_size)


font_size = 100
font_header = pygame.font.Font(font_style, font_size)

card_height = 332
card_width = 238

card_scale = 0.75


rect_height = 25


player_1_color = (249, 243, 153)
player_2_color = (28, 0, 46)

middle_edge = int(width * 0.3)
middle_edge_2 = int(width * 0.55)
left_edge = int(width * 0.75)

height_reference_0 = int(height / 3) * 1.2
height_reference_1 = int(height / 2)
height_references = {0: height_reference_0, 1: height_reference_1}

arcane_offset = 25

divider = 7
width_reference_0 = 20
width_reference_1 = int(width / divider) * 1
width_reference_2 = int(width / divider) * 2
width_reference_3 = int(width / divider) * 3
width_reference_4 = int(width / divider) * 4

width_reference_pitch = int(width / divider) * 5

width_reference_pile = int(width / divider) * 6
width_reference_hand = int(width / divider) * 4

width_references = {
    "0": width_reference_0,
    "1": width_reference_1,
    "2": width_reference_2,
    "3": width_reference_3,
    "4": width_reference_4,
    "pile": width_reference_pile,
    "pitch": width_reference_pitch,
    "hand": width_reference_hand,
    "banished": width_reference_pile - 40,
}

text_offset_piles = -100
