#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
"""

import sys
import traceback
import pygame
from card import card_colors
from enemy import Stance
from engine import GameState, GameEngine
from input_box import InputBox


from settings import (
    player_1_color,
    player_2_color,
    bounds,
    width_references,
    FPS,
    height_references,
    card_height,
    card_width,
    card_scale,
    cardBack,
    font_card_title,
    font,
    text_color,
    text_offset_piles,
)


class Game:
    def __init__(self):
        self.engine = GameEngine()
        self.window = pygame.display.set_mode(bounds)
        pygame.display.set_caption("Flesh and Blood AI enemy")

        self.input_box = InputBox(self.window)

        self.background = pygame.image.load("images/background.png")
        self.background = pygame.transform.smoothscale(
            self.background, self.window.get_size()
        )

    @staticmethod
    def quit_everything(active_scene=None):
        if active_scene:
            active_scene.terminate()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def render_background(self):
        self.window.blit(self.background, (0, 0))

    def render_end_background(self):
        self.background_bw = pygame.image.load("images/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))

    def render_attack_value(self, player_attack_value):
        text = font.render(
            str(player_attack_value) + " attack value",
            True,
            text_color,
        )
        self.window.blit(
            text,
            (
                width_references["pitch"] - 25,
                height_references[0] + text_offset_piles * 2,
            ),
        )

    def render_floating_resources(self):
        text = font.render(
            str(self.engine.enemy.floating_resources) + " floating resources",
            True,
            text_color,
        )
        self.window.blit(
            text,
            (
                width_references["pitch"] - 25,
                height_references[0] + text_offset_piles * 2,
            ),
        )

    def render_deck_pile(self):
        if len(self.engine.enemy.deck) > 0:
            self.window.blit(cardBack, (width_references["pile"], height_references[0]))

        text = font.render(str(len(self.engine.enemy.deck)) + " deck", True, "white")
        self.window.blit(
            text, (width_references["pile"], height_references[0] + text_offset_piles)
        )

    def render_hand(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " hand", True, "white")
        self.window.blit(
            text,
            (width_references["hand"], height_references[0] + text_offset_piles * 2),
        )

    def render_pitch_pile(self):
        if len(self.engine.enemy.pitched_cards) > 0:
            for pc in self.engine.enemy.pitched_cards:
                self.render_card("pitch", pc, width_references, height_references)

        text = font.render(
            str(len(self.engine.enemy.pitched_cards)) + " pitch",
            True,
            "white",
        )
        self.window.blit(
            text, (width_references["pitch"], height_references[0] + text_offset_piles)
        )

    def render_card(self, i, current_card, width_references, height_references):
        offset_factor = 1.35

        print(current_card)
        current_card.image = pygame.transform.scale(
            current_card.image,
            (int(card_width * card_scale), int(card_height * card_scale)),
        )
        self.window.blit(
            current_card.image, (width_references[str(i)], height_references[0])
        )

        # NAME
        self.rect = pygame.draw.rect(
            self.window,
            card_colors[current_card.color.name],
            (width_references[str(i)], height_references[0], card_width * 0.75, 25),
        )

        text = font_card_title.render(str(current_card.name), True, "black")

        self.window.blit(text, (width_references[str(i)], height_references[0]))

        # TYPE
        self.rect = pygame.draw.rect(
            self.window,
            "white",
            (
                width_references[str(i)],
                height_references[0] + card_height // 1.475,
                card_width * 0.75,
                25,
            ),
        )

        text = font_card_title.render(str(current_card.type.name), True, "black")

        self.window.blit(
            text,
            (width_references[str(i)], height_references[0] + card_height // 1.475),
        )

        # POWER
        text = font.render(str(current_card.power), True, "yellow")

        self.window.blit(
            text,
            (
                width_references[str(i)],
                height_references[0] + (card_height // offset_factor),
            ),
        )

        # DEFENSE
        text = font.render(str(current_card.defense), True, "black")

        self.window.blit(
            text,
            (
                width_references[str(i)] + card_width // 2,
                height_references[0] + (card_height // offset_factor),
            ),
        )

        # PITCH
        text = font.render(
            str(current_card.pitch), True, card_colors[current_card.color.name]
        )

        self.window.blit(
            text,
            (
                width_references[str(i)],
                height_references[0]
                - (card_height - card_height // offset_factor - 30),
            ),
        )

        # COST
        text = font.render(str(current_card.cost), True, "red")
        self.window.blit(
            text,
            (
                width_references[str(i)] + card_width // 2,
                height_references[0]
                - (card_height - card_height // offset_factor - 30),
            ),
        )

    def render_enemy_life(self):
        text = font.render(str(len(self.engine.enemy.hand)) + " life", True, "white")
        self.window.blit(
            text,
            (width_references["hand"], height_references[0] + text_offset_piles * 2),
        )

    def render_enemy_play(self):
        for i, current_card in enumerate(self.engine.enemy.played_cards):
            self.render_card(i, current_card, width_references, height_references)

    def render_turn_text(self):
        if self.engine.state == GameState.playing:
            color = None

            if self.engine.enemy.stance == Stance.defend:
                color = player_2_color

            else:
                color = player_1_color

            text = font.render(
                "enemy " + self.engine.enemy.stance.name + "ing", True, color
            )

            self.window.blit(text, (20, 50))

    def render_win(self):
        self.render_end_background()

        message = "The " + self.engine.currentPlayer.name + " trancended!"
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))

    def render_start_screen(self):
        self.background_start = pygame.image.load("images/background_start.png")
        self.window.blit(self.background_start, (0, 0))

        message = "Enter the abyss..."
        text = font.render(message, True, (100, 0, 0))
        self.window.blit(text, (20, 50))
        pygame.display.update()

    def render_initial_game_state(self):
        self.render_background()
        self.render_hand()

        message = ""
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))

        self.input_box.render()

        self.render()

        pygame.display.update()

    def render(self):
        self.render_background()

        self.render_enemy_play()

        self.render_floating_resources()

        self.render_deck_pile()

        self.render_hand()

        self.render_pitch_pile()

        self.render_turn_text()

        if self.engine.state == GameState.ended:
            self.render_win()

    def run(self):
        run = True

        clock = pygame.time.Clock()

        self.render_initial_game_state()

        self.input_box.player_attack_value = None

        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                self.input_box.check_activation(event)

                if event.type == pygame.KEYDOWN:
                    self.input_box.update(event=event)

                    if event.key == pygame.K_SPACE:
                        self.render()

                        if self.engine.state == GameState.playing:
                            if self.engine.enemy.stance == Stance.defend:
                                if self.input_box.active:
                                    self.input_box.player_attack_value = (
                                        self.input_box.send_input()
                                    )
                                    if self.input_box.player_attack_value is not None:
                                        self.input_box.player_attack_value = int(
                                            self.input_box.player_attack_value
                                        )

                                        print(self.input_box.player_attack_value)
                                        self.engine.play(
                                            self.input_box.player_attack_value
                                        )
                                        self.input_box.reset()

                            else:
                                self.engine.play(self.input_box.player_attack_value)

                        self.render_background()
                        self.render()

                    if event.key == pygame.K_RETURN:
                        if self.input_box.active:
                            self.input_box.player_attack_value = (
                                self.input_box.send_input()
                            )
                            if self.input_box.player_attack_value is not None:
                                self.input_box.player_attack_value = int(
                                    self.input_box.player_attack_value
                                )

                                print(self.input_box.player_attack_value)
                                self.engine.play(self.input_box.player_attack_value)
                                self.input_box.reset()

                        else:
                            self.engine.enemy.finish_phase()
                            self.render_background()

                        self.render_background()
                        self.render()

            if self.engine.enemy.stance == Stance.defend:
                if self.input_box.player_attack_value is not None:
                    self.input_box.color = "blue"
                self.input_box.render()

            self.render_floating_resources()

            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    # unittest.main()
    game = Game()

    tb = None

    try:
        game.run()
    except:
        tb = traceback.format_exc()
        print(tb)
        Game.quit_everything()
