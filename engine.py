#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:19:33 2023

@author: lukasgartmair
"""

from enum import Enum
import pygame
from deck import Deck
from player import Player
from enemy import Enemy

class GameState(Enum):
    PLAYING = 0
    ENDED = 1

class GameEngine:

    player1 = None
    enemy = None
    state = None
    currentPlayer = None

    def __init__(self):
        self.deck = Deck()
        self.player1 = Player(play_key=pygame.K_SPACE)
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.currentPlayer = self.player1
        self.state = GameState.PLAYING
        
        self.enemy.draw()

    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.enemy
        else:
            self.currentPlayer = self.player1

    def players_turn(self, key):
        if key == None:
            return

        if key == self.currentPlayer.play_key:
            print(len(self.currentPlayer.hand))
            if len(self.currentPlayer.hand) > 0:
                self.currentPlayer.play()
            else:
                self.state = GameState.ENDED
                
