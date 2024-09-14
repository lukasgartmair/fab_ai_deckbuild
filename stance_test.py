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

    combat_chain_start_enemy = State("combat_chain_start_enemy")
    combat_chain_end_enemy = State("combat_chain_end_enemy")

    combat_chain_start_player = State("combat_chain_start_player", initial=True)
    combat_chain_end_player = State("combat_chain_end_player")

    attack = State("attack")
    attack_reaction = State("attack_reaction")
    defense = State("defense")
    defensive_reaction = State("defensive_reaction")

    ### OFFENSE ###

    switch_from_combat_chain_start_enemy_to_attack = combat_chain_start_enemy.to(attack)

    stay_in_attack = attack.to.itself(internal=True, cond="attacks_left")

    switch_from_attack_to_attack_reaction = attack.to(attack_reaction)

    stay_in_attack_reaction = attack_reaction.to.itself(
        internal=True, cond="attack_reaction_left"
    )

    switch_from_attack_reaction_to_attack = attack_reaction.to(
        attack, cond="enemy_combat_chain_continues"
    )

    switch_from_attack_reaction_to_combat_chain_end_enemy = attack_reaction.to(
        combat_chain_end_enemy
    )

    switch_from_combat_chain_end_enemy_to_combat_chain_start_player = (
        combat_chain_end_enemy.to(combat_chain_start_player)
    )

    ### DEFENSE ###

    switch_from_combat_chain_start_player_to_defense = combat_chain_start_player.to(
        defense,
    )

    switch_from_defense_to_defensive_reaction = defense.to(defensive_reaction)

    stay_in_defensive_reaction = defensive_reaction.to.itself(
        internal=True, cond="defensive_reaction_left"
    )

    switch_from_defensive_reaction_to_defense = defensive_reaction.to(
        defense, cond="player_combat_chain_continues"
    )

    switch_from_defensive_reaction_to_combat_chain_end_player = defensive_reaction.to(
        combat_chain_end_player
    )

    switch_from_combat_chain_end_player_to_combat_chain_start_enemy = (
        combat_chain_end_player.to(combat_chain_start_enemy)
    )

    cycle = (
        switch_from_combat_chain_start_enemy_to_attack
        | switch_from_attack_to_attack_reaction
        | stay_in_attack
        | switch_from_attack_reaction_to_attack
        | switch_from_attack_reaction_to_combat_chain_end_enemy
        | stay_in_attack_reaction
        | switch_from_combat_chain_end_enemy_to_combat_chain_start_player
        | switch_from_combat_chain_start_player_to_defense
        | switch_from_defense_to_defensive_reaction
        | switch_from_defensive_reaction_to_defense
        | switch_from_defensive_reaction_to_combat_chain_end_player
        | switch_from_combat_chain_end_player_to_combat_chain_start_enemy
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

    def attack_reaction_left(self):
        return True if n_chance(chance) else False

    def player_combat_chain_continues(self):
        return True if n_chance(chance) else False

    def enemy_combat_chain_continues(self):
        return True if n_chance(chance) else False

    def any_combat_chain_continues(self):
        return (
            True
            if any(
                [
                    self.player_combat_chain_continues(),
                    self.enemy_combat_chain_continues(),
                ]
            )
            else False
        )

    def change_stance(self):
        # try:
        #     self.send("cycle")
        # except:
        #     tb = traceback.format_exc()
        #     print(tb)

        self.send("cycle")


if __name__ == "__main__":

    sm = StanceStateMachine()
    for i in range(100):
        sm.change_stance()
