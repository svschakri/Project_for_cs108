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
GREY = (152, 163, 181)

# Game over screen constants
over_title_wt = 2* (SCREEN_WIDTH // 3)
over_title_ht = title_ht
over_title_y = SCREEN_HEIGHT // 4
title_button_gap = over_title_ht
button_wt = SCREEN_WIDTH // 3    
button_ht = SCREEN_HEIGHT // 12
button_gap = SCREEN_HEIGHT // 24
BOX_BORDER_RADIUS = 10

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

        if np.any(np.all( rowFours == 1, axis=2)) or np.any(np.all(colFours == 1, axis=2)) or np.any(np.all(main_diagFours == 1, axis=2)) or np.any(np.all(anti_diagFours == 1, axis=2)):
            return 1
        elif np.any(np.all( rowFours == 2, axis=2)) or np.any(np.all(colFours == 2, axis=2)) or np.any(np.all(main_diagFours == 2, axis=2)) or np.any(np.all(anti_diagFours == 2, axis=2)):
            return 2
        elif not np.any(board_matrix == 0):
            return 0
        else:
            return -1
    
# initialize players and board
# user1 = sys.argv[1]
# user2 = sys.argv[2]

# make GUI

def make_title(screen, title_font, text_str, wt = SCREEN_WIDTH, ht = title_ht, center_y = title_ht // 2):
    bg_rect = pygame.Rect(0, 0, wt, ht)
    bg_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, TITLE_COLOR, bg_rect)
    text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    text_rect = text.get_rect(center = bg_rect.center)
    screen.blit(text, text_rect)

def make_board_circle(screen, x, y, color_code):
    r = circle_radius
    gap_x = col_gap
    gap_y = row_gap
    center_x = (SCREEN_WIDTH - board_wt) // 2  + (x-1) * (2 * r + gap_x) + gap_x + r
    center_y = title_ht + title_board_gap + (y-1) * (2 * r + gap_y) + gap_y + r

    if (color_code == 0):
        ball_color = WHITE
    elif (color_code == 1):
        ball_color = BALL_COLOR1
    elif (color_code == 2):
        ball_color = BALL_COLOR2
    else:
        ball_color = GREY

    pygame.draw.circle(screen, ball_color, (center_x, center_y), r)

def collide_col(i, mouse):
    top = title_ht + title_board_gap
    left = (SCREEN_WIDTH - board_wt) // 2 + i * (col_gap + 2 * circle_radius) + col_gap

    col_rect = pygame.Rect(left, top, 2 * circle_radius, board_ht)
    return col_rect.collidepoint(mouse)

def make_board(screen, board_matrix, mouse):
    center_y = title_ht + title_board_gap + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

    pygame.draw.rect(screen, BOARD_COLOR, board_rect, 0, 10, 10)
    for i in range(0, COLS):
        for j in range(0, ROWS):
            make_board_circle(screen, i+1, j+1, board_matrix[i][j])

    for i in range(COLS):
        if collide_col(i, mouse):
            for j in range(ROWS):
                if board_matrix[i][j] == 0:
                    make_board_circle(screen, i+1, j+1, 3)

def make_rect(center_y):   
        button_rect = pygame.Rect(0, 0, button_wt, button_ht)
        button_rect.center = (SCREEN_WIDTH // 2, center_y)
        return button_rect

def make_button(screen, button_font, button_rect, text_str, mouse):
        button_color = BUTTON_BG if text_str != "Quit" else QUIT_BG
        if button_rect.collidepoint(mouse):
            button_color = LIGHT_BUTTON_BG if text_str != "Quit" else LIGHT_QUIT_BG

        text = button_font.render(text_str, True, BUTTON_FONT_COLOR)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=BOX_BORDER_RADIUS)
        text_rect = text.get_rect(center = button_rect.center)
        screen.blit(text, text_rect)
        return button_rect

def draw_game_over(screen, title_font, msg):

    if not pygame.get_init():
        pygame.init()

    command = 0

    running = True
    button_font = pygame.font.SysFont("calibri", 40)
    while(running):
        mouse = pygame.mouse.get_pos()
        screen.fill(BGCOLOR)
        make_title(screen, title_font, msg, over_title_wt, over_title_ht, over_title_y)
        rect_dict = {}
        first_button_y = over_title_y + over_title_ht // 2 + title_button_gap + button_ht // 2
        rect_dict["Play Again"] = make_rect(first_button_y)
        rect_dict["Show Leaderboard"] = make_rect(first_button_y + button_ht + button_gap)
        quit_rect = make_rect(first_button_y + 2*(button_ht + button_gap))

        for name, rect in rect_dict.items():
            make_button(screen, button_font, rect, name, mouse)
        make_button(screen, button_font, quit_rect, "Quit", mouse)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    command = 0
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(mouse):
                    command = 0
                    running = False
                
                for name, rect in rect_dict.items():
                    if rect.collidepoint(mouse):
                        command = 1 if name == "Play Again" else 2
                        running = False
        pygame.display.flip()
    pygame.quit()
    return command
    

def check_result(screen, title_font, game):
    user1 = game.player1.user_name
    user2 = game.player2.user_name
    msgDict = {1 : f"{user1} WON!", 2 : f"{user2} WON!", 0 : "DRAW!"}
    win = game.check_win()

    if win == 1 or win == 2 or win == 0:
        make_title(screen, title_font, msgDict[win])
        pygame.display.flip()
        pygame.time.wait(1000)
        return draw_game_over(screen, title_font, msgDict[win])
    
    return -1

def run(user1, user2):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    game_board = Board(7, 6)

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
            col_code = 1
            title_text = f"{user1}'s turn"
        else:
            bg_col = BG_COLOR2
            col_code = 2
            title_text = f"{user2}'s turn"

        screen.fill(bg_col)

        make_title(screen, title_font, title_text)
        make_board(screen, board_matrix, mouse)

        command = check_result(screen, title_font, game)
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
                                make_board_circle(screen, i+1, j+1, col_code)
                                board_matrix[i][j] = col_code
                                game.switch_turn()
                                filled = True
                                break
                    if (filled):
                        break
                    
        pygame.display.flip()
    pygame.quit()
    return command