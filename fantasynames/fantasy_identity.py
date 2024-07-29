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

mypath = "images/enemy_images"
images = [f for f in listdir(mypath) if isfile(join(mypath, f))]

import random

classes = ["hobbit","elf","dwarf","human"]

class FantasyIdentity:
    def __init__(self):
        self.race = random.choice(classes)
        self.name = self.get_fantasy_name()
        self.image = random.choice(images)
        
    def get_fantasy_name(self):
    
        if self.race == "hobbit":
            return hobbit()
        elif self.race == "elf":
            return elf() 
        elif self.race == "dwarf":
            return dwarf() 
        elif self.race == "human":
            return human() 