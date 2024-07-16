#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:59:11 2024

@author: lukasgartmair
"""

from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from beautifultable import beautifultable
import seaborn as sns
sns.set_style("white")

from card import Card, CardColor

class DeckStrategy(Enum):
    defensive = 0
    neutral = 1
    aggressive = 2


strategy_parameters = {
    "aggressive": {"mu": 4, "sigma": 2},
    "neutral": {"mu": 3, "sigma": 1},
    "defensive": {"mu": 1.5, "sigma": 2},
}


def calc_power_distribution(n=500, deck_strategy=DeckStrategy.neutral):
    mu, sigma = (
        strategy_parameters[deck_strategy.name]["mu"],
        strategy_parameters[deck_strategy.name]["sigma"],
    )
    s = np.random.normal(mu, sigma, n)
    s = [np.round(si).astype(int) for si in s if si > 0]
    
    plot = True
    if plot:
        #plt.figure(figsize=(10,7), dpi= 80)
        #sns.distplot(s, color="dodgerblue", label="Compact")
        plt.hist(s,alpha=0.5,label="defensive")
        plt.legend()
        plt.xlabel("power")
        plt.ylabel("#cards")
        
    return s


class Deck:
    def __init__(self):
        self.n_cards = 60
        self.cards = []
        self.stats = {}

        self.strategy = DeckStrategy.defensive

        self.build_deck()
        self.calc_stats()

        self.shuffle()

    def shuffle(self):
        np.random.shuffle(self.cards)

    def build_deck(self):
        power_distribution = calc_power_distribution(deck_strategy=self.strategy)
        self.cards = [
            Card(np.random.choice(power_distribution)) for n in range(self.n_cards)
        ]

    def calc_stats(self):
        self.card_types = [c.card_type.name for c in self.cards]

        self.n_reds = len([c for c in self.cards if c.color == CardColor.red])
        self.n_yellows = len([c for c in self.cards if c.color == CardColor.yellow])
        self.n_blues = len([c for c in self.cards if c.color == CardColor.blue])

        self.powers = [c.power for c in self.cards]
        self.defenses = [c.defense for c in self.cards]
        self.pitches = [c.pitch for c in self.cards]
        self.costs = [c.cost for c in self.cards]

        # fabrary deck stats
        self.in_deck = len(self.cards)
        self.non_blocking = len([c for c in self.cards if c.defense == 0])
        self.attack_actions = len(
            [c for c in self.cards if c.card_type.name == "attack_action"]
        )
        self.non_attack_actions = len(
            [c for c in self.cards if c.card_type.name == "non_attack_action"]
        )

        # averages
        self.cost_avg = np.mean([c.cost for c in self.cards])
        self.pitch_avg = np.mean([c.pitch for c in self.cards])
        # TODO is this power avg only for attack action cards ir all cards?!
        self.power_avg = np.mean(
            [c.power for c in self.cards if c.card_type.name == "attack_action"]
        )
        self.defense_avg = np.mean([c.defense for c in self.cards if c.defense > 0])

    def get_stats(self):
        print("Deck statistics")
        table = beautifultable.BeautifulTable()
        table.columns.header = ["totals", "value", "averages", "value"]
        table.append_row(["in_deck", self.in_deck, "cost_avg", self.cost_avg])
        table.append_row(
            ["non_blocking", self.non_blocking, "pitch_avg", self.pitch_avg]
        )
        table.append_row(
            ["attack_actions", self.attack_actions, "power_avg", self.power_avg]
        )
        table.append_row(
            [
                "non_attack_actions",
                self.non_attack_actions,
                "defense_avg",
                self.defense_avg,
            ]
        )
        print(table)
