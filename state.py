#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 18:51:08 2024

@author: lukasgartmair
"""

from enum import Enum

from statemachine import StateMachine
from statemachine.states import States


class SettlementSelectionStatus(Enum):
    not_selected = 0
    selected = 1


class SettlementSelectionMachine(StateMachine):

    states = States.from_enum(
        SettlementSelectionStatus, initial=SettlementSelectionStatus.not_selected
    )

    select = states.not_selected.to(states.selected)
    deselect = states.selected.to(states.not_selected)


class SettlementConnectionStatus(Enum):
    not_connected = 0
    connected = 1


class SettlementConnectionMachine(StateMachine):

    states = States.from_enum(
        SettlementConnectionStatus, initial=SettlementConnectionStatus.not_connected
    )

    connect = states.not_connected.to(
        states.connected) | states.connected.to(states.connected)
    disconnect = states.connected.to(states.not_connected)