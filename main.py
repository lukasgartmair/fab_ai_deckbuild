#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
"""

import sys
import traceback
import pygame
from enemy import Stance
from engine import GameState, GameEngine
from input_box import InputBox

from settings import (
    player_1_color,
    player_2_color,
    bounds,
    width_reference_1,
    width_reference_2,
    width_reference_3,
    width_reference_4,
    width_reference_5,
    FPS,
    height_reference_1,
    height_reference_2,
)

pygame.font.init()

font_size = 65
font_style = pygame.font.match_font("z003")
font = pygame.font.Font(font_style, font_size)
font.set_bold(False)
text_color = (28, 0, 46)

card_height = 332
card_with = 238

card_scale = 0.75
cardBack = pygame.image.load("images/card_back.png")
cardBack = pygame.transform.scale(
    cardBack, (int(card_with * card_scale), int(card_height * card_scale))
)


game_engine = GameEngine()


class Game:
    def __init__(self):
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
        background_bw = pygame.image.load("images/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))

    def render_player_piles(self):
        self.window.blit(cardBack, (width_reference_5, height_reference_1))

        text = font.render(
            str(len(game_engine.enemy.hand)) + " cards", True, text_color
        )
        self.window.blit(text, (width_reference_5, height_reference_2))

    def render_player_hands(self):
        current_card = game_engine.enemy.hand[0]

        if current_card != None:
            current_card.image = pygame.transform.scale(
                current_card.image,
                (int(card_with * card_scale), int(card_height * card_scale)),
            )
            self.window.blit(
                current_card.image, (width_reference_1, height_reference_1)
            )

            current_card.image = pygame.transform.scale(
                current_card.image,
                (int(card_with * card_scale), int(card_height * card_scale)),
            )
            self.window.blit(
                current_card.image, (width_reference_2, height_reference_1)
            )

            current_card.image = pygame.transform.scale(
                current_card.image,
                (int(card_with * card_scale), int(card_height * card_scale)),
            )
            self.window.blit(
                current_card.image, (width_reference_3, height_reference_1)
            )

            current_card.image = pygame.transform.scale(
                current_card.image,
                (int(card_with * card_scale), int(card_height * card_scale)),
            )
            self.window.blit(
                current_card.image, (width_reference_4, height_reference_1)
            )

    def render_turn_text(self):
        if game_engine.state == GameState.playing:
            color = None

            if game_engine.enemy.stance == Stance.defend:
                color = player_2_color

            else:
                color = player_1_color

            text = font.render(
                "enemy " + game_engine.enemy.stance.name + "ing", True, color
            )

            self.window.blit(text, (20, 50))

    def render_win(self):
        self.render_end_background()

        message = "The " + game_engine.currentPlayer.name + " trancended!"
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
        self.render_player_hands()

        message = ""
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))

        pygame.display.update()

    def render(self):
        self.render_background()

        self.render_player_hands()

        self.render_player_piles()

        self.render_turn_text()

        if game_engine.state == GameState.ended:
            self.render_win()

    def intro(self):
        intro = False

        while intro == True:
            self.render_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    intro = False
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    intro = False
                    return

    def run(self):
        run = True

        clock = pygame.time.Clock()

        self.render_initial_game_state()
        self.input_box.render()

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
                    if event.key == pygame.K_SPACE:
                        game_engine.players_turn(event.key)
                        self.render()

                        if game_engine.state == GameState.playing:
                            game_engine.switch_stance()

                    if event.key != pygame.K_SPACE:
                        self.input_box.update(event=event)
                        self.render_background()
                        self.render()

                    if event.key == pygame.K_RETURN:
                        player_attack = self.input_box.send_input()
                        self.render_background()
                        self.render()
                        print(player_attack)

            self.input_box.render()

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
