#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:19:33 2023

@author: lukasgartmair
"""

from enum import Enum
from enemy import Enemy, Stance
from statemachine import StateMachine
from statemachine.states import State
from level_manager import LevelManager
from player_attack import PlayerAttack
from analyzer import GlobalAnalyzer
import random
from playstyle import PlayerClass
from mechanologist import Mechanologist
from guardian import Guardian
from ranger import Ranger


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

        # test_class = PlayerClass.mechanologist

        # self.player_class = test_class
        self.apply_player_class()

        self.state_machine = GameStateMachine()
        self.level_manager = LevelManager(level=1)
        self.enemy.initialize_play()
        self.win_condition = None
        self.player_attack = PlayerAttack()

        self.analyzer = GlobalAnalyzer(self)

    def apply_player_class(self):
        match self.player_class:
            case self.player_class if self.player_class == PlayerClass.mechanologist:
                self.enemy = Mechanologist()
            case self.player_class if self.player_class == PlayerClass.guardian:
                self.enemy = Guardian()
            case self.player_class if self.player_class == PlayerClass.ranger:
                self.enemy = Ranger()

            case _:
                self.enemy = Enemy(self.player_class)

    def finish_move(self, player_attack):
        self.analyzer.write_move_data(player_attack)
        self.level_manager.advandce_move()

    def finish_turn(self):
        self.enemy.finish_turn()
        self.level_manager.advandce_turn()

    def advance_level(self):
        self.win_condition = None
        self.player_class = random.choice(
            [
                p
                for p in list(PlayerClass)
                if p.name != "generic" and p.name != "mechanologist"
            ]
        )

        self.apply_player_class()

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
        if self.level_manager.move_index == 1:
            self.enemy.start_turn()

        self.enemy.start_move()

        print("NEXT MOVE")

        if self.enemy.stance == Stance.defend:
            if self.enemy.check_if_further_defense_possible() == True:
                self.enemy.sound.play_not_possible()

            self.enemy.defend(player_attack)
            self.finish_move(player_attack)

        elif self.enemy.stance == Stance.attack:
            if self.enemy.check_if_further_attack_possible() == True:
                self.enemy.perform_attack()
            else:
                self.enemy.sound.play_not_possible()

            self.finish_move(player_attack)
