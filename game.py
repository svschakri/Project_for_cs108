import pygame
import numpy as np 
import matplotlib
import pathlib
import sys
import os 
import time

USER1 = sys.argv[1] 
USER2 = sys.argv[2]
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
TURN = 0
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
BUTTON_SIZE = (SCREEN_WIDTH/3, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = (39, 135, 245)

class Player:
    def __init__(self, user_name, turn):
        self.user_name = user_name
        self.turn = TURN
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width , height))

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def switch_turn(self):
        self.player1.turn = 1 - self.player1.turn
        self.player2.turn = 1 - self.player2.turn

    def check_win(self):
        """ This would be used to check win condition """
        return
    
# handle gameplay
pygame.init()

HEADER_FONT = pygame.font.SysFont("Papyrus", 60)
BUTTON_FONT = pygame.font.SysFont("Calibri", 25)

player1 = Player(USER1, 1)
player2 = Player(USER2, 0)

WINDOW = pygame.display.set_mode(SIZE)

def make_button(text, center_x, center_y):
    pass

def start_menu():
    pygame.display.set_caption("GAME HUB")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        WINDOW.fill(BGCOLOR)

        HEADER_TEXT = HEADER_FONT.render(f"{USER1} V/S {USER2}", True, WHITE)
        WINDOW.blit(HEADER_TEXT, HEADER_TEXT.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/5)))

        TICTAC_BG_RECT = pygame.Rect(0, 0, SCREEN_WIDTH/4, 50)
        TICTAC_BG_RECT.center = (SCREEN_WIDTH/2, 0.4 * SCREEN_HEIGHT)

        pygame.draw.rect(WINDOW, WHITE, TICTAC_BG_RECT)
        TICTAC_BUTTON_TEXT = BUTTON_FONT.render("TIC-TAC-TOE", True, BLACK)
        TICTAC_RECT = TICTAC_BUTTON_TEXT.get_rect(center = (SCREEN_WIDTH/2, 0.4 * SCREEN_HEIGHT))
        WINDOW.blit(TICTAC_BUTTON_TEXT, TICTAC_RECT)
        pygame.display.update()

start_menu()

