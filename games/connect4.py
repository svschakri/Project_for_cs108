import numpy as np 
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import Game, Player, Board

# FPS
MAX_FPS = 60
# screen dimensions
SCREEN_WIDTH = 1537
SCREEN_HEIGHT = 1023
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

board_scale = 1.4
board_img_ht = ((SCREEN_HEIGHT * 681) // 1023) * board_scale
board_img_wt = ((SCREEN_WIDTH * 1024) // 1537) * board_scale
board_left = (SCREEN_WIDTH - board_img_wt) // 2
board_top = 50
coin_board_left = 446
coin_board_top = 305
col_gap = 24
row_gap = 18
st_gap_x = 38
st_gap_y = 16
sprite_ht = [250] * 4
sprite_wt = [(sprite_ht[0] * 359) // 695,(sprite_ht[0] * 363) // 687, (sprite_ht[1] * 457) // 546,(sprite_ht[1] * 458) // 585]
coin_radius = 30
sprite_pos = [(160, 440),(160, 440), (1210, 440),(1210, 440)]
ph_wt = 550
placeholder_dim = (ph_wt, (ph_wt * 379) // 676)
placeholder_pos = [(-50, 690), (1030, 690)]
FALLING_TIME = 15
# Images
#screen
screen_img = pygame.image.load("images/connect4_screen.png")
screen_img = pygame.transform.scale(screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
# coins

coin1 = pygame.image.load("images/bronze_connect4-removebg.png")
glow_coin1 = pygame.image.load("images/bronze_connect4_glowing.png")
win_glow_coin1 = pygame.image.load("images/skull_glowing.png")

coin2 = pygame.image.load("images/silver_connect4-removebg.png")
glow_coin2 = pygame.image.load("images/silver_connect4_glow.png")
win_glow_coin2 = pygame.image.load("images/spider_glowing.png")

coins = [coin1, coin2]
glow_coins = [glow_coin1, glow_coin2] 
win_glow_coins = [win_glow_coin1, win_glow_coin2]

for i in range(2):
    coins[i] = pygame.transform.smoothscale(coins[i], (coin_radius*2, coin_radius*2))
    glow_coins[i] = pygame.transform.smoothscale(glow_coins[i], (coin_radius*2, coin_radius*2))
    win_glow_coins[i] = pygame.transform.smoothscale(win_glow_coins[i], (coin_radius*2, coin_radius*2))

# sprites
sprite_still_blue = pygame.image.load("images/sprite_still_blue.png")
sprite_still_red = pygame.image.load("images/sprite_still_red.png")
sprite_active_blue = pygame.image.load("images/sprite_active_blue.png")
sprite_active_red = pygame.image.load("images/sprite_active_red.png")
sprites = [sprite_still_blue,sprite_still_red, sprite_active_blue,sprite_active_red]

for i in range(len(sprites)):
    sprites[i] = pygame.transform.smoothscale(sprites[i], (sprite_wt[i], sprite_ht[i]))

sprite_rects = [pygame.Rect(*sprite_pos[i], sprite_wt[i], sprite_ht[i]) for i in range(4)]

# board
board_img = pygame.image.load("images/connect4_board.png")
board_img = pygame.transform.smoothscale(board_img, (board_img_wt, board_img_ht))
coord_map = np.zeros((COLS, ROWS, 2))

# placeholders
ph_img = pygame.image.load("images/placeholder.png")
ph_img = pygame.transform.scale(ph_img, placeholder_dim)
# form coordinates and row-col pair map
for i in range(COLS):
    for j in range(ROWS):
        coord_map[i][j][0] = coin_board_left + st_gap_x + i*(2*coin_radius + col_gap) + coin_radius
        coord_map[i][j][1] = coin_board_top + st_gap_y + j*(2*coin_radius + row_gap) + coin_radius

col_rects = []
cell_w = 2 * coin_radius + col_gap
cell_h = 2 * coin_radius + row_gap
for col in range(COLS):
    left = coin_board_left + st_gap_x + col * cell_w - col_gap // 2
    top = coin_board_top + st_gap_y

    rect = pygame.Rect(left, top, cell_w, cell_h * ROWS )
    col_rects.append(rect)

# reset rectangle
reset_rect = pygame.Rect(514, 931, 140, 50)
reset_img = None
# back rectangle
back_rect = pygame.Rect(875, 931, 140, 50)
back_img = None

class Connect4(Game):
    def check_win(self, move):
        board_matrix = self.board.matrix
        x, y = move
        player = int(board_matrix[x][y])
        
        # Add padding in board_matrix
        padded_board = np.pad(board_matrix, pad_width=3)
        if player == 0:
            return [-1, None, None, None]
        pad_x = x + 3
        pad_y = y + 3
        temp = np.arange(4) 

        # Horizontal
        window_x = pad_x - temp
        windows = padded_board[window_x[:, None] + temp, pad_y]
        matches = np.all(windows == player, axis=1)
        if np.any(matches):
            idx = np.where(matches)[0][0]
            return [player, window_x[idx]-3, y, 0]

        # Vertical
        window_y = pad_y - temp
        windows = padded_board[pad_x, window_y[:, None] + temp]
        matches = np.all(windows == player, axis=1)
        if np.any(matches):
            idx = np.where(matches)[0][0]
            return [player, x, window_y[idx]-3, 90]

        # Main Diagonal
        window_x = pad_x - temp
        window_y = pad_y - temp
        windows = padded_board[window_x[:, None] + temp, window_y[:, None] + temp]
        matches = np.all(windows == player, axis=1)
        if np.any(matches):
            idx = np.where(matches)[0][0]
            return [player, window_x[idx]-3, window_y[idx]-3, 45]

        # Anti-Diagonal
        window_x = pad_x + temp
        window_y = pad_y - temp
        windows = padded_board[window_x[:, None] - temp, window_y[:, None] + temp]
        matches = np.all(windows == player, axis=1)
        if np.any(matches):
            idx = np.where(matches)[0][0]
            return [player, window_x[idx]-3, window_y[idx]-3, -45]

        # Check for draw
        if not np.any(board_matrix == 0):
            return [0, None, None, None]
            
        return [-1, None, None, None]
        
# glow == 0 --> No glow
# glow == 1 --> Natural hover glow
# glow == 2 --> Golden (after win glow)

def make_coin(screen, x, y, turn, glow=0):
    if glow == 0:
        coin = coins[turn-1]
    elif glow == 1:
        coin = glow_coins[turn-1]
    elif glow == 2:
        coin = win_glow_coins[turn-1]
    screen.blit(coin, (x-coin_radius, y-coin_radius))

def make_board_coin(screen, i, j, turn, glow=0):
    x = coord_map[i][j][0]
    y = coord_map[i][j][1]
    make_coin(screen, x, y, turn, glow)

def make_win_glow(screen, x, y, turn, theta):
    if theta == 0:
        for i in range(4):
            x_i = x + i
            y_i = y
            make_board_coin(screen, x_i, y, turn, glow=2)
    elif theta == -45 :
        for i in range(4):
            x_i = x - i
            y_i = y + i
            make_board_coin(screen, x_i, y_i, turn, glow=2)
    elif theta == 45:
        for i in range(4):
            x_i = x + i
            y_i = y + i
            make_board_coin(screen, x_i, y_i, turn, glow=2)
    elif theta == 90:
        for i in range(4):
            x_i = x
            y_i = y + i
            make_board_coin(screen, x_i, y_i, turn, glow=2)

def collide_col(i, mouse):
    return col_rects[i].collidepoint(mouse)

def make_placeholders(screen, game):
    player_names = [game.player1.user_name, game.player2.user_name]
    rects = []
    player_texts = []
    player_font = pygame.font.SysFont("timesnewroman", 40)
    for i in range(2):
        rect = pygame.Rect(*placeholder_pos[i], *placeholder_dim)
        screen.blit(ph_img, rect)
        rects.append(rect)

        font = player_font.render(player_names[i], True, WHITE)
        player_texts.append(font)

    text_rects = [text.get_rect() for text in player_texts]
    for i in range(2):
        text_rects[i].center = rects[i].center
        screen.blit(player_texts[i], text_rects[i])
    
def make_screen(screen, board_matrix, mouse):
    for i in range(COLS):
        for j in range(ROWS):
            if (int(board_matrix[i][j]) != 0):
                make_board_coin(screen, i, j, int(board_matrix[i][j]))
    
    for i in range(COLS):
        if collide_col(i, mouse):
            for j in range(ROWS):
                if (int(board_matrix[i][j]) != 0):
                    make_board_coin(screen, i, j, int(board_matrix[i][j]), 1)


def add_board(screen):
    screen.blit(board_img, (board_left, board_top))

def make_sprite(screen, status, turn):
    # status = 0 --> passive
    # status = 1 --> active
    screen.blit(sprites[status*2+turn-1], sprite_rects[turn])

def update_sprites(screen, turn):
    if turn == 1:
        make_sprite(screen, 0, 1) # blue active
        make_sprite(screen, 1, 2) # red still
    elif turn == 2:
        make_sprite(screen, 0, 2) # red active
        make_sprite(screen, 1, 1) # blue still

def update_screen(screen, board_matrix, game, mouse, i, j, turn):
    board_matrix[i][j] = 0
    init_y = coord_map[i][0][1]
    fin_y = coord_map[i][j][1]
    x = coord_map[i][j][0]
    for k in range(FALLING_TIME):
        y = init_y + ((fin_y - init_y)*k)/(FALLING_TIME-1)
        screen.blit(screen_img, (0, 0))
        make_screen(screen, board_matrix, mouse)
        make_coin(screen, x , y, turn)
        update_sprites(screen, turn)
        add_board(screen)
        make_placeholders(screen, game)
        make_buttons(screen)
        pygame.display.flip()
    board_matrix[i][j] = turn

def make_buttons(screen):
    pygame.draw.rect(screen, (255, 0, 0), reset_rect)
    pygame.draw.rect(screen, (0, 255, 0), back_rect)
    pass

def run(user1, user2, screen, flag):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    game_board = Board(7, 7)

    game = Connect4("Connect Four", player1, player2, game_board, INIT_TURN)
    board_matrix = game_board.matrix
    if flag:
        return game.draw_game_over(screen)
    if not pygame.get_init():
        pygame.init()
    pygame.display.set_caption("Connect Four")

    pygame.event.clear()
    running = True

    while running:
        clock = pygame.time.Clock()
        clock.tick(MAX_FPS)
        mouse = pygame.mouse.get_pos()
        turn = game.turn + 1

        screen.blit(screen_img, (0, 0))
        make_screen(screen, board_matrix, mouse)
        add_board(screen)
        update_sprites(screen, turn)
        make_placeholders(screen, game)

        make_buttons(screen)
        command = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 3
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(mouse)
                if reset_rect.collidepoint(event.pos):
                    game.reset_game()
                    board_matrix = game.board.matrix
                if back_rect.collidepoint(event.pos):
                    game.back_game()
                filled = False
                for i in range(COLS):
                    if collide_col(i, event.pos):
                        for j in range(ROWS - 1, -1, -1):
                            if int(board_matrix[i][j]) == 0:
                                # board_matrix[i][j] = 1 if turn == 1 else 2
                                game.make_move((i, j), turn)
                                update_screen(screen, board_matrix, game, mouse, i, j, turn)
                                pygame.event.clear(pygame.MOUSEBUTTONDOWN) # Clears all clicks in event queue registered in update_screen

                                win, x, y, theta = game.check_win((i, j))
                                if (win == 1 or win == 2):
                                    make_win_glow(screen, x, y, turn, theta)

                                command = game.update_result(screen, game, win)

                                game.switch_turn()
                                filled = True
                                break
                    if (filled):
                        break
                    
        pygame.display.flip()
        if command != -1:
            return command

    return command