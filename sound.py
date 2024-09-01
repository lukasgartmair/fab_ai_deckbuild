#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 08:32:11 2023

@author: lukasgartmair
"""

import pygame
from sound_effect import SoundEffect

VOLUME = 0.3

_sound_library = {}


class CustomTimer:
    def __init__(self, cooldown=500):
        self.now = pygame.time.get_ticks()
        self.last = pygame.time.get_ticks()
        self.cooldown = cooldown

    def check(self):
        self.get_now()
        if self.now - self.last >= self.cooldown:
            return True
        else:
            return False

    def set_last(self):
        self.last = self.now

    def get_now(self):
        self.now = pygame.time.get_ticks()


class Sound:
    pygame.mixer.init()

    sound_effect = SoundEffect()

    def __init__(self):
        self.intro_music = pygame.mixer.Sound("sounds/intro_music.wav")

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(VOLUME)

        self.intro_music = pygame.mixer.Sound("sounds/intro_music.wav")

        self.card_effects_channel = pygame.mixer.Channel(2)
        self.card_effects_channel.set_volume(VOLUME)

    def play_intro_music(self):
        pass
        # self.music_channel.play(self.intro_music, loops=-1)
        # Demented Nightmare by Darren Curtis | https://www.darrencurtismusic.com/
        # Music promoted by https://www.chosic.com/free-music/all/
        # Creative Commons CC BY 3.0
        # https://creativecommons.org/licenses/by/3.0/

    def stop_intro_music(self):
        self.music_channel.fadeout(3000)

    def play_outro_music(self):
        self.music_channel.play(self.outro_music, loops=-1)
        # Demented Nightmare by Darren Curtis | https://www.darrencurtismusic.com/
        # Music promoted by https://www.chosic.com/free-music/all/
        # Creative Commons CC BY 3.0
        # https://creativecommons.org/licenses/by/3.0/

    def stop_outro_music(self):
        self.music_channel.fadeout(3000)

    def play_draw_cards(self, n_cards=1):
        self.card_effects_channel.play(self.sound_effect.draw_card, loops=n_cards - 1)

    def play_flip_card(self):
        self.card_effects_channel.queue(self.sound_effect.flip_card)

    def play_change_stance_to_attack(self):
        self.card_effects_channel.queue(self.sound_effect.die)

    def play_attack(self, card):
        if card.sound:
            self.card_effects_channel.play(card.sound)

    def play_block(self):
        self.card_effects_channel.queue(self.sound_effect.block)

    def play_not_possible(self):
        self.card_effects_channel.play(self.sound_effect.slap)

    def play_pain(self):
        self.card_effects_channel.queue(self.sound_effect.pain)

    def play_pistol_shot(self):
        self.card_effects_channel.play(self.sound_effect.pistol_shot)
