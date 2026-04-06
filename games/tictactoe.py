import numpy as np 
import matplotlib
import pathlib
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # what is it doing
import pygame
import time
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import Game, Player, Board

pygame.init()

# initialize players and board
user1 = sys.argv[1]
user2 = sys.argv[2]

INIT_TURN = 1
player1 = Player(user1)
player2 = Player(user2)



# screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)


# title dimensions
title_ht, title_wt = SCREEN_HEIGHT // 7, SCREEN_WIDTH
TITLE_COLOR = (85, 250, 148)
TITLE_FONT_COLOR = (255, 255, 255)


# bottom clearence 
bottom_wt = SCREEN_WIDTH
bottom_ht = SCREEN_HEIGHT // 20 

# board dimensions
ROWS = 10
COLS = 10
title_board_gap = title_ht // 4
board_wt = (2 * SCREEN_WIDTH) // 3
board_ht  = SCREEN_HEIGHT - title_ht-bottom_ht
row_gap = board_ht // 10
col_gap = board_wt //10


# colors used
BG_COLOR1= (245, 88, 49)
BG_COLOR2 = (85, 85, 250)
BOARD_COLOR = (104, 118, 143)
BALL_COLOR1 = (255, 0, 0)
BALL_COLOR2 = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (152, 163, 181) 

# make a function to check win condition in new game class
class tictactoe(Game):
    def check_win(self):
        pass


game_board = Board(10,10)

game = Game(player1, player2, game_board, INIT_TURN)

screen = pygame.display.set_mode(screen_size)
title_font = pygame.font.SysFont("Calibri", 60)


def make_title(text_str):
    bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, title_ht)
    bg_rect.center = (SCREEN_WIDTH // 2, title_ht // 2)

    pygame.draw.rect(screen, TITLE_COLOR, bg_rect)
    text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    text_rect = text.get_rect(center = bg_rect.center)
    screen.blit(text, text_rect)

def make_board_box(x, y, value_code ):
    gap_x = col_gap
    gap_y = row_gap
    center_x = (SCREEN_WIDTH - board_wt) // 2  + (x-1) * (gap_x) + gap_x//2
    center_y = title_ht + title_board_gap + (y-1) * (gap_y) + gap_y//2

    if (value_code == 0):
        draw_rect(center_x-gap_x//2,center_y-gap_y//2)
    elif (value_code == 1):
        draw_cross(center_x-gap_x//2,center_y-gap_y//2,2*min(row_gap,col_gap)//3)
    elif (value_code == 2):
        draw_O(center_x-gap_x//2,center_y-gap_y//2,min(row_gap,col_gap)//3)
    else:
        ball_color = GREY

def draw_rect(x,y):
    pygame.draw.rect(screen,BLACK,(x,y,col_gap,row_gap),3)

def draw_cross(x,y,len):

    dia_len = pow(pow(col_gap,2)+pow(row_gap,2),0.5) 

    pygame.draw.rect(screen,BLACK,(x,y,col_gap,row_gap),3)
    pygame.draw.line(screen,WHITE,(x+ (dia_len-len)/2*(col_gap/dia_len) , y+ (dia_len-len)/2*(row_gap/dia_len)  ),(x+ col_gap - (dia_len-len)/2*(col_gap/dia_len) , y+row_gap- (dia_len-len)/2*(row_gap/dia_len)  ),3)
    pygame.draw.line(screen,WHITE,(x+ (dia_len-len)/2*(col_gap/dia_len) , y+row_gap- (dia_len-len)/2*(row_gap/dia_len)  ),(x+ col_gap - (dia_len-len)/2*(col_gap/dia_len) , y+ (dia_len-len)/2*(row_gap/dia_len)  ),3)



def draw_O(x,y,r):
    pygame.draw.rect(screen,BLACK,(x,y,col_gap,row_gap),3)
    pygame.draw.circle(screen,WHITE,(x+col_gap//2,y+row_gap//2),r,3)


def collide_box(x,y, mouse):
    top = title_ht + title_board_gap + (y-1)*row_gap 
    left = (SCREEN_WIDTH - board_wt) // 2 + (x-1) * (col_gap)

    col_rect = pygame.Rect(left, top, col_gap, row_gap)
    return col_rect.collidepoint(mouse)


def make_board(board_matrix, mouse):
    center_y = title_ht + title_board_gap + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

   
    pygame.draw.rect(screen, BOARD_COLOR, board_rect, 0, 10)
    for i in range(COLS):
        for j in range(ROWS):
            make_board_box(i+1, j+1, board_matrix[i][j])

    for i in range(COLS):
        for j in range(ROWS):
            if collide_box(i,j,mouse):
                if board_matrix[i][j] == 0:
                    make_board_box(i+1, j+1,0) 





pygame.display.set_caption("Tic-Tac-Toe")
running = True

while running:
    mouse = pygame.mouse.get_pos()
    turn = game.turn

    if game.check_win() == 1:
        make_title("f{user1} WON!")
    elif game.check_win() == 2:
        make_title("f{user2} WON!")
    elif game.check_win() == 0:
        make_title("DRAW!")

    if (turn == 1):
        bg_col = BG_COLOR1
        col_code = 1
        title_text = f"{user1}'s turn"
    else:
        bg_col = BG_COLOR2
        col_code = 2
        title_text = f"{user2}'s turn"
    
    screen.fill(bg_col)
    board_matrix = game_board.board

    make_title(title_text)
    make_board(board_matrix, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            filled = False
            for i in range(COLS):
                for j in range(ROWS - 1, -1, -1):
                    if collide_box(i+1,j+1,mouse):
                        if board_matrix[i][j] != 0 : break
                        make_board_box(i+1, j+1, col_code)
                        board_matrix[i][j] = col_code
                        game.switch_turn()
                        filled = True
                        break
            if (filled):
                break
                
    pygame.display.update()

pygame.quit()
sys.exit()  




print("I,am,Tic-Tac-Toe,2")

