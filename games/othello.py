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

# screen dimensions
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 1024
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)


# title dimensions
title_ht, title_wt = SCREEN_HEIGHT // 7, SCREEN_WIDTH
TITLE_COLOR = (85, 250, 148)
TITLE_FONT_COLOR = (255, 255, 255)


# bottom clearence 
bottom_wt = SCREEN_WIDTH
bottom_ht = SCREEN_HEIGHT // 20 


# board dimensions
ROWS = 8
COLS = 8
title_board_gap = title_ht // 4
board_wt = (2 * SCREEN_WIDTH) // 3
board_ht  = SCREEN_HEIGHT - title_ht-bottom_ht
row_gap = board_ht // 8
col_gap = board_wt // 8


# colors used
BG_COLOR1= (245, 255, 230)
BG_COLOR2 = (5, 5, 5)
BOARD_COLOR = (0, 255, 0)
BALL_COLOR1 = (255, 255, 255)
BALL_COLOR2 = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (152, 163, 181) 
GREEN = (0,255,0)



# make a function to check win condition in new game class
class othello(Game):
   def check_win(self):
    board_matrix = self.board.matrix

    a = np.sum(board_matrix == 1.5)
    b = np.sum(board_matrix == 2.5)

    if a == 0 and b == 0:
        p1 = np.sum(board_matrix == 1)
        p2 = np.sum(board_matrix == 2)
        if p1 > p2:
            return 1
        elif p2 > p1:
            return 2
        else:
            return 0
    return -1

def update_possible_moves(req_color,board_matrix):

    for i in range(8):
        for j in range(8):
            if board_matrix[i,j] != 0 :
                continue
            #VERTICAL - DOWN 
            if j<7 :
                if board_matrix[i,j+1] == req_color :
                    a,b = i,j+1
                    while b < 8 and board_matrix[a,b] == board_matrix[i,j+1] :
                        b+=1
                    if b == j+1 : pass
                    elif  b > 7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i,j+1]
                        continue
            # VERTICAL - UP
            if j>0 :
                if board_matrix[i,j-1] == req_color :
                    a,b = i,j-1
                    while b > -1 and board_matrix[a,b] == board_matrix[i,j-1] :
                        b-=1
                    if b == j-1 : pass
                    elif  b < 0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i,j-1]
                        continue
            #HORIZONTAL - RIGHT
            if i<7 :
                if board_matrix[i+1,j] == req_color :
                    a,b = i+1,j
                    while a < 8 and board_matrix[a,b] == board_matrix[i+1,j] :
                        a+=1
                    if a == i+1 : pass
                    elif  a > 7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i+1,j]
                        continue
            #HORIZONTAL - LEFT
            if i >0 :
                if board_matrix[i-1,j] == req_color :
                    a,b = i-1,j
                    while a > -1 and board_matrix[a,b] == board_matrix[i-1,j] :
                        a-=1
                    if a == i-1 : pass
                    elif  a < 0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i-1,j]
                        continue
                
            # TOP-LEFT-DIAG
            if i > 0 and j>0 : 
                if board_matrix[i-1,j-1] == req_color :
                    a,b = i-1,j-1
                    while a > -1 and b>-1 and board_matrix[a,b] == board_matrix[i-1,j-1] :
                        a-=1
                        b-=1
                    if b == j-1 : pass
                    elif  b<0 or a<0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i-1,j-1]
                        continue
            # BOTTOM-RIGHT-DIAG 
            if i < 7 and j < 7 : 
                if board_matrix[i+1,j+1] == req_color :
                    a,b = i+1,j+1
                    while a <8 and b<8 and board_matrix[a,b] == board_matrix[i+1,j+1] :
                        a+=1
                        b+=1
                    if b == j+1 : pass
                    elif  b>7 or a>7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i+1,j+1]
                        continue
            # TOP-RIGHT-DIAG 
            if i < 7 and j>0 : 
                if board_matrix[i+1,j-1] == req_color :
                    a,b = i+1,j-1
                    while a <8 and b>-1 and board_matrix[a,b] == board_matrix[i+1,j-1] :
                        a+=1
                        b-=1
                    if b == j-1 : pass
                    elif  b<0 or a>7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i+1,j-1]
                        continue
            # BOTTOM-LEFT-DIAG 
            if i > 0 and j < 7 : 
                if board_matrix[i-1,j+1] == req_color :
                    a,b = i-1,j+1
                    while a > -1 and b<8 and board_matrix[a,b] == board_matrix[i-1,j+1] :
                        a-=1
                        b+=1
                    if b == j+1 : pass
                    elif  b>7 or a<0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = 3.5 - board_matrix[i-1,j+1]
                        continue


def update_values(i,j,board_matrix):
    color_code = board_matrix[i,j]
    board_matrix[board_matrix == 1.5] = 0
    board_matrix[board_matrix == 2.5] = 0
    #VERTICAL - DOWN 
    if j<7 :
        if board_matrix[i,j+1] == 3-color_code :
            a,b = i,j+1
            while b < 8 and board_matrix[a,b] == board_matrix[i,j+1] :
                b+=1
            if b == j+1 : pass
            elif  b > 7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i,j:b]=color_code
    #VERTICAL - UP 
    if j>0 :
        if board_matrix[i,j-1] == 3-color_code :
            a,b = i,j-1
            while b >-1 and board_matrix[a,b] == board_matrix[i,j-1] :
                b-=1
            if b == j-1 : pass
            elif  b <0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i,b:j]=color_code
    #HORIZONTAL - RIGHT
    if i<7 :
        if board_matrix[i+1,j] == 3-color_code :
            a,b = i+1,j
            while a < 8 and board_matrix[a,b] == board_matrix[i+1,j] :
                a+=1
            if a == i-1 : pass
            elif  a > 7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i:a,j] = 3 - board_matrix[i+1,j]
                pass
    #HORIZONTAL - LEFT
    if i >0 :
        if board_matrix[i-1,j] == 3-color_code :
            a,b = i-1,j
            while a > -1 and board_matrix[a,b] == board_matrix[i-1,j] :
                a-=1
            if a == i-1 : pass
            elif  a < 0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[a:i,j] = 3 - board_matrix[i-1,j]
                pass
        
    # TOP-LEFT-DIAG
    if i > 0 and j>0 : 
        if board_matrix[i-1,j-1] == 3-color_code :
            a,b = i-1,j-1
            while a > -1 and b>-1 and board_matrix[a,b] == board_matrix[i-1,j-1] :
                a-=1
                b-=1
            if b == j-1 : pass
            elif  b<0 or a<0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                np.fill_diagonal(board_matrix[a:i, b:j], 3 - board_matrix[i-1, j-1])
                pass
    # BOTTOM-RIGHT-DIAG 
    if i < 7 and j < 7 : 
        if board_matrix[i+1,j+1] == 3-color_code :
            a,b = i+1,j+1
            while a <8 and b<8 and board_matrix[a,b] == board_matrix[i+1,j+1] :
                a+=1
                b+=1
            if b == j+1 : pass
            elif  b>7 or a>7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                np.fill_diagonal(board_matrix[i:a, j:b], 3 - board_matrix[i+1, j+1])
                pass
    # TOP-RIGHT-DIAG 
    if i < 7 and j>0 : 
        if board_matrix[i+1,j-1] == 3-color_code :
            a,b = i+1,j-1
            while a <8 and b>-1 and board_matrix[a,b] == board_matrix[i+1,j-1] :
                a+=1
                b-=1
            if b == j-1 : pass
            elif  b<0 or a>7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                for k in range (b,j) :
                    board_matrix[i+abs(j-k),k] = 3 - board_matrix[i+1,j-1]
                pass
    # BOTTOM-LEFT-DIAG 
    if i > 0 and j < 7 : 
        if board_matrix[i-1,j+1] == 3-color_code :
            a,b = i-1,j+1
            while a > -1 and b<8 and board_matrix[a,b] == board_matrix[i-1,j+1] :
                a-=1
                b+=1
            if b == j+1 : pass
            elif  b>7 or a<0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                for k in range (a,i) :
                    board_matrix[k,j+abs(i-k)] = 3 - board_matrix[i-1,j+1]
                pass

def make_title(screen, title_font,text_str):
    bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, title_ht)
    bg_rect.center = (SCREEN_WIDTH // 2, title_ht // 2)

    pygame.draw.rect(screen, TITLE_COLOR, bg_rect)
    text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    text_rect = text.get_rect(center = bg_rect.center)
    screen.blit(text, text_rect)

def make_board_circle(screen,x, y, color_code):
    r = min(col_gap,row_gap)//3 
    gap_x = col_gap
    gap_y = row_gap
    center_x = (SCREEN_WIDTH - board_wt) // 2  + (x-1) * ( gap_x ) +  gap_x //2 
    center_y = title_ht + title_board_gap + (y-1) * ( gap_y ) + gap_y //2

    if (color_code == 0):
        ball_color = GREEN
    elif (color_code == 1):
        ball_color = BALL_COLOR1
    elif (color_code == 2):
        ball_color = BALL_COLOR2
    elif (color_code == 1.5):
        ball_color = BALL_COLOR1
    elif (color_code == 2.5):
        ball_color = BALL_COLOR2
    if color_code in (1.5,2.5) :
        pygame.draw.circle(screen, ball_color, (center_x , center_y), r,3)
    else :
        pygame.draw.circle(screen, ball_color, (center_x , center_y), r)
    pygame.draw.rect(screen,BLACK,(center_x-col_gap//2,center_y-row_gap//2,col_gap,row_gap),3)
    

def collide_box(x,y, mouse):
    top = title_ht + title_board_gap + (y-1)*row_gap 
    left = (SCREEN_WIDTH - board_wt) // 2 + (x-1) * (col_gap)

    col_rect = pygame.Rect(left, top, col_gap, row_gap)
    return col_rect.collidepoint(mouse)


def make_board(screen,board_matrix, mouse):
    center_y = title_ht + title_board_gap + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

   
    pygame.draw.rect(screen, BOARD_COLOR, board_rect, 0, 10)


    for i in range(COLS):
        for j in range(ROWS):
            make_board_circle(screen,i+1, j+1, board_matrix[i][j])

    for i in range(COLS):
        for j in range(ROWS):
            if collide_box(i,j,mouse):
                if board_matrix[i][j] == 0:
                    make_board_circle(screen,i+1, j+1,0)

def run(user1,user2):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)
    if not pygame.get_init():
        pygame.init()
    pygame.display.set_caption("othello")
    running = True
    board_img = pygame.image.load("images/othello_board.png")
    board_img = pygame.transform.scale(board_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    game_board = Board(8,8)

    game = othello(player1, player2, game_board, INIT_TURN)

    screen = pygame.display.set_mode(screen_size)
    title_font = pygame.font.SysFont("Calibri", 60)

    game_board.matrix[3][3]=1
    game_board.matrix[4][4]=1
    game_board.matrix[4][3]=2
    game_board.matrix[3][4]=2

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
        screen.blit(board_img)
        board_matrix = game_board.matrix
        update_possible_moves(3-col_code,board_matrix)
        make_title(screen,title_font,title_text)
        make_board(screen, board_matrix, mouse)
        win_status = game.check_win()

        if win_status == 1:
            make_title(screen,title_font,f"{user1} WON!")
            pygame.display.update()
    
        elif win_status == 2:
            make_title(screen,title_font,f"{user2} WON!")
            pygame.display.update()

        elif win_status == 0:
            make_title(screen,title_font,"DRAW!")
            pygame.display.update()

        command = game.update_result(screen, title_font, game, win_status)
        if command != -1:
            return command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                filled = False
                for i in range(COLS):
                    for j in range(ROWS - 1, -1, -1):
                        if collide_box(i+1,j+1,mouse):
                            if board_matrix[i][j] != col_code+0.5  : break
                            make_board_circle(screen,i+1, j+1, col_code)
                            board_matrix[i][j] = col_code
                            update_values(i,j,board_matrix)
                            # update_possible_moves(3-col_code)
                            game.switch_turn()
                            filled = True
                            break
                if (filled):
                    break
                    
        pygame.display.update()

   
    pygame.quit()
    return command




