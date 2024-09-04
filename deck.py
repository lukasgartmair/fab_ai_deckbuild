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
from playstyle import PlayerClass, CardType, Playstyle, Keyword, SecondaryKeyword
from settings import DECK_SIZE, CARD_RESOLUTION
from card import (
    Card,
    CardColor,
    MAX_PHYSICAL_ATTACK,
    generate_rnd_image,
    img_to_surfarray,
)
from utils import n_chance
from multiprocessing import Pool, cpu_count


def calc_physical_distribution(playstyle_obj, n=DECK_SIZE):
    s = np.random.normal(
        playstyle_obj.physical_parameters["mu"],
        playstyle_obj.physical_parameters["sigma"],
        n,
    )
    s = [np.round(si).astype(int) if si > 0 else 0 for si in s]
    s = [si if si >= MAX_PHYSICAL_ATTACK else si for si in s]

    plot = False
    if plot:
        plt.hist(s, alpha=0.5, label=str(playstyle_obj))
        plt.legend()
        plt.xlabel("physical")
        plt.ylabel("#cards")

    return s


def calc_keyword_distribution(playstyle_obj, n=DECK_SIZE):
    # print(type(playstyle_obj).__name__)
    # print(playstyle_obj.keywords)
    # print(playstyle_obj.keyword_ratios.values())

    sampled_keywords = random.choices(
        playstyle_obj.keywords, weights=playstyle_obj.keyword_ratios.values(), k=n
    )
    return sampled_keywords


def calc_secondary_keyword_distribution(playstyle_obj, n=DECK_SIZE):
    # print(type(playstyle_obj).__name__)
    # print(playstyle_obj.keywords)
    # print(playstyle_obj.keyword_ratios.values())

    sampled_keywords = random.choices(
        playstyle_obj.secondary_keywords,
        weights=playstyle_obj.secondary_keyword_ratios.values(),
        k=n,
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


def calc_arcane_distribution(playstyle_obj):
    s = np.random.normal(
        playstyle_obj.arcane_parameters["mu"],
        playstyle_obj.arcane_parameters["sigma"],
        int(playstyle_obj.arcane_ratio * DECK_SIZE),
    )
    s = [np.round(si).astype(int) if si > 0 else 0 for si in s]

    plot = False
    if plot:
        plt.hist(s, alpha=0.5, label=str(playstyle_obj))
        plt.legend()
        plt.xlabel("arcane")
        plt.ylabel("#cards")

    return s


def calc_card_color_distribution(playstyle_obj, n=DECK_SIZE):
    sampled_card_colors = random.choices(
        list(CardColor), weights=playstyle_obj.pitch_ratios.values(), k=n
    )
    return sampled_card_colors


def calc_card_class_distribution(playstyle_obj, n=DECK_SIZE):
    sampled_card_classes = random.choices(
        playstyle_obj.card_classes,
        weights=playstyle_obj.card_class_ratios.values(),
        k=n,
    )
    return sampled_card_classes


def calc_card_images(n=DECK_SIZE):
    results = []
    for i in range(n):
        results.append(generate_rnd_image(size=CARD_RESOLUTION))
    return results


# def calc_card_images_pool(n=DECK_SIZE):
#     card_images = calc_card_images()
#     return [img_to_surfarray(r) for r in card_images]


def calc_card_images_pool(n=DECK_SIZE):
    results = []
    n_pools = cpu_count()
    with Pool(n_pools) as p:
        results = p.map(
            calc_card_images, [np.ceil(DECK_SIZE / n_pools).astype(int)] * n_pools
        )

    r2 = []
    for r in results:
        for ri in r:
            r2.append(img_to_surfarray(ri))
    return r2[:DECK_SIZE]


class Deck:
    def __init__(
        self,
        player_class=PlayerClass.generic,
        playstyle=Playstyle(),
        deck_size=DECK_SIZE,
        card_resolution=5,
    ):
        self.n_cards = deck_size
        self.cards = []
        self.stats = {}

        self.card_resolution = card_resolution

        self.player_class = player_class
        self.playstyle = playstyle
        self.build_deck()
        self.calc_stats()

        self.print_stats()

        calc_card_images()

    def is_empty(self):
        return True if self.get_length() == 0 else False

    def shuffle(self):
        np.random.shuffle(self.cards)

    def put_to_bottom(self, card):
        self.cards.insert(0, card)

    def draw_top_cards(self, n=1):
        if len(self.cards) > 0:
            if n == 1:
                return [self.cards.pop()]
            else:
                drawn_cards = self.cards[-n:].copy()
                self.cards = self.cards[:-n]
                return drawn_cards
        else:
            return []

    def draw_top_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def get_length(self):
        return len(self.cards)

    def build_deck(self):
        physical_distribution = calc_physical_distribution(self.playstyle)
        physical_distribution = [1 if x == 0 else x for x in physical_distribution]

        if self.playstyle.arcane_ratio > 0:
            arcane_distribution = calc_arcane_distribution(self.playstyle)
            arcane_distribution = [1 if x == 0 else x for x in arcane_distribution]

        keyword_distribution = calc_keyword_distribution(self.playstyle)
        secondary_keyword_distribution = calc_secondary_keyword_distribution(
            self.playstyle
        )
        card_type_distribution = calc_card_type_distribution(self.playstyle)
        card_color_distribution = calc_card_color_distribution(self.playstyle)
        card_class_distribution = calc_card_class_distribution(self.playstyle)

        card_images = calc_card_images_pool()

        self.cards = [
            Card(card_resolution=self.card_resolution) for n in range(self.n_cards)
        ]

        for c in self.cards:
            if n_chance(p=0.4):
                c.card_class = self.player_class

        indices = list(range(len(self.cards)))
        random.shuffle(indices)

        if self.playstyle.arcane_ratio > 0:
            arcane_indices = list(
                range(int(len(self.cards) * self.playstyle.arcane_ratio))
            )
            random.shuffle(arcane_indices)

        for i, card in enumerate(self.cards):
            card.color = card_color_distribution.pop()
            card.physical = physical_distribution.pop()

            card.keywords = [keyword_distribution.pop()]
            card.card_type = card_type_distribution.pop()

            if card.card_type == CardType.non_attack_action:
                card.keywords = [Keyword.go_again]

            if secondary_keyword_distribution[-1] not in card.keywords:
                card.keywords.append(secondary_keyword_distribution.pop())

            card.keywords.sort(key=lambda x: x.value, reverse=False)

            card.card_class = card_class_distribution[indices[i]]
            card.image = card_images[indices[i]]

            if self.playstyle.arcane_ratio > 0:
                if card.card_type != CardType.defensive_reaction:
                    if len(arcane_distribution) > 0:
                        card.arcane = arcane_distribution.pop()

            card.initialize()

        # print("deck contents:")
        # for i, c in enumerate(self.cards):
        #     print("Card {}: {}".format(i, c.name))

    def calc_stats(self):
        self.stats["card_types"] = [c.card_type.name for c in self.cards]

        self.stats["sn_reds"] = len([c for c in self.cards if c.color == CardColor.red])
        self.stats["n_yellows"] = len(
            [c for c in self.cards if c.color == CardColor.yellow]
        )
        self.stats["n_blues"] = len(
            [c for c in self.cards if c.color == CardColor.blue]
        )

        self.stats["physicals"] = [c.physical for c in self.cards]
        self.stats["defenses"] = [c.defense for c in self.cards]
        self.stats["pitches"] = [c.pitch for c in self.cards]
        self.stats["costs"] = [c.cost for c in self.cards]

        self.stats["keywords"] = [c.keywords for c in self.cards if c is not None]

        # fabrary deck stats
        self.stats["in_deck"] = len(self.cards)
        self.stats["non_blocking"] = len([c for c in self.cards if c.defense == 0])
        self.stats["attack_actions"] = len(
            [c for c in self.cards if c.card_type.name == "attack_action"]
        )
        self.stats["non_attack_actions"] = len(
            [c for c in self.cards if c.card_type.name == "non_attack_action"]
        )

        # averages
        self.stats["cost_avg"] = np.mean([c.cost for c in self.cards])
        self.stats["pitch_avg"] = np.mean([c.pitch for c in self.cards])
        # TODO is this physical avg only for attack action cards ir all cards?!
        self.stats["physical_avg"] = np.mean(
            [c.physical for c in self.cards if c.card_type.name == "attack_action"]
        )
        self.stats["defense_avg"] = np.mean(
            [c.defense for c in self.cards if c.defense > 0]
        )

    def print_stats(self):
        print("Deck statistics")
        table = beautifultable.BeautifulTable()
        table.columns.header = ["totals", "value", "averages", "value"]
        table.append_row(
            ["in_deck", self.stats["in_deck"], "cost_avg", self.stats["cost_avg"]]
        )
        table.append_row(
            [
                "non_blocking",
                self.stats["non_blocking"],
                "pitch_avg",
                self.stats["pitch_avg"],
            ]
        )
        table.append_row(
            [
                "attack_actions",
                self.stats["attack_actions"],
                "physical_avg",
                self.stats["physical_avg"],
            ]
        )
        table.append_row(
            [
                "non_attack_actions",
                self.stats["non_attack_actions"],
                "defense_avg",
                self.stats["defense_avg"],
            ]
        )
        print(table)
