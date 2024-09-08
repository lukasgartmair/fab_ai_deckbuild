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
from stance import StanceStateMachine


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

        test_class = PlayerClass.ninja

        self.player_class = test_class
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

    def trigger_stance_switch(self):
        self.enemy.stance_state_machine.change_stance()

        print("CURRENT STRATE")
        print(self.enemy.stance_state_machine.current_state)

        match self.enemy.stance_state_machine.current_state:
            case self.enemy.stance_state_machine.current_state if self.enemy.stance_state_machine.current_state == self.enemy.stance_state_machine.defense:
                self.finish_turn()

            case self.enemy.stance_state_machine.current_state if self.enemy.stance_state_machine.current_state == self.enemy.stance_state_machine.attack:
                self.enemy.switch_to_offense()

            case _:
                pass

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
        if len(self.enemy.hand) == 0 and self.enemy.deck.is_empty():
            self.win_condition = WinCondition.enemy_fatigued
            self.state_machine.end_game()
            return True

    def play(self, player_attack=None):
        if self.level_manager.move_index == 1:
            self.enemy.start_turn()

        self.enemy.start_move()

        print("NEXT MOVE")

        current_state = self.enemy.stance_state_machine.current_state
        match current_state:
            case current_state if current_state == self.enemy.stance_state_machine.defense:
                if self.enemy.check_if_further_defense_possible() == False:
                    self.enemy.sound.play_not_possible()
                self.enemy.defend(player_attack)
                self.finish_move(player_attack)
            case current_state if current_state == self.enemy.stance_state_machine.defensive_reaction:
                if self.enemy.check_if_further_defensive_reaction_possible() == False:
                    self.enemy.perform_defensive_reaction(player_attack)
                else:
                    self.enemy.sound.play_not_possible()

                self.finish_move(player_attack)

            case current_state if current_state == self.enemy.stance_state_machine.attack:
                if self.enemy.check_if_further_attack_possible() == True:
                    self.enemy.perform_attack()
                else:
                    self.enemy.sound.play_not_possible()

            case current_state if current_state == self.enemy.stance_state_machine.attack_reaction:
                if self.enemy.check_if_further_attack_reaction_possible() == True:
                    self.enemy.perform_attack()
                else:
                    self.enemy.sound.play_not_possible()

        self.level_manager.move_index += 1
