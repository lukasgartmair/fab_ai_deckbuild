#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:22:55 2024

@author: lukasgartmair
"""

FPS = 10

width = 1500
height = 550
bounds = (width, height)


player_1_color = (249, 243, 153)
player_2_color = (28, 0, 46)

right_edge = int(width * 0.1)
middle_edge = int(width * 0.3)
middle_edge_2 = int(width * 0.55)
left_edge = int(width * 0.75)

height_reference_0 = int(height / 3) * 1.2
height_reference_1 = int(height / 2)
height_references = {0: height_reference_0, 1: height_reference_1}

divider = 7
width_reference_0 = int(width / divider)
width_reference_1 = int(width / divider) * 2
width_reference_2 = int(width / divider) * 3
width_reference_3 = int(width / divider) * 4

width_reference_4 = int(width / 5) * 4

width_references = {
    0: width_reference_0,
    1: width_reference_1,
    2: width_reference_2,
    3: width_reference_3,
    4: width_reference_4,
}
