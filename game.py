import numpy as np 
import matplotlib
import pathlib
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import time
import subprocess

class Player:
    def __init__(self, user_name):
        self.user_name = user_name
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros((width , height))

class Game:
    def __init__(self, player1, player2, board, turn):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.turn = turn

    def switch_turn(self):
        self.turn = 1 - self.turn

    def check_win(self):
        """ This would be used to check win condition """
        return

if __name__ == "__main__":
    # handle users
    user1 = sys.argv[1] 
    user2 = sys.argv[2]

    # dimensions
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1000
    screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

    title_ht, title_wt = SCREEN_HEIGHT // 5, SCREEN_WIDTH
    title_header_gap = SCREEN_HEIGHT // 20

    header_ht = SCREEN_HEIGHT // 6
    header_wt = 2 * (SCREEN_WIDTH // 3)
    HEADER_BORDER_RADIUS = 50

    GAME_PATH = {} 
    GAME_LIST = []

    with open("games.csv", "r") as f:
        for line in f:
            line_arr = line.strip().split(",")
            GAME_PATH[line_arr[0]] = line_arr[1]
            GAME_LIST.append(line_arr[0])

    GAME_LIST = list(GAME_PATH.keys())

    button_number = len(GAME_LIST)
    button_wt = SCREEN_WIDTH // 3         
    button_ht = SCREEN_HEIGHT // 12
    button_gap = SCREEN_HEIGHT // 24
    button_stack_ht = (button_number)*button_gap + (button_number+1)*button_ht # include quit button

    header_box_gap = (SCREEN_HEIGHT - title_ht - title_header_gap - header_ht - button_stack_ht) // 3
    BOX_BORDER_RADIUS = 10

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BGCOLOR = (245, 182, 66)

    TITLE_BG = (111, 245, 66)
    TITLE_COLOR = WHITE

    HEADER_BG = (239, 245, 66)
    HEADER_COLOR = BLACK

    BUTTON_BG = (245, 66, 233)
    LIGHT_BUTTON_BG = (237, 147, 227)
    BUTTON_FONT_COLOR = WHITE

    QUIT_BG = (242, 90, 63)
    LIGHT_QUIT_BG = (242, 121, 99)
        
    # menu design
    def init_pygame():
        pygame.init()
        screen = pygame.display.set_mode(screen_size)

        title_font = pygame.font.SysFont(None, 100)
        header_font = pygame.font.SysFont("timesnewroman", 60)
        button_font = pygame.font.SysFont("calibri", 40)

        return screen, title_font, header_font, button_font

    def make_box(screen, text, center_y, wt, ht, box_color, box_border_radius = 0):
        bg_rect = pygame.Rect(0, 0, wt, ht)
        bg_rect.center = (SCREEN_WIDTH // 2, center_y)

        pygame.draw.rect(screen, box_color, bg_rect, border_radius=box_border_radius)
        text_rect = text.get_rect(center = bg_rect.center)
        screen.blit(text, text_rect)

    def make_button(screen, button_font, text_str, center_y, mouse):
        text = button_font.render(text_str, True, BUTTON_FONT_COLOR)
        button_rect = pygame.Rect(0, 0, button_wt, button_ht)
        button_rect.center = (SCREEN_WIDTH // 2, center_y)

        button_color = BUTTON_BG if text_str != "Quit" else QUIT_BG
        if button_rect.collidepoint(mouse):
            button_color = LIGHT_BUTTON_BG if text_str != "Quit" else LIGHT_QUIT_BG

        pygame.draw.rect(screen, button_color, button_rect, border_radius=BOX_BORDER_RADIUS)
        text_rect = text.get_rect(center = button_rect.center)
        screen.blit(text, text_rect)
        return button_rect

    def play_game(game_name):
        module_path = GAME_PATH[game_name]   # e.g. "games.tictactoe"

        game_module = __import__(module_path, fromlist=['run'])

        command = game_module.run(user1, user2)

        return command
    
    def analysis_menu():
        subprocess.run(["bash", "leaderboard.sh"])
        # display matplotlib charts
        
        # back to menu or quit shown on screen
        back_to_menu = True
        # if next run post_game_loop and return true
        return back_to_menu


    def game_over_menu(game_name):
        while True:
            command = play_game(game_name)
            if command == 0: # quit
                return False
            elif command == 1: # play again
                continue
            elif command == 2: # show leaderboard
                return analysis_menu()
            else:
                return False
            
    # start menu
    def start_menu():
        screen, title_font, header_font, button_font = init_pygame()
        pygame.display.set_caption("GAME HUB")
        running = True
        while running:
            mouse = pygame.mouse.get_pos()

            screen.fill(BGCOLOR)

            # title
            title_text = title_font.render("GAME HUB", True, TITLE_COLOR)
            title_center_y = title_ht // 2
            make_box(screen, title_text, title_center_y, title_wt, title_ht, TITLE_BG)

            # header
            header_text = header_font.render(f"{user1} V/S {user2}", True, HEADER_COLOR)
            header_center_y = title_ht + title_header_gap + header_ht // 2
            make_box(screen, header_text, header_center_y, header_wt, header_ht, HEADER_BG, HEADER_BORDER_RADIUS)

            # game buttons
            game_rect_list = []
            buttons_top =  title_ht + title_header_gap + header_ht + header_box_gap

            for i in range(button_number):
                game_name = GAME_LIST[i]
                center_i = buttons_top + i * (button_ht + button_gap) + button_ht // 2
                game_rect_list.append((game_name, make_button(screen, button_font, game_name, center_i, mouse)))
            
            # quit button
            quit_center = buttons_top + (button_number) * (button_ht + button_gap) + button_ht // 2
            quit_rect = make_button(screen, button_font, "Quit", quit_center, mouse)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_rect.collidepoint(mouse):
                        running = False

                    for game_name, game_rect in game_rect_list:
                        if game_rect.collidepoint(mouse):
                            while True:
                                e = pygame.event.wait()
                                if e.type == pygame.MOUSEBUTTONUP:
                                    break
                                pygame.event.clear()
                                
                            running = game_over_menu(game_name)
                            if running:
                                screen, title_font, header_font, button_font = init_pygame()
                                pygame.display.set_caption("GAME HUB")
            if not running:
                break
            pygame.display.update()

    start_menu()
    pygame.quit()
    sys.exit()