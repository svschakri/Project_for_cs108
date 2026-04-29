import numpy as np 
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # hiding pygame msg
import pygame

# Add the parent directory of the current file to Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import Game, Player, Board

# FPS
MAX_FPS = 60
# screen dimensions
SCREEN_WIDTH = 1537
SCREEN_HEIGHT = 1023
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# player name rects 
Player1_name_rect = pygame.Rect(66,123,211,85)
Player2_name_rect = pygame.Rect(1269,123,211,85)
Player1_score_rect = pygame.Rect(67,286,180,130)
Player2_score_rect = pygame.Rect(1281,284,186,130)

#final images position of title like winner and loser
p1_fin_rect = pygame.Rect(64, 213, 265, 140)
p2_fin_rect = pygame.Rect(1265, 213, 265, 140)

# reset rect
reset_rect = pygame.Rect(1288,829,190,125)

# back rect
back_rect = pygame.Rect(66,829,190,125)



# board dimensions
ROWS = 8
COLS = 8
LEFT_BOARD=475
TOP_BOARD=176
board_wt = 600
board_ht  = 665
row_gap = board_ht // ROWS
col_gap = board_wt // COLS

# colors used for making glow used for showing all possible moves in respective move
GLOW_COLOR1 = (235, 64, 52) # red
GLOW_COLOR2 = (52, 92, 235) # blue

#sprite_constanst 
scale1 = 2.2 # it is just a varible for increasing the size with out writing constansts everytime
scale2 = 1.5 
sprite_ht = [375] * 4 + [375 * scale1, 375 * scale2, 375 * scale1, 375 * scale2] 
sprite_wt = [193, 198, 315, 313, 160 * scale1, 315 * scale2, 140 * scale1, 315 * scale2]
sprite_pos = [(40, 450), (1230, 450), (40,450), (1230, 450), (0, 172), (-30, 368), (1150, 130), (1100, 365)] # positions for sprites in a order of in sprites thing

# sprites in ongoing game
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
    sprites[i] = pygame.transform.smoothscale(sprites[i], (sprite_wt[i], sprite_ht[i])) # smoothscale is used for curved images

sprite_rects = [pygame.Rect(*sprite_pos[i], sprite_wt[i], sprite_ht[i]) for i in range(len(sprites))] # * -> unpacking operator which means it unpack the tuple or array or even strings 

# make a function to check win condition in new game class
class othello(Game):
   
   def  reset_game(self):
        self.board.matrix = np.zeros((8,8))
        # the below four are intial coins  in othello
        self.board.matrix[3][3]=2 
        self.board.matrix[4][4]=2
        self.board.matrix[3][4]=1
        self.board.matrix[4][3]=1
        self.move_array = [] # remove every move
        self.turn = 1  # making the move also to the first player 


   def back_game(self):
        if len(self.move_array) == 0:
            return # returns if nothing to do back 

        last_move = self.move_array.pop() # gets the last move

        played_row, played_col = last_move[0] # the is the coin position which is being placed 

        # Read code BEFORE removing the piece
        code = self.board.matrix[played_row][played_col]

        # Remove the played piece
        self.board.matrix[played_row][played_col] = 0

        # Revert flipped pieces to the opponent's color
        opponent = 3 - code
        for row, col in last_move[1:]: # all filiped coins
            self.board.matrix[row][col] = opponent 
        # self.board.matrix[self.board.matrix == 1.5] = 0
        # self.board.matrix[self.board.matrix == 2.5] = 0
        update_possible_moves(opponent,self.board.matrix) #

        self.switch_turn()

   def make_move(self, move, code ,board_matrix):
        row, col = move # move is position of the cell

        board_matrix[row][col] = code # putting the coin in 

        arr = update_values(row, col, board_matrix) # getting the array  of  this picec + all filiped pieces

        self.move_array.append(arr) 
   def check_win(self):
    board_matrix = self.board.matrix 
    a = np.sum(board_matrix == 2)
    b = np.sum(board_matrix == 1)
    if a == 0 : return 2
    if b == 0 : return 1
    if (a+b==64) : 
        if a > b:
            return 1
        elif b > a:
            return 2 # player 2 wins
        else:
            return 0 # draw 
    if (no_of_possible(board_matrix,1) == 0 and no_of_possible(board_matrix,2) == 0) : 
        if a > b:
            return 1 #player 1 wins
        elif b > a:
            return 2 # player 2 wins
        else:
            return 0 # draw 
    
    return -1 # game still going on  

def update_possible_moves(req_color,board_matrix):
    board_matrix[board_matrix==1.5] = 0 # removes the old possible moves
    board_matrix[board_matrix==2.5] = 0 
    opposite = 3-req_color
    for i in range(8):
        for j in range(8):
            if board_matrix[i,j] != 0 :
                continue
            #VERTICAL
            if j<7 :
                if board_matrix[i,j+1] == opposite :
                    a,b = i,j+1
                    while b < 8 and board_matrix[a,b] == board_matrix[i,j+1] :
                        b+=1
                    if b == j+1 : pass
                    elif  b > 7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5 #  checking whether it atleast one coin is in between or not
                        continue
            # VERTICAL - UP
            if j>0 :
                if board_matrix[i,j-1] == opposite :
                    a,b = i,j-1
                    while b > -1 and board_matrix[a,b] == board_matrix[i,j-1] :
                        b-=1
                    if b == j-1 : pass
                    elif  b < 0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
            #HORIZONTAL - RIGHT
            if i<7 :
                if board_matrix[i+1,j] == opposite :
                    a,b = i+1,j
                    while a < 8 and board_matrix[a,b] == board_matrix[i+1,j] :
                        a+=1
                    if a == i+1 : pass
                    elif  a > 7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
            #HORIZONTAL - LEFT
            if i >0 :
                if board_matrix[i-1,j] == opposite :
                    a,b = i-1,j
                    while a > -1 and board_matrix[a,b] == board_matrix[i-1,j] :
                        a-=1
                    if a == i-1 : pass
                    elif  a < 0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
                
            # TOP-LEFT-DIAG
            if i > 0 and j>0 : 
                if board_matrix[i-1,j-1] == opposite :
                    a,b = i-1,j-1
                    while a > -1 and b>-1 and board_matrix[a,b] == board_matrix[i-1,j-1] :
                        a-=1
                        b-=1
                    if b == j-1 : pass
                    elif  b<0 or a<0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
            # BOTTOM-RIGHT-DIAG 
            if i < 7 and j < 7 : 
                if board_matrix[i+1,j+1] == opposite :
                    a,b = i+1,j+1
                    while a <8 and b<8 and board_matrix[a,b] == board_matrix[i+1,j+1] :
                        a+=1
                        b+=1
                    if b == j+1 : pass
                    elif  b>7 or a>7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
            # TOP-RIGHT-DIAG 
            if i < 7 and j>0 : 
                if board_matrix[i+1,j-1] == opposite :
                    a,b = i+1,j-1
                    while a <8 and b>-1 and board_matrix[a,b] == board_matrix[i+1,j-1] :
                        a+=1
                        b-=1
                    if b == j-1 : pass
                    elif  b<0 or a>7 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue
            # BOTTOM-LEFT-DIAG 
            if i > 0 and j < 7 : 
                if board_matrix[i-1,j+1] == opposite :
                    a,b = i-1,j+1
                    while a > -1 and b<8 and board_matrix[a,b] == board_matrix[i-1,j+1] :
                        a-=1
                        b+=1
                    if b == j+1 : pass
                    elif  b>7 or a<0 : pass
                    elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
                    else :
                        board_matrix[i,j] = req_color + 0.5
                        continue


def update_values(i,j,board_matrix):
    color_code = board_matrix[i,j]
    oppenent = 3 - color_code
    arr = [(i,j)] # arr includes first point + filiping coins locations
    #VERTICAL - DOWN 
    if j<7 :
        if board_matrix[i,j+1] ==  oppenent : # if passed then taking it as ref 
            a,b = i,j+1
            while b < 8 and board_matrix[a,b] == board_matrix[i,j+1] :
                b+=1
            if b == j+1 : pass # no use as the coin not between two identical coins for all remaining three cases
            elif  b > 7 : pass 
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i,j:b]=color_code # changing the coin
                arr += [(i,k) for k in range(j+1,b)] # storing the positions of the changed coins
    #VERTICAL - UP 
    if j>0 :
        if board_matrix[i,j-1] == oppenent :
            a,b = i,j-1
            while b >-1 and board_matrix[a,b] == board_matrix[i,j-1] :
                b-=1
            if b == j-1 : pass
            elif  b <0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i,b:j]=color_code
                arr += [(i,k) for k in range(b+1,j)] 

    #HORIZONTAL - RIGHT
    if i<7 :
        if board_matrix[i+1,j] == oppenent :
            a,b = i+1,j
            while a < 8 and board_matrix[a,b] == board_matrix[i+1,j] :
                a+=1
            if a == i-1 : pass
            elif  a > 7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[i:a,j] = color_code
                arr += [(k,j) for k in range(i+1,a)] 
                pass
    #HORIZONTAL - LEFT
    if i >0 :
        if board_matrix[i-1,j] == oppenent:
            a,b = i-1,j
            while a > -1 and board_matrix[a,b] == board_matrix[i-1,j] :
                a-=1
            if a == i-1 : pass
            elif  a < 0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                board_matrix[a:i,j] = color_code
                arr += [(k,j) for k in range(a+1,i)] 
                pass
        
    # TOP-LEFT-DIAG
    if i > 0 and j>0 : 
        if board_matrix[i-1,j-1] == oppenent :
            a,b = i-1,j-1
            while a > -1 and b>-1 and board_matrix[a,b] == board_matrix[i-1,j-1] :
                a-=1
                b-=1
            if b == j-1 : pass
            elif  b<0 or a<0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                np.fill_diagonal(board_matrix[a:i, b:j], color_code)
                arr+=[(i-k,j-k) for k in range(1,i-a)]
                pass
    # BOTTOM-RIGHT-DIAG 
    if i < 7 and j < 7 : 
        if board_matrix[i+1,j+1] == oppenent :
            a,b = i+1,j+1
            while a <8 and b<8 and board_matrix[a,b] == board_matrix[i+1,j+1] :
                a+=1
                b+=1
            if b == j+1 : pass
            elif  b>7 or a>7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                np.fill_diagonal(board_matrix[i:a, j:b], color_code)
                arr+=[(i+k,j+k) for k in range(1,a-i)]
                pass
    # TOP-RIGHT-DIAG 
    if i < 7 and j>0 : 
        if board_matrix[i+1,j-1] == oppenent:
            a,b = i+1,j-1
            while a <8 and b>-1 and board_matrix[a,b] == board_matrix[i+1,j-1] :
                a+=1
                b-=1
            if b == j-1 : pass
            elif  b<0 or a>7 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                for k in range (b,j) :
                    board_matrix[i+abs(j-k),k] =color_code
                arr+=[(i+k,j-k) for k in range(1,a-i)]
                pass
    # BOTTOM-LEFT-DIAG 
    if i > 0 and j < 7 : 
        if board_matrix[i-1,j+1] == oppenent:
            a,b = i-1,j+1
            while a > -1 and b<8 and board_matrix[a,b] == board_matrix[i-1,j+1] :
                a-=1
                b+=1
            if b == j+1 : pass
            elif  b>7 or a<0 : pass
            elif board_matrix [a,b] in (0 ,1.5 ,2.5) : pass
            else :
                for k in range (a,i) :
                    board_matrix[k,j+abs(i-k)] = color_code
                arr+=[(i-k,j+k) for k in range(1,i-a)]
                pass
    
    return arr

def make_score(screen,board_matrix,Number_font):
    tot_1 = np.sum(board_matrix == 2) # for player 1
    tot_2 = np.sum(board_matrix == 1) # for player 2

    text_1 = Number_font.render(str(tot_1), True, (250, 250, 250))
    text_2 = Number_font.render(str(tot_2), True, (250, 250, 250))

    screen.blit(text_1, Player1_score_rect.center)
    screen.blit(text_2, Player2_score_rect.center)


def make_board_circle(screen,x, y, color_code):
    r = min(col_gap,row_gap)*2/5 
    gap_x = col_gap
    gap_y = row_gap
    center_x = LEFT_BOARD  + (x-1) * ( gap_x ) +  gap_x //2 
    center_y = TOP_BOARD + (y-1) * ( gap_y ) + gap_y //2

    if (color_code == 2):
        ball_img =pygame.image.load("images/White_othello.png")
        ball_img = pygame.transform.scale(ball_img,(2*r,2*r))
        rect = ball_img.get_rect(center=(center_x, center_y))
    elif (color_code == 1):
        ball_img =pygame.image.load("images/Black_othello.png")
        ball_img = pygame.transform.scale(ball_img,(2*r,2*r))
        rect = ball_img.get_rect(center=(center_x, center_y))
    elif (color_code == 1.5):
        glow_col = GLOW_COLOR1 # red 
    elif (color_code == 2.5):
        glow_col = GLOW_COLOR2 # blue

    if color_code in (1.5,2.5) :
        create_glow(screen, r, center_x, center_y, glow_col)
    elif color_code != 0 :
        screen.blit(ball_img,rect)

def create_glow(screen, radius, x, y, glow_color = (255, 255, 0), alpha = 80): # creates a new surface to show the transplant glow
    glow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA) 
    pygame.draw.circle(glow, (*glow_color, alpha), (radius, radius), radius)
    screen.blit(glow, (x-radius, y-radius))

def collide_box(x,y, mouse): # checks whether mouse click that or not
    top = TOP_BOARD + (y-1)*row_gap 
    left = LEFT_BOARD + (x-1) * (col_gap)

    col_rect = pygame.Rect(left, top, col_gap, row_gap)
    return col_rect.collidepoint(mouse)
def draw_over(screen, win): # final winning screen
    win_title_img = pygame.image.load("images/winner_title.png")
    win_title_img = pygame.transform.scale(win_title_img,(265,140))
    lose_title_img = pygame.image.load("images/loser_title.png")
    lose_title_img = pygame.transform.scale(lose_title_img,(265,140))

    # if win == 1 --> draw happy_blue (sprites idx = 6) and crying_red (sprites idx = 5)
    if win == 1:
        screen.blit(win_title_img,p1_fin_rect)
        screen.blit(lose_title_img,p2_fin_rect)
        screen.blit(sprites[5], sprite_rects[5]) 
        screen.blit(sprites[6], sprite_rects[6])
    # if win == 2 --> draw crying_blue (sprites idx = 4) and happy_red (sprites idx = 7)
    else:
        screen.blit(win_title_img,p2_fin_rect)
        screen.blit(lose_title_img,p1_fin_rect)
        screen.blit(sprites[4], sprite_rects[4])
        screen.blit(sprites[7], sprite_rects[7])
    
    pygame.time.wait(2000)

def make_board(screen,board_matrix,Number_font, mouse):
    center_y = TOP_BOARD + board_ht // 2
    board_rect = pygame.Rect(0, 0, board_wt, board_ht)
    board_rect.center = (SCREEN_WIDTH // 2, center_y)

    make_score(screen,board_matrix,Number_font)

    for i in range(COLS):
        for j in range(ROWS):
            make_board_circle(screen,i+1, j+1, board_matrix[i][j])

    for i in range(COLS):
        for j in range(ROWS):
            if collide_box(i,j,mouse):
                if board_matrix[i][j] == 0:
                    make_board_circle(screen,i+1, j+1,0)

def make_sprite(screen, status, turn):
    # status = 0 --> passive
    # status = 1 --> active
    # status*2 + turn-1 acts like a bijection function 
    screen.blit(sprites[status*2 + turn-1], sprite_rects[status*2 + turn-1])

# it is used for updating sprites from making passice to active and active to passive respectively based on turn
def update_sprites(screen, turn):
    if turn == 1:
        make_sprite(screen, 0, 1)
        make_sprite(screen, 1, 2)
    elif turn == 2:
        make_sprite(screen, 0, 2)
        make_sprite(screen, 1, 1)

# text writting function with req font and color at the req position on the require screen
def write_text(screen,text,rect,font,color) :
        rendered_font = font.render(text, True,color)
        text_rect = rendered_font.get_rect()
        text_rect.center = rect.center
        screen.blit(rendered_font, text_rect)
def no_of_possible(matrix,code) :
    matrix2=matrix.view()
    update_possible_moves(code,matrix2)
    return np.sum(matrix2==code+0.5)

def run(user1,user2, screen, flag):
    INIT_TURN = 1 # initial turn 1 represents left side player(blue)(p1)
    player1 = Player(user1)
    player2 = Player(user2)
    if not pygame.get_init():
        pygame.init()
    pygame.display.set_caption("othello")
    running = True
    board_img = pygame.image.load("images/othello_board.jpeg") # board image
    board_img = pygame.transform.scale(board_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    game_board = Board(8,8)

    game = othello("Othello", player1, player2, game_board, INIT_TURN)
    if flag: # game over screen
        return game.draw_game_over(screen)
    font=pygame.font.Font("./fonts/Cinzel-VariableFont_wght.ttf", 36)
    Number_font = font

    game_board.matrix[3][3]=2
    game_board.matrix[4][4]=2
    game_board.matrix[4][3]=1
    game_board.matrix[3][4]=1
    while running:
        clock = pygame.time.Clock()
        clock.tick(MAX_FPS) # stes the maximum fps

        mouse = pygame.mouse.get_pos()
        turn = game.turn 

        piece_code = 1 + turn 
        # piece_code  1 --> right(2)(red)
        #             2 --> left(1)(red)
        
        screen.blit(board_img) # board image
        write_text(screen,game.player1.user_name,Player1_name_rect,font,"#E2E8F0") # player names
        write_text(screen,game.player2.user_name,Player2_name_rect,font,"#E2E8F0")
        board_matrix = game_board.matrix
        update_possible_moves( piece_code, board_matrix) 
        make_board(screen, board_matrix, Number_font, mouse)
        update_sprites(screen, piece_code)
        
        if (no_of_possible(board_matrix.view(),piece_code) == 0) :
            game.switch_turn()
            make_board(screen,board_matrix,Number_font,mouse)
            pygame.display.update()
            pygame.time.wait(1000)
            continue
        command = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 3
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos) :
                    game.back_game()
                    start=False
                    board_matrix=game.board.matrix
                    continue
                if reset_rect.collidepoint(event.pos) :
                    game.reset_game()
                    board_matrix=game.board.matrix
                    continue
                filled = False
                for i in range(COLS):
                    for j in range(ROWS - 1, -1, -1):
                        if collide_box(i+1,j+1,mouse):
                            # print(mouse)
                            if board_matrix[i][j] != piece_code+0.5 :
                                break
                            start = True
                            game.make_move((i, j), piece_code ,board_matrix)
                            update_sprites(screen, piece_code)
                            # update_values(i, j, board_matrix)
                            win = game.check_win()
                            if (win == 1 or win == 2) :
                                screen.blit(board_img,(0,0))
                                write_text(screen,user1.capitalize(),Player1_name_rect,font,"#E2E8F0")
                                write_text(screen,user2.capitalize(),Player2_name_rect,font,"#E2E8F0")
                                make_board(screen,board_matrix,font,mouse)
                                draw_over(screen, win)
                            command = game.update_result(screen, game, win)
                            if command != -1:
                                return command
                            game.switch_turn()
                            filled = True
                            break
                if (filled): # what is the use of this condition any ways
                    break
            
        pygame.display.update()
        if command != -1:
            return command

    return command
