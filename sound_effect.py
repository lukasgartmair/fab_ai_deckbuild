#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 21:28:21 2024

@author: lukasgartmair
"""

import pygame


class SoundEffect:
    pygame.mixer.init()
    flip_card = pygame.mixer.Sound("sounds/flip_card_louder.wav")
    # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=91468">Pixabay</a>
    draw_card = pygame.mixer.Sound("sounds/draw_card_short.wav")
    # Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=35956">Pixabay</a>
    attack = pygame.mixer.Sound("sounds/attack.wav")
    # Sound Effect by <a href="https://pixabay.com/users/gamesfxpacks-23801316/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=234986">Cyberwave Orchestra</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=234986">Pixabay</a>
    block = pygame.mixer.Sound("sounds/block_short.wav")
    # Sound Effect by <a href="https://pixabay.com/users/daviddumaisaudio-41768500/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185433">David Dumais</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185433">Pixabay</a>
    die = pygame.mixer.Sound("sounds/die.wav")
    # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=47695">Pixabay</a>
    slap = pygame.mixer.Sound("sounds/slap.wav")
    # Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=90128">Pixabay</a>
    pain = pygame.mixer.Sound("sounds/pain.wav")
    # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=61964">Pixabay</a>
    pistol = pygame.mixer.Sound("sounds/pistol_silenced.wav")
    # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6349">Pixabay</a>
    bow = pygame.mixer.Sound("sounds/bow.wav")
    # Sound Effect by <a href="https://pixabay.com/users/dennish18-26151496/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=146419">Dennis</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=146419">Pixabay</a>
