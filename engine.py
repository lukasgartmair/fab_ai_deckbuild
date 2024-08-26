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
import random
from playstyle import PlayerClass
from mechanologist import Mechanologist


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
        self.player_class = random.choice(
            [
                p
                for p in list(PlayerClass)
                if p.name != "generic" and p.name != "mechanologist"
            ]
        )

        # self.player_class = PlayerClass.wizard

        if self.player_class == PlayerClass.mechanologist:
            self.enemy = Mechanologist()
        else:
            self.enemy = Enemy(self.player_class)

        self.state_machine = GameStateMachine()
        self.level_manager = LevelManager(level=1)
        self.enemy.initialize_play()
        self.win_condition = None
        self.attack = Attack()

        self.analyzer = GlobalAnalyzer(self)

    def finish_move(self, player_attack):
        self.analyzer.write_move_data(player_attack)
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
        if self.enemy.life_counter.life <= 0:
            self.win_condition = WinCondition.enemy_died
            self.state_machine.end_game()

    def check_fatigue_condition(self):
        if len(self.enemy.hand) + self.enemy.deck.get_length() == 0:
            self.win_condition = WinCondition.enemy_fatigued
            self.state_machine.end_game()
            return True

    def play(self, player_attack=None):
        self.enemy.start_move()

        if self.enemy.stance == Stance.defend:
            if self.enemy.further_defense_possible == False:
                print("no more defensive actions from the enemy this turn")
                print("press enter to change the enemy stance to ATTACK")
            self.enemy.defend(player_attack)
            self.finish_move(player_attack)

        elif self.enemy.stance == Stance.attack:
            if self.enemy.further_attack_possible == False:
                print("no more attacks from the enemy this turn")
                print("press enter to change the enemy stance to DEFEND")

            else:
                self.enemy.attack()
            self.finish_move(player_attack)
