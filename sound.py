#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 08:32:11 2023

@author: lukasgartmair
"""
import pygame

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
    def __init__(self):
        pygame.mixer.init()

        self.intro_music = pygame.mixer.Sound("sounds/intro_music.wav")

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(VOLUME)

        self.intro_music = pygame.mixer.Sound("sounds/intro_music.wav")

        self.flip_card = pygame.mixer.Sound("sounds/flip_card_louder.wav")
        self.draw_card = pygame.mixer.Sound("sounds/draw_card_short.wav")
        self.attack = pygame.mixer.Sound("sounds/attack.wav")
        self.block = pygame.mixer.Sound("sounds/block_short.wav")
        self.die = pygame.mixer.Sound("sounds/die.wav")
        self.slap = pygame.mixer.Sound("sounds/slap.wav")
        self.pain = pygame.mixer.Sound("sounds/pain.wav")

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

    # Sound Effect by <a href="https://pixabay.com/users/lucadialessandro-25927643/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=143276">Luca Di Alessandro</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=143276">Pixabay</a>

    def play_draw_cards(self, n_cards=1):
        self.card_effects_channel.play(self.draw_card, loops=n_cards - 1)

        # Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=35956">Pixabay</a>

    def play_flip_card(self):
        self.card_effects_channel.play(self.flip_card)
        # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=91468">Pixabay</a>

    def play_change_stance_to_attack(self):
        self.card_effects_channel.play(self.die)
        # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=47695">Pixabay</a>

    def play_attack(self):
        self.card_effects_channel.play(self.attack)
        # Sound Effect by <a href="https://pixabay.com/users/gamesfxpacks-23801316/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=234986">Cyberwave Orchestra</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=234986">Pixabay</a>

    def play_block(self):
        self.card_effects_channel.play(self.block)
        # Sound Effect by <a href="https://pixabay.com/users/daviddumaisaudio-41768500/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185433">David Dumais</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=185433">Pixabay</a>

    def play_not_possible(self):
        self.card_effects_channel.play(self.slap)
        # Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=90128">Pixabay</a>

    def play_pain(self):
        self.card_effects_channel.queue(self.pain)
        # Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=61964">Pixabay</a>
