#!/usr/bin/env python3
# -*- coding= utf-8 -*-
"""
Created on Fri Aug  9 19=27=38 2024

@author= lukasgartmair
"""

from colorir import *
from settings import display_mode, DisplayMode

color_palette_dark_mode = Palette(
    white="#ffffff",
    color0="#5A3044",
    color1="#382831",
    color2="#593D5C",
    color3="#BF3240",
    color4="#D93D4E",
    color5="ffbe55",
    green="#367040",
    black="000000",
    text_color="ffffff",
)

color_palette_light_mode = Palette(
    white="#ffffff",
    color0="#5A3044",
    color1="#382831",
    color2="#593D5C",
    color3="#BF3240",
    color4="#D93D4E",
    text_color="ffffff",
)


def get_color_palette():
    if display_mode == DisplayMode.light:
        return color_palette_light_mode
    else:
        return color_palette_dark_mode


color_palette = get_color_palette()
