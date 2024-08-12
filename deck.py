#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:59:11 2024

@author: lukasgartmair
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from beautifultable import beautifultable
from playstyle import PlayerClass, CardType, Playstyle
from settings import DECK_SIZE
from card import Card, CardColor
from utils import n_chance


def calc_physical_distribution(playstyle_obj, n=DECK_SIZE):
    mu, sigma = (
        playstyle_obj.strategy_parameters["mu"],
        playstyle_obj.strategy_parameters["sigma"],
    )
    s = np.random.normal(mu, sigma, n)
    s = [np.round(si).astype(int) if si > 0 else 0 for si in s]

    plot = False
    if plot:
        plt.hist(s, alpha=0.5, label=str(playstyle_obj))
        plt.legend()
        plt.xlabel("physical")
        plt.ylabel("#cards")

    return s


def calc_keyword_distribution(playstyle_obj, n=DECK_SIZE):
    sampled_keywords = random.choices(
        playstyle_obj.keywords, weights=playstyle_obj.keyword_ratios.values(), k=n
    )
    return sampled_keywords


def calc_card_type_distribution(playstyle_obj, n=DECK_SIZE):
    sampled_card_types = random.choices(
        [
            c
            for c in CardType
            if c
            in [
                CardType.attack_action,
                CardType.non_attack_action,
                CardType.attack_reaction,
                CardType.defensive_reaction,
            ]
        ],
        weights=playstyle_obj.card_type_ratios.values(),
        k=n,
    )
    return sampled_card_types


def create_arcane_cards(cards, arcane_ratio, n=DECK_SIZE):
    arcane_cards = random.choices(list(cards), k=int(n * arcane_ratio))

    for ac in arcane_cards:
        ac.adjust_arcane_physical()


def calc_card_color_distribution(playstyle_obj, n=DECK_SIZE):
    sampled_card_colors = random.choices(
        list(CardColor), weights=playstyle_obj.pitch_ratios.values(), k=n
    )
    return sampled_card_colors


class Deck:
    def __init__(self, player_class=PlayerClass.generic, playstyle=Playstyle()):
        self.n_cards = DECK_SIZE
        self.cards = []
        self.stats = {}

        self.player_class = player_class
        self.playstyle = playstyle
        self.build_deck()
        self.calc_stats()
        self.get_stats()

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)

    def build_deck(self):
        physical_distribution = calc_physical_distribution(self.playstyle)
        physical_distribution = [1 if x == 0 else x for x in physical_distribution]
        keyword_distribution = calc_keyword_distribution(self.playstyle)
        card_type_distribution = calc_card_type_distribution(self.playstyle)
        card_color_distribution = calc_card_color_distribution(self.playstyle)

        self.cards = [Card() for n in range(self.n_cards)]

        for c in self.cards:
            if n_chance(p=0.4):
                c.card_class = self.player_class

        indices = list(range(len(self.cards)))
        random.shuffle(indices)
        for i, card in enumerate(self.cards):
            card.color = card_color_distribution[indices[i]]
            card.physical = physical_distribution[indices[i]]
            card.keywords = [keyword_distribution[indices[i]]]
            card.card_type = card_type_distribution[indices[i]]

            card.calc_card_values()

        if self.playstyle.arcane_ratio > 0:
            create_arcane_cards(self.cards, self.playstyle.arcane_ratio)

        # print("deck contents:")
        # for i, c in enumerate(self.cards):
        #     print("Card {}: {}".format(i, c.name))

    def calc_stats(self):
        self.card_types = [c.card_type.name for c in self.cards]

        self.n_reds = len([c for c in self.cards if c.color == CardColor.red])
        self.n_yellows = len([c for c in self.cards if c.color == CardColor.yellow])
        self.n_blues = len([c for c in self.cards if c.color == CardColor.blue])

        self.physicals = [c.physical for c in self.cards]
        self.defenses = [c.defense for c in self.cards]
        self.pitches = [c.pitch for c in self.cards]
        self.costs = [c.cost for c in self.cards]

        self.keywords = [c.keywords for c in self.cards if c is not None]

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
        # TODO is this physical avg only for attack action cards ir all cards?!
        self.physical_avg = np.mean(
            [c.physical for c in self.cards if c.card_type.name == "attack_action"]
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
            ["attack_actions", self.attack_actions, "physical_avg", self.physical_avg]
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
