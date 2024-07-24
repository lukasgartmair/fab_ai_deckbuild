#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:19:33 2023

@author: lukasgartmair
"""

from enum import Enum
import pygame
from deck import Deck
from enemy import Enemy, Stance

from statemachine import StateMachine
from statemachine.states import States


class GameState(Enum):
    playing = 0
    ended = 1


class GameStateMachine(StateMachine):
    states = States.from_enum(GameState, initial=GameState.playing)

    end = states.playing.to(states.ended)


class GameEngine:
    enemy = None
    state = None

    def __init__(self):
        self.deck = Deck()
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.state = GameState.playing

        self.enemy.draw()

    def switch_stance(self):
        if self.enemy.stance == Stance.defend:
            self.enemy.stance = Stance.attack
        else:
            self.enemy.stance = Stance.defend

        self.enemy.finish_phase()

    def play(self):
        if self.enemy.stance == Stance.defend:
            if self.enemy.check_if_further_defense_possible() == False:
                print("no more defensive actions from the enemy this turn")
                print("press enter to change the enemy stance to ATTACK")
            else:
                self.enemy.defend()

        elif self.enemy.stance == Stance.attack:
            self.enemy.calc_possible_attacks()
            if self.enemy.check_if_further_attack_possible() == False:
                print("no more attacks from the enemy this turn")
                print("press enter to change the enemy stance to DEFEND")

            else:
                self.enemy.attack()
