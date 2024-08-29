#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 08:32:11 2023

@author: lukasgartmair
"""
import pygame
import os

VOLUME = 0.3

_sound_library = {}


def play_sound(path, loop=0):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace("/", os.sep).replace("\\", os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play(loop)


class Sound:
    def __init__(self):
        pygame.mixer.init()

        self.intro_music = pygame.mixer.Sound("sounds/intro_music.mp3")

        self.intro_music_channel = pygame.mixer.Channel(0)
        self.intro_music_channel.set_volume(VOLUME)

    def play_intro_music(self):
        self.intro_music_channel.play(self.intro_music, loops=-1)
        # Demented Nightmare by Darren Curtis | https://www.darrencurtismusic.com/
        # Music promoted by https://www.chosic.com/free-music/all/
        # Creative Commons CC BY 3.0
        # https://creativecommons.org/licenses/by/3.0/

    def stop_intro_music(self):
        print("stopping")
        self.intro_music_channel.fadeout(3000)

    def draw_card(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def banish_card(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def loose_hp(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def play_strong_card(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def change_stance_to_defense(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def change_stance_to_attack(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)

    def play_outro_music(self):
        draw_card_path = "sounds/place_settlement.wav"
        play_sound(draw_card_path, loop=0)
