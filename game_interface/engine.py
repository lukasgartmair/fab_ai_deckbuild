#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:19:33 2023

@author: lukasgartmair
"""

from enum import Enum
import pygame
from models import Deck, Player


class GameState(Enum):
    PLAYING = 0
    ENDED = 1

class GameEngine:

    player1 = None
    player2 = None
    state = None
    currentPlayer = None

    def __init__(self):
        self.deck = Deck()
        self.player1 = Player("Aspirant", pygame.K_SPACE)
        self.player2 = Player("Enemy", pygame.K_SPACE)
        self.currentPlayer = self.player1
        self.state = GameState.PLAYING
        self.initialize_player_hands()

    def initialize_player_hands(self):

        self.player1.init_hand()
        self.player2.init_hand()

    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def players_turn(self, key):
        if key == None:
            return

        if key == self.currentPlayer.playKey:
            if len(self.currentPlayer.hand) > 0:
                self.currentPlayer.play()
            else:
                self.state = GameState.ENDED
                
