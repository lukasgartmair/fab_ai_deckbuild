#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Nov 13 10:29:21 2023

@author: lukasgartmair
'''
import pygame
from engine import GameEngine, GameState
import sys

width = 1024
height = 700
bounds = (width, height)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption('Flesh and Blood')

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


def initialize_game_engine():
    return GameEngine()


def render_background():
    window.blit(background, (0, 0))


def render_end_background():

    background_bw = pygame.image.load('images/background_bw.png')
    window.blit(background_bw, (0, 0))

    # if gameEngine.currentPlayer == gameEngine.player1:
    #     end_background = pygame.image.load('images/player_1_win.png')
    # elif gameEngine.currentPlayer == gameEngine.player2:
    #     end_background = pygame.image.load('images/player_2_win.png')

    # window.blit(end_background, (0, 0))


def render_player_hands():

    # player 1
    window.blit(cardBack, (right_edge, height_reference_1))

    text = font.render(str(len(gameEngine.player1.hand)) +
                       ' cards', True, text_color)
    window.blit(text, (right_edge, height_reference_2))

    # player2
    window.blit(cardBack, (left_edge, height_reference_1))

    text = font.render(str(len(gameEngine.player2.hand)) +
                       ' cards', True, text_color)
    window.blit(text, (left_edge, height_reference_2))


def render_player_piles():

    edge = middle_edge

    current_card_player_1 = gameEngine.player1.pile.get_current_card()

    if (current_card_player_1 != None):

        current_card_player_1.image = pygame.transform.scale(
            current_card_player_1.image, (int(card_with*card_scale), int(card_height*card_scale)))
        window.blit(current_card_player_1.image, (edge, height_reference_1))

    edge = middle_edge_2
    
    current_card_player_2 = gameEngine.player2.pile.get_current_card()
    
    if (current_card_player_2 != None):

        current_card_player_2.image = pygame.transform.scale(
            current_card_player_2.image, (int(card_with*card_scale), int(card_height*card_scale)))
        window.blit(current_card_player_2.image, (edge, height_reference_1))

def render_turn_text():

    if gameEngine.state == GameState.PLAYING:
        color = None
        if gameEngine.currentPlayer == gameEngine.player1:
            color = player_1_color
        elif gameEngine.currentPlayer == gameEngine.player2:
            color = player_2_color

        text = font.render(gameEngine.currentPlayer.name +
                           "'s turn", True, color)

        window.blit(text, (20, 50))


def render_win():

    render_end_background()

    message = 'The ' + \
        gameEngine.currentPlayer.name + ' trancended!'
    text = font.render(message, True, player_2_color)
    window.blit(text, (20, 50))


def render_start_screen():

    background_start = pygame.image.load('images/background_start.png')
    window.blit(background_start, (0, 0))

    message = 'Enter the abyss...'
    text = font.render(message, True, (100, 0, 0))
    window.blit(text, (20, 50))
    pygame.display.update()


gameEngine = initialize_game_engine()

 
def render_initial_game_state():
    render_background()
    render_player_hands()

    message = 'Play?!'
    text = font.render(message, True, player_2_color)
    window.blit(text, (20, 50))

    pygame.display.update()

def renderGame(window, font):
    render_background()

    render_player_hands()

    render_player_piles()

    render_turn_text()

    if gameEngine.state == GameState.ENDED:

        render_win()

def intro():
    intro = True

    while intro == True:

        render_start_screen()
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


def main():
    run = True

    render_initial_game_state()

    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                key = event.key

                gameEngine.players_turn(key)
                renderGame(window, font)
                pygame.display.update()
                
                if gameEngine.state == GameState.PLAYING:
                    gameEngine.switchPlayer()
                



intro()
main()
