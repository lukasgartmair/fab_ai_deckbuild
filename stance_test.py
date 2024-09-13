#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:34:42 2024

@author: lukasgartmair
"""

from statemachine import StateMachine
from statemachine.states import State
from enum import Enum
import traceback
from utils import n_chance
from statemachine.contrib.diagram import DotGraphMachine


class Stance(Enum):
    defend = 0
    attack = 1


chance = 0.5


class StanceStateMachine(StateMachine):
    attack = State("attack", initial=True)
    attack_reaction = State("attack_reaction")
    defense = State("defense")
    defensive_reaction = State("defensive_reaction")

    switch_from_defensive_reaction_to_attack = defensive_reaction.to(
        attack, unless="defensive_reaction_left"
    )

    switch_from_attack_to_attack_reaction = attack.to(
        attack_reaction, unless="attacks_left"
    )
    stay_in_attack = attack.to.itself(internal=True)

    switch_from_attack_reaction_to_attack = attack_reaction.to(
        attack, cond="enemy_combat_chain_continues"
    )

    switch_from_attack_reaction_to_defense = attack_reaction.to(
        defense, unless="enemy_combat_chain_continues"
    )

    stay_in_attack_reaction = attack_reaction.to.itself(internal=True)

    switch_from_defense_to_defensive_reaction = defense.to(defensive_reaction)

    switch_from_defensive_reaction_to_defense = defensive_reaction.to(
        defense, cond="enemy_combat_chain_continues"
    )

    stay_in_defensive_reaction = defensive_reaction.to.itself(internal=True)

    cycle = (
        switch_from_attack_to_attack_reaction
        | stay_in_attack
        | switch_from_attack_reaction_to_defense
        | stay_in_attack_reaction
        | switch_from_attack_reaction_to_attack
        | switch_from_defense_to_defensive_reaction
        | switch_from_defensive_reaction_to_defense
        | switch_from_defensive_reaction_to_attack
        | stay_in_defensive_reaction
    )

    def __init__(self):

        super(StanceStateMachine, self).__init__()

    def after_transition(self, event: str, source: State, target: State, event_data):
        print(
            f"Running {event} from {source!s} to {target!s}: {event_data.trigger_data.kwargs!r}"
        )

    def defensive_reaction_left(self):
        return True if n_chance(chance) else False

    def attacks_left(self):
        return True if n_chance(chance) else False

    def attack_reactions_left(self):
        return True if n_chance(chance) else False

    def player_combat_chain_continues(self):
        return True if n_chance(chance) else False

    def enemy_combat_chain_continues(self):
        return True if n_chance(chance) else False

    def change_stance(self):
        # try:
        #     self.send("cycle")
        # except:
        #     tb = traceback.format_exc()
        #     print(tb)

        self.send("cycle")


if __name__ == "__main__":

    sm = StanceStateMachine()
    for i in range(20):
        sm.change_stance()
