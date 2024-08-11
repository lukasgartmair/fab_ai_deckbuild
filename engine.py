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
from statemachine.states import States, State


class GameState(Enum):
    starting = 0
    playing = 1
    ended = 2


class GameStateMachine(StateMachine):
    # states = States.from_enum(GameState, initial=GameState.playing)

    starting = State("starting", initial=True)
    playing = State("playing")
    ended = State("ended")

    start_game = starting.to(playing)
    end_game = playing.to(ended)
    restart_game = ended.to(starting)


class GameEngine:
    enemy = None
    state = None

    def __init__(self):
        self.deck = Deck()
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.state_machine = GameStateMachine()

        self.enemy.draw()

    def restart(self):
        self.deck = Deck()
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.state_machine.restart_game()

    def check_win_condition(self):
        print(self.enemy.life)
        if self.enemy.life <= 0:
            print("here")
            self.state_machine.end_game()
            print(self.state_machine.current_state)

    def play(self, player_attack=None, modifiers=None):
        if self.enemy.stance == Stance.defend:
            if self.enemy.further_defense_possible == False:
                print("no more defensive actions from the enemy this turn")
                print("press enter to change the enemy stance to ATTACK")
            else:
                self.enemy.defend(player_attack, modifiers)

        elif self.enemy.stance == Stance.attack:
            if self.enemy.further_attack_possible == False:
                print("no more attacks from the enemy this turn")
                print("press enter to change the enemy stance to DEFEND")

            else:
                self.enemy.attack()
