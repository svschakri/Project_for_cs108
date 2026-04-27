import numpy as np 
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import Game, Player, Board

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
sprite_scale = 1.3
sprite_ht = [100 * sprite_scale, 170 * sprite_scale]
sprite_wt = [(sprite_ht[0] * 706) // 354, (sprite_ht[1] * 546) // 457]
coin_radius = 30
sprite_pos = [(160, 440), (1210, 440)]
ph_wt = 550
placeholder_dim = (ph_wt, (ph_wt * 379) // 676)
placeholder_pos = [(-50, 690), (1030, 690)]
FALLING_TIME = 15
# Images
#screen
screen_img = pygame.image.load("images/connect4_screen.png")
screen_img = pygame.transform.scale(screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
# coins
coin1 = pygame.image.load("images/silver_connect4-removebg.png")
glow_coin1 = pygame.image.load("images/silver_connect4_glow.png")

coin2 = pygame.image.load("images/bronze_connect4-removebg.png")
glow_coin2 = pygame.image.load("images/bronze_connect4_glowing.png")

coins = [coin1, coin2]
glow_coins = [glow_coin1, glow_coin2] 

for i in range(2):
    coins[i] = pygame.transform.smoothscale(coins[i], (coin_radius*2, coin_radius*2))
    glow_coins[i] = pygame.transform.smoothscale(glow_coins[i], (coin_radius*2, coin_radius*2))

# sprites
sprite_passive = pygame.image.load("images/sprite_passive.png")
sprite_active = pygame.image.load("images/sprite_active.png")
sprites = [sprite_passive, sprite_active]

for i in range(len(sprites)):
    sprites[i] = pygame.transform.smoothscale(sprites[i], (sprite_ht[i], sprite_wt[i]))

sprite_rects = [pygame.Rect(*sprite_pos[i], sprite_wt[i], sprite_ht[i]) for i in range(2)]

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
    left = coin_board_left + st_gap_x + col * cell_w
    top = coin_board_top + st_gap_y

    rect = pygame.Rect(left, top, cell_w, cell_h * ROWS )
    col_rects.append(rect)


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

def make_coin(screen, x, y, turn, glow=False):
    if not glow:
        coin = coins[turn-1]
    else:
        coin = glow_coins[turn-1]
    screen.blit(coin, (x-coin_radius, y-coin_radius))

def make_board_coin(screen, i, j, turn, glow=False):
    x = coord_map[i][j][0]
    y = coord_map[i][j][1]
    make_coin(screen, x, y, turn, glow)

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
                    make_board_coin(screen, i, j, int(board_matrix[i][j]), True)


def add_board(screen):
    screen.blit(board_img, (board_left, board_top))

def make_sprite(screen, status, turn):
    # status = 0 --> passive
    # status = 1 --> active
    screen.blit(sprites[status], sprite_rects[turn-1])

def update_sprites(screen, turn):
    if turn == 1:
        make_sprite(screen, 0, 1)
        make_sprite(screen, 1, 2)
    elif turn == 2:
        make_sprite(screen, 0, 2)
        make_sprite(screen, 1, 1)

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
        pygame.display.flip()
    board_matrix[i][j] = turn

def run(user1, user2, screen):
    INIT_TURN = 1
    player1 = Player(user1)
    player2 = Player(user2)

    game_board = Board(7, 7)

    game = Connect4("Connect Four", player1, player2, game_board, INIT_TURN)
    board_matrix = game_board.matrix

    if not pygame.get_init():
        pygame.init()
    title_font = pygame.font.SysFont("Calibri", 60)
    pygame.display.set_caption("Connect Four")

    pygame.event.clear()
    running = True

    while running:
        clock = pygame.time.Clock()
        clock.tick(120)
        mouse = pygame.mouse.get_pos()
        turn = game.turn + 1

        screen.blit(screen_img, (0, 0))
        make_screen(screen, board_matrix, mouse)
        add_board(screen)
        update_sprites(screen, turn)
        make_placeholders(screen, game)
        command = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command = 3
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(mouse)
                filled = False
                for i in range(COLS):
                    if collide_col(i, event.pos):
                        for j in range(ROWS - 1, -1, -1):
                            if int(board_matrix[i][j]) == 0:
                                board_matrix[i][j] = 1 if turn == 1 else 2
                                update_screen(screen, board_matrix, game, mouse, i, j, turn)
                                win = game.check_win()
                                command = game.update_result(screen, screen_img, game, win)
                                game.switch_turn()
                                filled = True
                                break
                    if (filled):
                        break
                    
        pygame.display.flip()
        if command != -1:
            return command

    return command