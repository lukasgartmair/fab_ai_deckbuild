#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 22:16:22 2024

@author: lukasgartmair
"""

from statemachine import StateMachine
from statemachine.states import State
from playstyle import CardType


class ArsenalStateMachine(StateMachine):
    face_down = State("face_down", initial=True)
    face_up = State("face_up")

    turn_face_up = face_down.to(face_up)
    turn_face_down = face_up.to(face_down)


class Arsenal:
    def __init__(self):
        self.arsenal = []
        self.state_machine = ArsenalStateMachine()

    def fill(self, card):
        self.arsenal.append(card)

    def get_arsenal(self):
        return self.arsenal

    def get_arsenaled_card(self):
        if self.is_empty() == False:
            return self.arsenal[0]

    def get_length(self):
        return len(self.arsenal)

    def remove_card(self, card):
        if card in self.arsenal:
            self.arsenal.remove(card)

    def clear(self):
        self.arsenal = []

    def is_in_arsenal(self, card):
        return True if card in self.arsenal else False

    def is_empty(self):
        return True if len(self.arsenal) == 0 else False

    def get_state(self):
        return self.state_machine.current_state

    def is_defensive_reaction(self):
        return (
            True
            if self.is_empty() == False
            and self.get_arsenaled_card().card_type == CardType.defensive_reaction
            else False
        )

    def is_attack_reaction(self):
        return (
            True
            if self.is_empty() == False
            and self.get_arsenaled_card().card_type == CardType.attack_reaction
            else False
        )
