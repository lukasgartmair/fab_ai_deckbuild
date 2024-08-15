#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:40:14 2024

@author: lukasgartmair
"""

from fantasynames.hobbit import hobbit
from fantasynames.elf import elf
from fantasynames.dwarf import dwarf
from fantasynames.human_diverse import human

from os import listdir
from os.path import isfile, join
import random


races = ["elf", "dwarf", "human"]


class FantasyIdentity:
    def __init__(self, player_class):
        self.race = random.choice(races)
        self.name = self.get_fantasy_name()
        image_path = "images/" + player_class.name + "/"
        images = [f for f in listdir(image_path) if isfile(join(image_path, f))]
        self.image_number = random.choice(images)

    def get_fantasy_name(self):
        # if self.race == "hobbit":
        #     return hobbit()
        if self.race == "elf":
            return elf()
        elif self.race == "dwarf":
            return dwarf()
        elif self.race == "human":
            return human()
