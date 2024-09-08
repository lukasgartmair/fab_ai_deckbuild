#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 19:17:10 2024

@author: lukasgartmair
"""

from statemachine import StateMachine
from statemachine.states import State
from enum import Enum
from sound import Sound


class Stance(Enum):
    defend = 0
    attack = 1


class StanceStateMachine(StateMachine):
    attack = State("attack", initial=True)
    attack_reaction = State("attack_reaction")
    defense = State("defense")
    defensive_reaction = State("defensive_reaction")

    switch_from_defensive_reaction_to_attack = defensive_reaction.to(attack)
    switch_from_attack_to_attack_reaction = attack.to(
        attack_reaction, cond="further_attack_reaction_planned"
    )
    switch_from_attack_reaction_to_attack = attack_reaction.to(
        attack, cond="further_attack_planned"
    )

    switch_from_attack_reaction_to_defense = attack_reaction.to(defense)
    switch_from_defense_to_defensive_reaction = defense.to(defensive_reaction)
    switch_from_defensive_reaction_to_defense = defensive_reaction.to(defense)

    cycle = (
        switch_from_attack_to_attack_reaction
        | (
            switch_from_attack_reaction_to_attack
            | switch_from_attack_reaction_to_defense
        )
        | switch_from_defense_to_defensive_reaction
        | (
            switch_from_defensive_reaction_to_defense
            | switch_from_defensive_reaction_to_attack
        )
    )

    def __init__(self):
        self.stance = Stance.attack
        self.sound = Sound()

        if self.stance == Stance.defend:
            self.defense.initial = True
            self.attack.initial = False

        super(StanceStateMachine, self).__init__()

    def on_enter_attack(self):
        self.stance = Stance.attack
        self.sound.play_change_stance_to_attack()

    def on_exit_attack_reaction(self):
        self.stance = Stance.defend

    def on_enter_defense(self):
        self.stance = Stance.defend

    def on_exit_defensive_reaction(self):
        self.stance = Stance.attack

    def change_stance(self):
        self.send("cycle")
