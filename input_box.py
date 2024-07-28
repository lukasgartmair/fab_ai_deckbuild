#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:48:35 2024

@author: lukasgartmair
"""

import pygame

pygame.font.init()
font_size = 25
font_style = pygame.font.match_font("z003")
font2 = pygame.font.Font(font_style, font_size)


class InputBox:
    def __init__(self, window):
        self.window = window
        self.active = False
        self.color_inactive = pygame.Color("red")
        self.color_active = pygame.Color("green")
        self.color = self.color_inactive
        self.font = pygame.font.Font(None, 32)

        self.box = pygame.Rect(100, 150, 140, 32)
        self.text = ""

    def send_input(self):
        text_temp = self.text
        self.text = ""
        self.render()
        self.active = False
        self.color = self.color_inactive
        if text_temp.isnumeric():
            return text_temp
        
        self.player_attack_value = None
        
    def reset(self):
        self.player_attack_value = None
        self.color = "red"
        self.text = ""

    def check_activation(self, event):
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.color_active if self.active else self.color_inactive

    def render(self):
        message = "Enter your attack value here"
        text = font2.render(message, True, (0, 0, 0))
        self.window.blit(text, (self.box.x, self.box.y - 30))
        txt_surface = self.font.render(self.text, True, self.color)
        self.window.blit(txt_surface, (self.box.x + 5, self.box.y + 5))
        pygame.draw.rect(self.window, self.color, self.box, 2)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.key in [
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ]:
                        self.text += event.unicode
