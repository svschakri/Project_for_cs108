import pygame
import numpy as np 
import matplotlib
import pathlib
import sys
import os 
import time

# handle users
USER1 = sys.argv[1] 
USER2 = sys.argv[2]
TURN = 0

# dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

title_ht, title_wt = SCREEN_HEIGHT // 5, SCREEN_WIDTH
title_header_gap = SCREEN_HEIGHT // 20

header_ht = SCREEN_HEIGHT // 6
header_wt = 2 * (SCREEN_WIDTH // 3)
HEADER_BORDER_RADIUS = 50

BUTTON_LIST = ["Tic-Tac-Toe", "Othello", "Connect4"]
button_number = len(BUTTON_LIST)
button_wt = SCREEN_WIDTH // 3
button_ht = SCREEN_HEIGHT // 12
button_gap = SCREEN_HEIGHT // 24
button_stack_ht = (button_number-1)*button_gap + (button_number)*button_ht

header_box_gap = (SCREEN_HEIGHT - title_ht - title_header_gap - header_ht - button_stack_ht) // 3
BOX_BORDER_RADIUS = 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = (245, 182, 66)

TITLE_BG = (111, 245, 66)
TITLE_COLOR = WHITE

HEADER_BG = (239, 245, 66)
HEADER_COLOR = BLACK

BUTTON_BG = (245, 66, 233)
BUTTON_COLOR = WHITE

class Player:
    def __init__(self, user_name, turn):
        self.user_name = user_name
        self.turn = turn
    
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
    
# menu design
pygame.init()

TITLE_FONT = pygame.font.SysFont("comicsansms", 100)
HEADER_FONT = pygame.font.SysFont("timesnewroman", 60)
BUTTON_FONT = pygame.font.SysFont("calibri", 40)

screen = pygame.display.set_mode(screen_size)

def make_box(text, center_y, wt, ht, box_color, box_border_radius = 0):
    bg_rect = pygame.Rect(0, 0, wt, ht)
    bg_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, box_color, bg_rect, border_radius=box_border_radius)
    button_rect = text.get_rect(center = (SCREEN_WIDTH/2, center_y))
    screen.blit(text, button_rect)

def make_button(str, center_y):
    text = BUTTON_FONT.render(str, True, BUTTON_COLOR)
    make_box(text, center_y, button_wt, button_ht, BUTTON_BG, BOX_BORDER_RADIUS)

def start_menu():
    pygame.display.set_caption("GAME HUB")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        screen.fill(BGCOLOR)

        # title
        title_text = TITLE_FONT.render("GAME HUB", True, TITLE_COLOR)
        title_center_y = title_ht // 2
        make_box(title_text, title_center_y, title_wt, title_ht, TITLE_BG)

        # header
        header_text = HEADER_FONT.render(f"{USER1} V/S {USER2}", True, HEADER_COLOR)
        header_center_y = title_ht + title_header_gap + header_ht // 2
        make_box(header_text, header_center_y, header_wt, header_ht, HEADER_BG, HEADER_BORDER_RADIUS)

        # game buttons
        for i in range(button_number):
            game_name = BUTTON_LIST[i]
            buttons_top =  title_ht + title_header_gap + header_ht + header_box_gap
            center_i = buttons_top + i*(button_ht + button_gap) + button_ht // 2
            make_button(game_name, center_i)
        
        pygame.display.update()

start_menu()
