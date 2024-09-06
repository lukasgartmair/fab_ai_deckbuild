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

    switch_to_attack = defensive_reaction.to(attack)
    switch_to_attack_reaction = attack.to(attack_reaction)
    switch_to_defense = attack_reaction.to(defense)
    switch_to_defensive_reaction = defense.to(defensive_reaction)

    cycle = (
        switch_to_attack
        | switch_to_attack_reaction
        | switch_to_defense
        | switch_to_defensive_reaction
    )

    def __init__(self):
        self.stance = Stance.attack
        self.sound = Sound()

        if self.stance == Stance.defend:
            self.defsense.initial = True
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
