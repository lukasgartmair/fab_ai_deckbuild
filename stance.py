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
import traceback


class Stance(Enum):
    defend = 0
    attack = 1


class StanceStateMachine(StateMachine):
    attack = State("attack", initial=True)
    attack_reaction = State("attack_reaction")
    defense = State("defense")
    defensive_reaction = State("defensive_reaction")

    switch_from_defensive_reaction_to_attack = defensive_reaction.to(
        attack, unless=["player_combat_chain_continues", "defensive_reaction_left"]
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
        defense, cond="player_combat_chain_continues"
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

    def __init__(self, enemy):
        self.stance = Stance.attack
        self.sound = Sound()
        self.enemy = enemy
        self.continue_combat_chain = None
        self.defensive_reaction_left = None

        if self.stance == Stance.defend:
            self.defense.initial = True
            self.attack.initial = False

        super(StanceStateMachine, self).__init__()

    def on_enter_attack(self):
        self.continue_combat_chain = None
        self.stance = Stance.attack
        self.sound.play_change_stance_to_attack()

    def on_exit_attack_reaction(self):
        self.stance = Stance.defend
        self.enemy.finish_turn()

    def on_enter_defense(self):
        self.continue_combat_chain = False
        self.stance = Stance.defend
        self.enemy.start_move()

    def on_enter_defensive_reaction(self):
        self.enemy.start_move()

    def on_exit_defensive_reaction(self):
        self.stance = Stance.attack
        self.enemy.exit_defensive_reaction()

    def after_transition(self, event: str, source: State, target: State, event_data):
        print(
            f"Running {event} from {source!s} to {target!s}: {event_data.trigger_data.kwargs!r}"
        )

    def defensive_reaction_left(self):
        return True if self.defensive_reaction_left == True else False

    def attacks_left(self):
        if self.enemy.combat_chain.is_empty() == True:
            return False
        current_link = self.enemy.combat_chain.get_current_link()

        if current_link is None:
            current_link = self.enemy.combat_chain.get_next_link()

        if current_link is not None:
            return False if current_link.attack_step_finished() == True else True
        else:
            return False

    def attack_reactions_left(self):
        return True if self.enemy.further_attack_reaction_planned() == True else False

    def player_combat_chain_continues(self):
        return True if self.continue_combat_chain == True else False

    def enemy_combat_chain_continues(self):
        return (
            True if self.enemy.combat_chain.has_unplayed_links_left() == True else False
        )

    def change_stance(self):
        # try:
        #     self.send("cycle")
        # except:
        #     tb = traceback.format_exc()
        #     print(tb)

        self.send("cycle")
