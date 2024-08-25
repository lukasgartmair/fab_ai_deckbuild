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
from level_manager import LevelManager
from attack import Attack
from analyzer import GlobalAnalyzer

from copy import deepcopy


class WinCondition(Enum):
    enemy_died = 0
    enemy_fatigued = 1


class GameStateMachine(StateMachine):
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
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.state_machine = GameStateMachine()
        self.level_manager = LevelManager(level=1)
        self.enemy.initialize_play()
        self.win_condition = None
        self.attack = Attack()

        self.analyzer = GlobalAnalyzer(self)

    # def __deepcopy__(self, memo):

    #     return GameEngine()

    def finish_move(self):
        self.analyzer.write_move_data()
        self.level_manager.advandce_move()

    def finish_turn(self):
        self.level_manager.advandce_turn()

    def advance_level(self):
        self.win_condition = None
        self.enemy = Enemy(play_key=pygame.K_SPACE)
        self.enemy.initialize_play()
        self.state_machine.restart_game()
        self.level_manager.advance_level()

    def check_win_condition(self):
        if self.enemy.life <= 0:
            self.win_condition = WinCondition.enemy_died
            self.state_machine.end_game()

    def check_fatigue_condition(self):
        if len(self.enemy.hand) + len(self.enemy.deck) == 0:
            self.win_condition = WinCondition.enemy_fatigued
            self.state_machine.end_game()
            return True

    def play(self, player_attack=None):
        self.enemy.check_if_further_move_possible()

        if self.enemy.stance == Stance.defend:
            if self.enemy.further_defense_possible == False:
                print("no more defensive actions from the enemy this turn")
                print("press enter to change the enemy stance to ATTACK")
            self.enemy.defend(player_attack)
            self.finish_move()

        elif self.enemy.stance == Stance.attack:
            if self.enemy.further_attack_possible == False:
                print("no more attacks from the enemy this turn")
                print("press enter to change the enemy stance to DEFEND")

            else:
                self.enemy.attack()
            self.finish_move()
