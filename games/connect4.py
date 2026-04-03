import pygame
import numpy as np 
import matplotlib
import pathlib
import sys
import os 
import time
import subprocess

sys.path.append(os.path.abspath(".."))
from game import Game, Player, Board

# screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

# title dimensions
title_ht, title_wt = SCREEN_HEIGHT // 7, SCREEN_WIDTH
TITLE_COLOR = (85, 250, 148)
TITLE_FONT_COLOR = (255, 255, 255)

# board dimensions
ROWS = 6
COLS = 7
title_board_gap = title_ht // 4
board_wt = (2 * SCREEN_WIDTH) // 3
board_ht  = SCREEN_HEIGHT - title_ht
circle_radius = (3 * board_ht) // (7 * ROWS + 2)
row_gap = circle_radius // 3
col_gap = (board_wt - 2 * circle_radius * COLS) // (1 + COLS)

# colors used
BG_COLOR1= (245, 88, 49)
BG_COLOR2 = (85, 85, 250)
BOARD_COLOR = (104, 118, 143)
BALL_COLOR1 = (255, 0, 0)
BALL_COLOR2 = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# make a function to check win condition in new game class
class Connect4(Game):
    def check_win(self):
        pass
    
# initialize players and board
user1 = sys.argv[1]
user2 = sys.argv[2]

turn = 1
player1 = Player(user1, 1)
player2 = Player(user2, 0)

game_board = Board(7, 6)

# make GUI
pygame.init()
screen = pygame.display.set_mode(screen_size)
title_font = pygame.font.SysFont("Calibri", 60)

def make_title(turn):
    bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, title_ht)
    bg_rect.center = (SCREEN_WIDTH // 2, title_ht // 2)

    if turn == 1:
        text_str = f"{user1}'s turn"
    else:
        text_str = f"{user2}'s turn"

    pygame.draw.rect(screen, TITLE_COLOR, bg_rect)
    text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    text_rect = text.get_rect(center = bg_rect.center)
    screen.blit(text, text_rect)

def make_board_circle(x, y, color_code):
    r = circle_radius
    gap_x = col_gap
    gap_y = row_gap
    center_x = (SCREEN_WIDTH - board_wt) // 2  + (x-1) * (2 * r + gap_x) + gap_x + r
    center_y = title_ht + title_board_gap + (y-1) * (2 * r + gap_y) + gap_y + r

    if (color_code == 0):
        ball_color = WHITE
    elif (color_code == 1):
        ball_color = BALL_COLOR1
    else:
        ball_color = BALL_COLOR2

    pygame.draw.circle(screen, ball_color, (center_x, center_y), r)

def make_board(board_matrix):
    center_y = title_ht + title_board_gap + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, BOARD_COLOR, board_rect, 0, 10, 10)
    for i in range(0, COLS):
        for j in range(0, ROWS):
            make_board_circle(i+1, j+1, board_matrix[i][j])


def fill_board():
    # takes numpy array as input and fills board
    pass

pygame.display.set_caption("Connect Four")
running = True

while running:
    if (turn == 1):
        bg_col = BG_COLOR1
    else:
        bg_col = BG_COLOR2
    
    screen.fill(bg_col)
    make_title(turn)
    make_board(game_board.board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    pygame.display.update()
pygame.quit()
sys.exit()