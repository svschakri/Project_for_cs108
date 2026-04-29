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
# user1 = sys.argv[1]
# user2 = sys.argv[2]




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
row_gap = board_ht // 10
col_gap = board_wt //10


#sprite_constanst 
sprite_ht = [375 ,375 ,375 ,375 ]
sprite_wt = [300,300,250,250]
sprite_pos = [(40,),(55,500), (1204, 458), (1204, 458)]


# sprites
sprite_still_blue = pygame.image.load("images/sprite_still_blue.png")
sprite_still_red = pygame.image.load("images/sprite_still_red.png")
sprite_active_blue = pygame.image.load("images/sprite_active_blue.png")
sprite_active_red = pygame.image.load("images/sprite_active_red.png")
sprites = [sprite_still_blue,sprite_still_red, sprite_active_blue,sprite_active_red]

for i in range(len(sprites)):
    sprites[i] = pygame.transform.smoothscale(sprites[i], (sprite_ht[i], sprite_wt[i]))

sprite_rects = [pygame.Rect(*sprite_pos[i], sprite_wt[i], sprite_ht[i]) for i in range(4)]


def draw_line(screen, x,y,theta) :
    X_centre = LEFT_BOARD + col_gap*x + col_gap // 2 
    Y_centre =  TOP_BOARD+ row_gap*y + row_gap // 2
    X_final = X_centre if theta == 90 else X_centre + 4*col_gap 
    if theta == -45 :
        X_final =X_centre - 4*col_gap 
    Y_final = Y_centre if theta == 0 else Y_centre + 4*row_gap 
    pygame.draw.line(screen,(0,0,0),(X_centre,Y_centre),(X_final,Y_final),3) 


# make a function to check win condition in new game class
class tictactoe(Game):
    def check_win(self, screen):
        board_matrix = self.board.matrix
        board_t = np.transpose(board_matrix)
        ht = self.board.height
        wt = self.board.width
        matches = 5

        a = np.arange(matches)
        b = np.arange(wt - matches + 1)
        c = np.arange(ht - matches + 1)

        # rows
        d = a[None, :] + b[:, None]
        rowFives = board_t[:, d]
        
        # columns
        e = a[None, :] + c[:, None]
        colFives = board_matrix[:, e]

        # anti diagonal
        main_diagFives = board_t[e[:, None, :], d[None, :, :]]

        # main diagonal
        f = np.flip(e)
        anti_diagFives = board_t[f[:, None, :], d[None, :, :]]
        

        # horizontal lines
        if np.any(np.all( rowFives == 1, axis=2)) :
            x=np.where(np.all( rowFives == 1, axis=2))[0][0]
            y=np.where(np.all( rowFives == 1, axis=2))[1][0]
            draw_line(screen, y,x,0)
        if np.any(np.all( rowFives == 2, axis=2)) :
            x=np.where(np.all( rowFives == 2, axis=2))[0][0]
            y=np.where(np.all( rowFives == 2, axis=2))[1][0]
            draw_line(screen, y,x,0)
        

        # vertical lines
        if np.any(np.all( colFives == 1, axis=2)) :
            x=np.where(np.all( colFives == 1, axis=2))[0][0]
            y=np.where(np.all( colFives == 1, axis=2))[1][0]
            draw_line(screen, x,y,90)
        if np.any(np.all( colFives == 2, axis=2)) :
            x=np.where(np.all( colFives == 2, axis=2))[0][0]
            y=np.where(np.all( colFives == 2, axis=2))[1][0]
            draw_line(screen, x,y,90)
        
        #diagonal-lines
        if np.any(np.all( main_diagFives == 1, axis=2)) :
            x=np.where(np.all( main_diagFives == 1, axis=2))[0][0]
            y=np.where(np.all( main_diagFives == 1, axis=2))[1][0]
            draw_line(screen, y,x,45)
        if np.any(np.all( main_diagFives == 2, axis=2)) :
            x=np.where(np.all( main_diagFives == 2, axis=2))[0][0]
            y=np.where(np.all( main_diagFives == 2, axis=2))[1][0]
            draw_line(screen, y,x,45)
        

        #anti-diagonal-lines
        if np.any(np.all( anti_diagFives == 1, axis=2)) :
            x=np.where(np.all( anti_diagFives == 1, axis=2))[0][0]
            y=np.where(np.all( anti_diagFives == 1, axis=2))[1][0]
            draw_line(screen, y+4,5-x,-45)
        if np.any(np.all( anti_diagFives == 2, axis=2)) :
            x=np.where(np.all( anti_diagFives == 2, axis=2))[0][0]
            y=np.where(np.all( anti_diagFives == 2, axis=2))[1][0]
            draw_line(screen, y+4,5-x,-45)
        
        if np.any(np.all( rowFives == 1, axis=2)) or np.any(np.all (colFives == 1, axis=2)) or np.any(np.all(main_diagFives == 1, axis=2)) or np.any(np.all(anti_diagFives == 1, axis=2)):
            return 1
        elif np.any(np.all( rowFives == 2, axis=2)) or np.any(np.all (colFives == 2, axis=2)) or np.any(np.all(main_diagFives == 2, axis=2)) or np.any(np.all(anti_diagFives == 2, axis=2)):
            return 2
        elif not np.any(board_matrix == 0):
            return 0
        else:
            return -1

def make_board_box(screen, x, y, value_code ):
    gap_x = col_gap
    gap_y = row_gap
    center_x = LEFT_BOARD  + (x-1) * (gap_x) + gap_x//2
    center_y = TOP_BOARD+ (y-1) * (gap_y) + gap_y//2

    if(value_code == 1):
        draw_cross(screen, center_x-gap_x//3,center_y-gap_y//3,2*min(row_gap,col_gap)//3)
    elif (value_code == 2):
        draw_O(screen, center_x-gap_x//3,center_y-gap_y//3,min(row_gap,col_gap)//3)


def draw_cross(screen, x,y,len):
    img = pygame.image.load("images/cross_ttc.png")
    img = pygame.transform.scale(img,(col_gap/3*2,row_gap/3*2))
    screen.blit(img,(x,y)) # check whether this works or not


def draw_O(screen, x,y,r):
    img = pygame.image.load("images/circle_ttc.png")
    img = pygame.transform.scale(img,(col_gap/3*2,row_gap/3*2))
    screen.blit(img,(x,y)) # check whether this works or not

def collide_box(x,y, mouse):
    top = TOP_BOARD + (y-1)*row_gap 
    left = LEFT_BOARD + (x-1) * (col_gap)

    col_rect = pygame.Rect(left, top, col_gap, row_gap)
    return col_rect.collidepoint(mouse)


def make_board(screen, board_matrix, mouse):
    center_y = TOP_BOARD + board_ht // 2
   
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

    screen.blit(sprites[status*2+turn-1], sprite_rects[turn])
def update_sprites(screen, turn):
    if turn == 1:
        make_sprite(screen, 0, 1)
        make_sprite(screen, 1, 2)
    elif turn == 2:
        make_sprite(screen, 0, 2)
        make_sprite(screen, 1, 1)

def run(user1, user2, screen):

    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    pygame.display.set_caption("Tic-Tac-Toe")
    board_img = pygame.image.load("images/tic-tac-toe.png")
    board_img = pygame.transform.scale(board_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    game_board = Board(10,10)

    game = tictactoe("Tic-Tac-Toe", player1, player2, game_board, INIT_TURN)
    board_matrix = game_board.matrix

    if not pygame.get_init():
        pygame.init()
    title_font = pygame.font.SysFont("Calibri", 60)
    pygame.display.set_caption("Tic-Tac-Toe")

    pygame.event.clear()
    running = True

    while running:
        clock = pygame.time.Clock()
        clock.tick(120)
        mouse = pygame.mouse.get_pos()
        turn = game.turn+1

        screen.blit(board_img, (0, 0))
        win_situation = game.check_win(screen)

        if win_situation == 1:
            # make_title(screen, title_font, f"{user1} WON!")
            pygame.display.update()

        elif win_situation == 2:
            # make_title(screen, title_font, f"{user2} WON!")
            pygame.display.update()

        elif win_situation == 0:
            # make_title(screen, title_font, "DRAW!") 
            pygame.display.update()
        
        command = game.update_result(screen, title_font, game, win_situation)
        if command != -1:
            return command
        screen.blit(board_img)
        update_sprites(screen, turn)
        board_matrix = game_board.matrix

        make_board(screen, board_matrix, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 3
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                filled = False
                for i in range(COLS):
                    for j in range(ROWS - 1, -1, -1):
                        if collide_box(i+1,j+1,mouse):
                            if board_matrix[i][j] != 0 : break
                            make_board_box(screen, i+1, j+1, turn)
                            update_sprites(screen,turn)
                            board_matrix[i][j] = turn
                            game.switch_turn()
                            filled = True
                            break
                if (filled):
                    break
                    
        pygame.display.update()

    return command





