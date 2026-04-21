import numpy as np 
import matplotlib
import pathlib
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import time
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import Game, Player, Board

# screen dimensions
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 1024
screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

# title dimensions
title_ht, title_wt = SCREEN_HEIGHT // 8, SCREEN_WIDTH
TITLE_COLOR = (85, 250, 148)
TITLE_FONT_COLOR = (255, 255, 255)

# board dimensions
ROWS = 7
COLS = 7
title_board_gap = 4*title_ht // 5
board_wt = (2 * SCREEN_WIDTH) // 3
board_ht  = SCREEN_HEIGHT - title_ht - title_board_gap
circle_radius = (3 * board_ht) // (7 * ROWS + 2)
border_width = circle_radius // 6
row_gap = circle_radius // 3
start_circle_gap = 2*row_gap
col_gap = (board_wt - 2 * circle_radius * COLS) // (1 + COLS)
hover_circle_offset = 2*(circle_radius // 3)

# colors used
BG_COLOR1 = (224, 123, 72)
BG_COLOR2 = (72, 110, 224)
BOARD_COLOR = (104, 118, 143)
BALL_COLOR1 = (255, 0, 0)
BALL_COLOR2 = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (152, 163, 181)

# Animation related
FALLING_TIME = 100
TRANSITION_TIME = 100

# Game over screen constants
over_title_wt = 2* (SCREEN_WIDTH // 3)
over_title_ht = title_ht
over_title_y = SCREEN_HEIGHT // 4
title_button_gap = over_title_ht
button_wt = SCREEN_WIDTH // 3    
button_ht = SCREEN_HEIGHT // 12
button_gap = SCREEN_HEIGHT // 24
BOARD_BORDER_RADIUS = 30

BGCOLOR = (245, 182, 66)
BUTTON_BG = (245, 66, 233)
LIGHT_BUTTON_BG = (237, 147, 227)
BUTTON_FONT_COLOR = WHITE

QUIT_BG = (242, 90, 63)
LIGHT_QUIT_BG = (242, 121, 99)

# make a function to check win condition in new game class
class Connect4(Game):
    def check_win(self):
        board_matrix = self.board.matrix
        board_t = np.transpose(board_matrix)
        ht = self.board.height
        wt = self.board.width
        matches = 4
        
        a = np.arange(matches)
        b = np.arange(wt - matches + 1)
        c = np.arange(ht - matches + 1)

        # rows
        d = a[None, :] + b[:, None]
        rowFours = board_t[:, d]
        
        # columns
        e = a[None, :] + c[:, None]
        colFours = board_matrix[:, e]

        # anti diagonal
        anti_diagFours = board_t[e[:, None, :], d[None, :, :]]

        # main diagonal
        f = np.flip(e)
        main_diagFours = board_t[f[:, None, :], d[None, :, :]]

        if np.any(np.all(rowFours == 1, axis=2)) or np.any(np.all(colFours == 1, axis=2)) or np.any(np.all(main_diagFours == 1, axis=2)) or np.any(np.all(anti_diagFours == 1, axis=2)):
            return 1
        elif np.any(np.all(rowFours == 2, axis=2)) or np.any(np.all(colFours == 2, axis=2)) or np.any(np.all(main_diagFours == 2, axis=2)) or np.any(np.all(anti_diagFours == 2, axis=2)):
            return 2
        elif not np.any(board_matrix == 0):
            return 0
        else:
            return -1

def make_title(screen, title_font, text_str, wt = SCREEN_WIDTH, ht = title_ht, center_y = title_ht // 2):
    bg_rect = pygame.Rect(0, 0, wt, ht)
    bg_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, TITLE_COLOR, bg_rect)
    text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    text_rect = text.get_rect(center = bg_rect.center)
    screen.blit(text, text_rect)

def make_board_circle(screen, x, y, ball_color, offset_y = 0):
    r = circle_radius
    gap_x = col_gap
    gap_y = row_gap
    center_x = (SCREEN_WIDTH - board_wt) // 2  + (x-1) * (2 * r + gap_x) + gap_x + r
    center_y = title_ht + title_board_gap + (y-1) * (2 * r + gap_y) + gap_y + r + start_circle_gap

    pygame.draw.circle(screen, ball_color, (center_x, center_y - offset_y), r)
    pygame.draw.circle(screen, BLACK, (center_x, center_y - offset_y), r, border_width)

def collide_col(i, mouse):
    top = title_ht + title_board_gap
    left = (SCREEN_WIDTH - board_wt) // 2 + i * (col_gap + 2 * circle_radius) + col_gap

    col_rect = pygame.Rect(left, top, 2 * circle_radius, board_ht)
    return col_rect.collidepoint(mouse)

def make_board_rect(screen):
    center_y = title_ht + title_board_gap + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, BOARD_COLOR, board_rect, 0, 0, BOARD_BORDER_RADIUS, BOARD_BORDER_RADIUS, 0, 0)
    pygame.draw.rect(screen, BLACK, board_rect, border_width, 0, BOARD_BORDER_RADIUS, BOARD_BORDER_RADIUS, 0, 0)

def make_hover_circles(screen, board_matrix, mouse, ball_color):
    for i in range(COLS):
        if collide_col(i, mouse):
            make_board_circle(screen, i+1, 1, ball_color, row_gap + start_circle_gap + circle_radius + hover_circle_offset)
            for j in range(ROWS):
                if board_matrix[i][j] == 0:
                    make_board_circle(screen, i+1, j+1, GREY)

def make_board_circles(screen, board_matrix):
    for i in range(0, COLS):
        for j in range(0, ROWS):
            code = board_matrix[i][j]
            if (code == 1):
                ball_color = BALL_COLOR1
            elif (code == 2):
                ball_color = BALL_COLOR2
            elif (code == 0):
                ball_color = WHITE
            make_board_circle(screen, i+1, j+1, ball_color)

def make_board(screen, board_matrix, mouse, ball_color):
    make_hover_circles(screen, board_matrix, mouse, ball_color)
    make_board_rect(screen)
    make_board_circles(screen, board_matrix)

def update_screen(screen, title_font, title_text, board_matrix, mouse, turn, x, y):
    init_col = BG_COLOR1 if turn == 1 else BG_COLOR2
    fin_col = BG_COLOR2 if turn == 1 else BG_COLOR1
    init_ball_col = BALL_COLOR1 if turn == 1 else BALL_COLOR2
    fin_ball_col = BALL_COLOR2 if turn == 1 else BALL_COLOR1
    
    screen.fill(init_col)
    make_title(screen, title_font, title_text)
    # init_y = row_gap + start_circle_gap + circle_radius + hover_circle_offset
    # fin_y = y
    # init_offset = fin_y - init_y
    # for i in range(FALLING_TIME):
    #     offset_i = init_offset - (init_offset*i)/FALLING_TIME
    #     make_board_circle(screen, x, y, init_ball_col, int(offset_i))
    #     make_board(screen, board_matrix, mouse, init_ball_col)

    for i in range(TRANSITION_TIME):
        col_r = init_col[0] + ((fin_col[0] - init_col[0]) / (TRANSITION_TIME)) * i
        col_g = init_col[1] + ((fin_col[1] - init_col[1]) / (TRANSITION_TIME)) * i
        col_b = init_col[2] + ((fin_col[2] - init_col[2]) / (TRANSITION_TIME)) * i
        bg_col = (int(col_r), int(col_g), int(col_b))

        ball_col_r = init_ball_col[0] + ((fin_ball_col[0] - init_ball_col[0]) / (TRANSITION_TIME)) * i
        ball_col_g = init_ball_col[1] + ((fin_ball_col[1] - init_ball_col[1]) / (TRANSITION_TIME)) * i
        ball_col_b = init_ball_col[2] + ((fin_ball_col[2] - init_ball_col[2]) / (TRANSITION_TIME)) * i
        ball_col = (int(ball_col_r), int(ball_col_g), int(ball_col_b))

        screen.fill(bg_col)
        make_title(screen, title_font, title_text)
        make_board(screen, board_matrix, mouse, ball_col)
        pygame.display.flip()
        

def run(user1, user2):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    game_board = Board(7, 7)

    game = Connect4(player1, player2, game_board, INIT_TURN)
    board_matrix = game_board.matrix

    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode(screen_size)
    title_font = pygame.font.SysFont("Calibri", 60)
    pygame.display.set_caption("Connect Four")

    pygame.event.clear()
    running = True

    while running:
        mouse = pygame.mouse.get_pos()
        turn = game.turn

        if (turn == 1):
            bg_col = BG_COLOR1
            code = 1
            ball_color = BALL_COLOR1
            title_text = f"{user1}'s turn"
        else:
            bg_col = BG_COLOR2
            code = 2
            ball_color = BALL_COLOR2
            title_text = f"{user2}'s turn"

        screen.fill(bg_col)

        make_title(screen, title_font, title_text)
        make_board(screen, board_matrix, mouse, ball_color)

        win = game.check_win()
        command = game.update_result(screen, title_font, game, win)
        if command != -1:
            return command

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 0
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                filled = False
                for i in range(COLS):
                    if collide_col(i, mouse):
                        for j in range(ROWS - 1, -1, -1):
                            if board_matrix[i][j] == 0:
                                make_board_circle(screen, i+1, j+1, ball_color)
                                update_screen(screen, title_font, title_text, board_matrix, mouse, turn, i+1, j+1)
                                board_matrix[i][j] = code
                                game.switch_turn()
                                filled = True
                                break
                    if (filled):
                        break
                    
        pygame.display.flip()
    pygame.quit()
    return command