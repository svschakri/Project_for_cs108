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
# FPS
MAX_FPS = 60
# screen dimensions
SCREEN_WIDTH = 1537
SCREEN_HEIGHT = 1023
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)


# board dimensions
ROWS = 10
COLS = 10
LEFT_BOARD = 453
TOP_BOARD = 236
board_wt = 630
board_ht  = 577
row_gap = board_ht // 10 + 1
col_gap = board_wt //10


#sprite_constanst 
scale1 = 2.2
scale2 = 1.5
sprite_ht = [375] * 4 + [375 * scale1, 375 * scale2, 375 * scale1, 375 * scale2]
sprite_wt = [193, 198, 315, 313, 160 * scale1, 315 * scale2, 140 * scale1, 315 * scale2]
sprite_pos = [(40, 510), (1204, 510), (55,510), (1204, 510), (0, 250), (-30, 450), (1150, 205), (1100, 450)]

# BACK
back_rect= pygame.Rect(432,894,265,70)

#RESET
reset_rect = pygame.Rect(830,894,265,70)

# sprites
sprite_still_blue = pygame.image.load("images/sprite_still_blue.png")
sprite_still_red = pygame.image.load("images/sprite_still_red.png")
sprite_active_blue = pygame.image.load("images/sprite_active_blue.png")
sprite_active_red = pygame.image.load("images/sprite_active_red.png")

# sprites after game_over
crying_blue = pygame.image.load("images/Lose_blue.png")
happy_blue = pygame.image.load("images/Win_blue.png")

crying_red = pygame.image.load("images/Lose_red.png")
happy_red = pygame.image.load("images/Win_red.png")

sprites = [sprite_still_blue, sprite_still_red, sprite_active_blue, sprite_active_red, crying_blue, happy_blue, crying_red, happy_red]

for i in range(len(sprites)):
    sprites[i] = pygame.transform.smoothscale(sprites[i], (sprite_wt[i], sprite_ht[i]))

sprite_rects = [pygame.Rect(*sprite_pos[i], sprite_wt[i], sprite_ht[i]) for i in range(len(sprites))]

# text rectangles
text_rect1 = pygame.Rect(60, 44, 264, 107)
text_rect2 = pygame.Rect(1230, 44, 260, 110)

# cross image
cross_img = pygame.image.load("images/cross_ttc.png")
cross_img = pygame.transform.scale(cross_img,(col_gap/3*2,row_gap/3*2))

# zero image
zero_img = pygame.image.load("images/circle_red.png")
zero_img = pygame.transform.scale(zero_img,(col_gap/3*2,row_gap/3*2))

# win cross image
win_cross_img = pygame.image.load("images/Win_cross.png")
win_cross_img = pygame.transform.scale(win_cross_img,(col_gap/3*2,row_gap/3*2))

# win zero image
win_zero_img = pygame.image.load("images/Win_circle.png")
win_zero_img = pygame.transform.scale(win_zero_img,(col_gap/3*2,row_gap/3*2))


def draw_line(screen, x,y,theta) :
    X_centre = LEFT_BOARD + col_gap*x + col_gap // 2 
    Y_centre =  TOP_BOARD + row_gap*y + row_gap // 2
    X_final = X_centre if theta == 90 else X_centre + 4*col_gap 
    if theta == -45 :
        X_final = X_centre - 4*col_gap 
    Y_final = Y_centre if theta == 0 else Y_centre + 4*row_gap 
    pygame.draw.line(screen,(0,0,0),(X_centre,Y_centre),(X_final,Y_final),6) 


# make a function to check win condition in new game class
class tictactoe(Game):
    def check_win(self, move):
            board_matrix = self.board.matrix
            x, y = move
            player = int(board_matrix[x][y])
            
            # Add padding in board_matrix
            padded_board = np.pad(board_matrix, pad_width=4)
            if player == 0:
                return [-1, None, None, None]
            pad_x = x + 4
            pad_y = y + 4
            temp = np.arange(5) 

            # Horizontal
            window_x = pad_x - temp
            windows = padded_board[window_x[:, None] + temp, pad_y]
            matches = np.all(windows == player, axis=1)
            if np.any(matches):
                idx = np.where(matches)[0][0]
                return [player, window_x[idx]-4, y, 0]

            # Vertical
            window_y = pad_y - temp
            windows = padded_board[pad_x, window_y[:, None] + temp]
            matches = np.all(windows == player, axis=1)
            if np.any(matches):
                idx = np.where(matches)[0][0]
                return [player, x, window_y[idx]-4, 90]

            # Main Diagonal
            window_x = pad_x - temp
            window_y = pad_y - temp
            windows = padded_board[window_x[:, None] + temp, window_y[:, None] + temp]
            matches = np.all(windows == player, axis=1)
            if np.any(matches):
                idx = np.where(matches)[0][0]
                return [player, window_x[idx]-4, window_y[idx]-4, 45]

            # Anti-Diagonal
            window_x = pad_x + temp
            window_y = pad_y - temp
            windows = padded_board[window_x[:, None] - temp, window_y[:, None] + temp]
            matches = np.all(windows == player, axis=1)
            if np.any(matches):
                idx = np.where(matches)[0][0]
                return [player, window_x[idx]-4, window_y[idx]-4, -45]

            # Check for draw
            if not np.any(board_matrix == 0):
                return [0, None, None, None]
                
            return [-1, None, None, None]

def make_board_box(screen, x, y, value_code):
    gap_x = col_gap
    gap_y = row_gap
    center_x = LEFT_BOARD  + (x-1) * (gap_x) + gap_x//2
    center_y = TOP_BOARD+ (y-1) * (gap_y) + gap_y//2

    if value_code == 1:
        draw_cross(screen, center_x-gap_x//3,center_y-gap_y//3)
    elif value_code == 2:
        draw_O(screen, center_x-gap_x//3,center_y-gap_y//3)
    elif value_code == 3:
        draw_win_cross(screen, center_x-gap_x//3,center_y-gap_y//3)
    elif value_code == 4:
        draw_win_zero(screen, center_x-gap_x//3,center_y-gap_y//3)

def draw_cross(screen, x,y):
    screen.blit(cross_img,(x, y)) 

def draw_win_cross(screen, x, y):
    screen.blit(win_cross_img, (x, y))

def draw_win_zero(screen, x, y):
    screen.blit(win_zero_img, (x, y))

def draw_O(screen, x, y):
    screen.blit(zero_img,(x,y)) #

def collide_box(x,y, mouse):
    top = TOP_BOARD + (y-1)*row_gap 
    left = LEFT_BOARD + (x-1) * (col_gap)

    col_rect = pygame.Rect(left, top, col_gap, row_gap)
    return col_rect.collidepoint(mouse)


def make_board(screen, board_matrix, mouse):
    center_y = TOP_BOARD + board_ht // 2
   #DCBE78
    for i in range(COLS):
        for j in range(ROWS):
            make_board_box(screen, i+1, j+1, board_matrix[i][j])

    for i in range(COLS):
        for j in range(ROWS):
            if collide_box(i,j,mouse):
                if board_matrix[i][j] == 0:
                    make_board_box(screen, i+1, j+1,0) 
def make_sprite(screen, status, turn):
    # status = 0 --> passive
    # status = 1 --> active
    screen.blit(sprites[status*2+turn-1], sprite_rects[status*2+turn-1])
    
def update_sprites(screen, turn):
    if turn == 1:
        make_sprite(screen, 1, 1)
        make_sprite(screen, 0, 2)
    elif turn == 2:
        make_sprite(screen, 0, 1)
        make_sprite(screen, 1, 2)

def write_name(screen,text,rect,font) :
        rendered_font = font.render(text, True, "BLACK")
        text_rect = rendered_font.get_rect()
        text_rect.center = rect.center
        screen.blit(rendered_font, text_rect)

def draw_win_col(screen, x, y, theta, win):
    value_code = win + 2
    if theta == 0:  # horizontal
        for i in range(5):
            make_board_box(screen, x + i + 1, y + 1, value_code)
    elif theta == 45:  # main diagonal
        for i in range(5):
            make_board_box(screen, x + i + 1, y + i + 1, value_code)
    elif theta == -45:  # anti diagonal
        for i in range(5):
            make_board_box(screen, x - i + 1, y + i + 1, value_code)
    elif theta == 90:  # vertical
        for i in range(5):
            make_board_box(screen, x + 1, y + i + 1, value_code)

def draw_over(screen, win):
    # if win == 1 --> draw happy_blue (sprites idx = 6) and crying_red (sprites idx = 5)
    if win == 1:
        screen.blit(sprites[5], sprite_rects[5])
        screen.blit(sprites[6], sprite_rects[6])
    # if win == 2 --> draw crying_blue (sprites idx = 4) and happy_red (sprites idx = 7)
    else:
        screen.blit(sprites[4], sprite_rects[4])
        screen.blit(sprites[7], sprite_rects[7])

def run(user1, user2, screen, flag):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    pygame.display.set_caption("Tic-Tac-Toe")
    board_img = pygame.image.load("images/Tic-Tac-Toe_final.png")
    board_img = pygame.transform.scale(board_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    game_board = Board(10,10)

    game = tictactoe("Tic-Tac-Toe", player1, player2, game_board, INIT_TURN)
    if flag:
        return game.draw_game_over(screen)
    board_matrix = game_board.matrix

    if not pygame.get_init():
        pygame.init()
    pygame.display.set_caption("Tic-Tac-Toe")
    font = pygame.font.Font("./fonts/Cinzel,EB_Garamond/EB_Garamond/EBGaramond-VariableFont_wght.ttf", 48)

    pygame.event.clear()
    running = True

    while running:
        clock = pygame.time.Clock()
        clock.tick(MAX_FPS)

        # clock.tick(120)
        mouse = pygame.mouse.get_pos()
        turn = 2 - game.turn

        command = -1

        screen.blit(board_img, (0, 0))
        update_sprites(screen, turn)
        board_matrix = game_board.matrix
        make_board(screen, board_matrix, mouse)
        write_name(screen,user1.capitalize(),text_rect1,font)
        write_name(screen,user2.capitalize(),text_rect2,font)

        for rect in back_rect, reset_rect:
            if rect.collidepoint(mouse):
                hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                hover_surface.fill((0, 0, 0, 50))
                screen.blit(hover_surface, rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 3
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos) :
                    game.back_game()
                    board_matrix=game.board.matrix
                    
                if reset_rect.collidepoint(event.pos) :
                    game.reset_game()
                    board_matrix=game.board.matrix
                    
                filled = False
                for i in range(COLS):
                    for j in range(ROWS - 1, -1, -1):
                        if collide_box(i+1,j+1,mouse):
                            if board_matrix[i][j] != 0 :
                                break
                            # board_matrix[i][j] = turn
                            game.make_move((i, j), turn)
                            make_board_box(screen, i+1, j+1, turn)
                            update_sprites(screen, turn)

                            win_situation, x, y, theta = game.check_win((i, j))
                            if (win_situation == 1 or win_situation == 2):
                                screen.blit(board_img, (0, 0))
                                make_board(screen, board_matrix, mouse)
                                write_name(screen,user1.capitalize(),text_rect1,font)
                                write_name(screen,user2.capitalize(),text_rect2,font)
                                draw_win_col(screen, x, y, theta, win_situation)
                                draw_line(screen, x, y, theta)
                                draw_over(screen, win_situation)
                            command = game.update_result(screen, game, win_situation)
                            game.switch_turn()
                            filled = True
                            break
                if (filled):
                    break
                    
        pygame.display.flip()
        if command != -1:
            return command

    return command
