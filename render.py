#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 19:30:01 2024

@author: lukasgartmair
"""

class Render:

    def render_background(self):
        self.window.blit(self.background, (0, 0))
    
    def render_end_background(self):
        self.background_bw = pygame.image.load("images/background_bw.png")
        self.window.blit(self.background_bw, (0, 0))
    
    def render_player_piles(self):
        if len(self.engine.enemy.deck) > 0:
            self.window.blit(cardBack, (width_references[4], height_references[0]))
    
        text = font.render(
            str(len(self.engine.enemy.hand)) + " cards", True, text_color
        )
        self.window.blit(text, (width_references[4], height_references[0]))
    
    def render_card(self, i, current_card, width_references, height_references):
        offset_factor = 1.35
    
        current_card.image = pygame.transform.scale(
            current_card.image,
            (int(card_width * card_scale), int(card_height * card_scale)),
        )
        self.window.blit(
            current_card.image, (width_references[i], height_references[0])
        )
    
        # NAME
        self.rect = pygame.draw.rect(
            self.window,
            (1, 1, 1),
            (width_references[i], height_references[0], card_width * 0.75, 25),
        )
    
        text = font_card_title.render(str(current_card.name), True, "white")
    
        self.window.blit(text, (width_references[i], height_references[0]))
    
        # POWER
        text = font.render(str(current_card.power), True, "yellow")
    
        self.window.blit(
            text,
            (
                width_references[i],
                height_references[0] + (card_height // offset_factor),
            ),
        )
    
        # DEFENSE
        text = font.render(str(current_card.defense), True, "black")
    
        self.window.blit(
            text,
            (
                width_references[i] + card_width // 2,
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
                width_references[i],
                height_references[0] - (card_height - card_height // offset_factor),
            ),
        )
    
        # COST
        text = font.render(str(current_card.cost), True, "red")
        self.window.blit(
            text,
            (
                width_references[i] + card_width // 2,
                height_references[0] - (card_height - card_height // offset_factor),
            ),
        )
    
    def render_enemy_play(self):
        for i, current_card in enumerate(self.engine.enemy.played_cards):
            self.render_card(i, current_card, width_references, height_references)
    
    def render_enemy_hand(self):
        for i, current_card in enumerate(self.engine.enemy.hand):
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
        self.render_enemy_hand()
    
        message = ""
        text = font.render(message, True, player_2_color)
        self.window.blit(text, (20, 50))
    
        self.input_box.render()
    
        self.render()
    
        pygame.display.update()
    
    def render(self):
        self.render_background()
    
        self.render_enemy_play()
    
        self.render_player_piles()
    
        self.render_turn_text()
    
        if self.engine.state == GameState.ended:
            self.render_win()
