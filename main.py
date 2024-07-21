#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
'''
import pygame
from enemy import Stance
from engine import GameState, GameEngine
import sys
import traceback

FPS = 10

width = 1024
height = 700
bounds = (width, height)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption('Flesh and Blood AI enemy')

background = pygame.image.load('images/background.png')

player_1_color = (249, 243, 153)
player_2_color = (28, 0, 46)

right_edge = int(width*0.1)
middle_edge = int(width*0.3)
middle_edge_2 = int(width*0.55)
left_edge = int(width*0.75)

height_reference_1 = int(height/3)
height_reference_2 = int(height/4)

pygame.font.init()
font_size = 65
font_style = pygame.font.match_font("z003")
font = pygame.font.Font(font_style, font_size)
font.set_bold(False)
text_color = (28, 0, 46)

card_height = 332
card_with = 238

card_scale = 0.75
cardBack = pygame.image.load('images/card_back.png')
cardBack = pygame.transform.scale(
    cardBack, (int(card_with*card_scale), int(card_height*card_scale)))



game_engine = GameEngine()

def render_background():
    window.blit(background, (0, 0))


def render_end_background():

    background_bw = pygame.image.load('images/background_bw.png')
    window.blit(background_bw, (0, 0))


def render_player_hands():

    # # player 1
    # window.blit(cardBack, (right_edge, height_reference_1))

    # text = font.render(str(len(gameEngine.player1.hand)) +
    #                    ' cards', True, text_color)
    # window.blit(text, (right_edge, height_reference_2))

    # enemy
    window.blit(cardBack, (left_edge, height_reference_1))

    text = font.render(str(len(game_engine.enemy.hand)) +
                       ' cards', True, text_color)
    window.blit(text, (left_edge, height_reference_2))


def render_player_piles():

    # edge = middle_edge

    # current_card_player_1 = gameEngine.player1.pile.get_current_card()

    # if (current_card_player_1 != None):

    #     current_card_player_1.image = pygame.transform.scale(
    #         current_card_player_1.image, (int(card_with*card_scale), int(card_height*card_scale)))
    #     window.blit(current_card_player_1.image, (edge, height_reference_1))

    edge = middle_edge_2
    
    current_card_player_2 = game_engine.enemy.pile.get_current_card()
    
    if (current_card_player_2 != None):

        current_card_player_2.image = pygame.transform.scale(
            current_card_player_2.image, (int(card_with*card_scale), int(card_height*card_scale)))
        window.blit(current_card_player_2.image, (middle_edge, height_reference_1))

def render_turn_text():

    if game_engine.state == GameState.playing:
        color = None
        
        if game_engine.enemy.stance == Stance.defend:
            color = player_2_color
        
        else:

            color = player_1_color

        text = font.render("enemy " + game_engine.enemy.stance.name +
                           "ing", True, color)

        window.blit(text, (20, 50))

def render_input_box():
    pass


def render_win():

    render_end_background()

    message = 'The ' + \
        game_engine.currentPlayer.name + ' trancended!'
    text = font.render(message, True, player_2_color)
    window.blit(text, (20, 50))


def render_start_screen():

    background_start = pygame.image.load('images/background_start.png')
    window.blit(background_start, (0, 0))

    message = 'Enter the abyss...'
    text = font.render(message, True, (100, 0, 0))
    window.blit(text, (20, 50))
    pygame.display.update()


 
def render_initial_game_state(window):
    render_background()
    render_player_hands()

    message = ''
    text = font.render(message, True, player_2_color)
    window.blit(text, (20, 50))

    pygame.display.update()

def render_game(window, font):
    render_background()

    render_player_hands()

    render_player_piles()

    render_turn_text()

    if game_engine.state == GameState.ended:

        render_win()
        
class InputBox:

    def __init__(self, window):
        self.window = window
        self.active = False
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = pygame.font.Font(None, 32)
        
        self.box = pygame.Rect(100, 150, 140, 32)
        self.text = ''
        
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
        
        txt_surface = self.font.render(self.text, True, self.color)
        self.window.blit(txt_surface, (self.box.x+5, self.box.y+5))
        pygame.draw.rect(self.window, self.color, self.box, 2)
        
    def update(self, event):
                
        if event.type == pygame.KEYDOWN:                
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        
        
def intro():
    intro = False

    while intro == True:

        render_start_screen(window)
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


class Game:
    
    def __init__(self, window):
        self.window = window
        self.input_box = InputBox(self.window)

    @staticmethod
    def quit_everything(active_scene=None):
        if active_scene:
            active_scene.terminate()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    
    def run(self):
        run = True
    
        clock = pygame.time.Clock()
    
        render_initial_game_state(window)
        self.input_box.render()
    
        while run:
            key = None
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
                        render_game(window, font)
                        
                        if game_engine.state == GameState.playing:
                            game_engine.switch_stance()


                    if event.key != pygame.K_SPACE:
                        self.input_box.update(event=event)
                        

            self.input_box.render()                                
            
            pygame.display.flip()
            clock.tick(FPS)

                    

if __name__ == "__main__":
    # unittest.main()
    game = Game(window)

    tb = None

    try:
        game.run(

        )
    except:
        tb = traceback.format_exc()
        print(tb)
        Game.quit_everything()