#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:48:35 2024

@author: lukasgartmair
"""

import pygame
from attack import Attack

pygame.font.init()
font_size = 25
font_style = pygame.font.match_font("z003")
font2 = pygame.font.Font(font_style, font_size)


class InputBox:
    def __init__(self, window, y=150, box_type="physical"):
        self.window = window
        self.active = False
        self.box_type = box_type
        self.color_inactive = pygame.Color("red")
        self.color_active = pygame.Color("green")
        self.color = self.color_inactive
        self.font = pygame.font.Font(None, 32)
        self.x = 100
        self.y = y
        self.width = 140
        self.height = 32
        self.box = pygame.Rect(self.x, y, self.width, self.height)
        self.text = ""

    def send_input(self):
        text_temp = self.text
        self.text = ""
        self.render()
        self.active = False
        self.color = self.color_inactive
        if text_temp.isnumeric():
            return int(text_temp)

    def has_text(self):
        return self.text != ""

    def reset(self):
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
        message = "{} DAMAGE value".format(self.box_type.upper())
        text = font2.render(message, True, (0, 0, 0))
        self.window.blit(text, (self.box.x, self.box.y - 30))
        txt_surface = self.font.render(self.text, True, "blue")
        self.window.blit(txt_surface, (self.box.x + 5, self.box.y + 5))
        pygame.draw.rect(self.window, self.color, self.box, 2)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    print("here")
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
