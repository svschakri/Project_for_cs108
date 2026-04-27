import numpy as np 
import matplotlib.pyplot as plt
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import csv
import pygame
from datetime import date
import subprocess

# dimensions
SCREEN_WIDTH = 1537
SCREEN_HEIGHT = 1023
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
TITLE_FONT_COLOR = (255, 255, 255)

# Game over screen constants
over_title_wt = 2* (SCREEN_WIDTH // 3)
over_title_ht = SCREEN_HEIGHT // 8
over_title_y = SCREEN_HEIGHT // 4
title_button_gap = over_title_ht
# Function to fix dimensions
def dim(coords):
    return [((SCREEN_HEIGHT * coords[i]) // 1024 if i%2 == 1 else (SCREEN_WIDTH * coords[i] )// 1536 ) for i in range(len(coords))]

# button_name: [top_left_corner_x, top_left_corner_y, width, height]
button_dict = {
    "PLAY AGAIN": dim([607, 380, 320, 105]),
    "LEADERBOARD": dim([607, 497, 320, 100]),
    "GO TO MENU": dim([607, 605, 320, 100]),
    "QUIT": dim([607, 715, 320, 100])
}
OVER_TITLE_BG = (85, 250, 148)
BOX_BORDER_RADIUS = 15

class Player:
    def __init__(self, user_name):
        self.user_name = user_name
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros((width , height))

class Game:
    def __init__(self, name, player1, player2, board, turn):
        self.name = name
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.turn = turn

    def switch_turn(self): 
        self.turn = 1 - self.turn

    def check_win(self, screen = None):
        """ This would be used to check win condition """
        return
    
    # def make_title(self, screen, title_font, text_str, wt = SCREEN_WIDTH, ht = over_title_ht, center_y = over_title_ht // 2):
    #     bg_rect = pygame.Rect(0, 0, wt, ht)
    #     bg_rect.center = (SCREEN_WIDTH // 2, center_y)

    #     pygame.draw.rect(screen, OVER_TITLE_BG, bg_rect)
    #     text = title_font.render(text_str, True, TITLE_FONT_COLOR)
    #     text_rect = text.get_rect(center = bg_rect.center)
    #     screen.blit(text, text_rect)

    def make_rect(self, left, top, wt, ht):   
        return pygame.Rect(left, top, wt, ht)

    def draw_game_over(self, screen):

        if not pygame.get_init():
            pygame.init()

        command = 0
        # command = 0 --> Quit
        # command = 1 --> Play Again
        # command = 2 --> Show Leaderboard
        # command = 3 --> Back to menu
        command_dict = {
            "QUIT": 0,
            "PLAY AGAIN": 1,
            "LEADERBOARD": 2,
            "GO TO MENU": 3
        }
        screen_img = pygame.image.load("images/game_over_screen.png")
        screen_img = pygame.transform.scale(screen_img,(SCREEN_WIDTH,SCREEN_HEIGHT))
        running = True
        # button_font = pygame.font.SysFont("calibri", 40)
        while(running):
            mouse = pygame.mouse.get_pos()
            screen.blit(screen_img, (0, 0))

            rect_dict = {}
            for button_name, coords in button_dict.items():
                rect_dict[button_name] = self.make_rect(coords[0], coords[1], coords[2], coords[3])
            
            for rect in rect_dict.values():
                if (rect.collidepoint(mouse)):
                    hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    hover_surface.fill((0, 0, 0, 50))
                    screen.blit(hover_surface, rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        command = 0
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:                   
                    for name, rect in rect_dict.items():
                        if rect.collidepoint(mouse):
                            command = command_dict[name]
                            running = False
            pygame.display.flip()
        return command

    def update_result(self, screen, img_object, game, win):
        user1 = game.player1.user_name
        user2 = game.player2.user_name

        if win == 1 or win == 2 or win == 0:
            # self.make_title(screen, title_font, msgDict[win])
            pygame.display.flip()
            pygame.time.wait(500)
            # Add result to history.csv
            with open("history.csv", "a") as f:
                writer = csv.writer(f)
                winner = ""
                loser = ""
                today_date = date.today().strftime("%d-%m-%Y")
                if win != 0:
                    winner = user1 if win == 1 else user2
                    loser = user1 if win == 2 else user2
                    writer.writerow([self.name,"", winner, loser, today_date])
                else:
                    writer.writerow([self.name, "Draw", "", "", today_date])
            return self.draw_game_over(screen)
        
        return -1

if __name__ == "__main__":
    # handle users
    user1 = sys.argv[1] 
    user2 = sys.argv[2]

    # menu design
    def init_pygame(screen):
        title_font = pygame.font.SysFont(None, 100)
        header_font = pygame.font.SysFont("timesnewroman", 60)
        button_font = pygame.font.SysFont("calibri", 40)

        return title_font, header_font, button_font

    def make_box(screen, text, center_y, wt, ht, box_color, box_border_radius = 0):
        bg_rect = pygame.Rect(0, 0, wt, ht)
        bg_rect.center = (SCREEN_WIDTH // 2, center_y)

        pygame.draw.rect(screen, box_color, bg_rect, border_radius=box_border_radius)
        text_rect = text.get_rect(center = bg_rect.center)
        screen.blit(text, text_rect)

    def make_button_icon(screen, button_font, text_str, center_y, mouse):
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

    def play_game(game_name, screen):
        module_path = GAME_PATH[game_name]

        game_module = __import__(module_path, fromlist=['run'])

        command = game_module.run(user1, user2, screen)

        return command
    
    def analysis_menu():
        subprocess.run(["bash", "leaderboard.sh"])
        # display matplotlib charts
        game_freq = {}
        player_data = {} # [wins, losses, win/loss ratio]
        with open("history.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if (row[0] not in game_freq):
                    game_freq[row[0]] = 0
                game_freq[row[0]] += 1

                if (row[2] not in player_data):
                    player_data[row[2]] = [0, 0]
                if (row[3] not in player_data):
                    player_data[row[3]] = [0, 0]

                player_data[row[2]][0] += 1
                player_data[row[3]][1] += 1
        
        for data in player_data.values():
            data.append(data[0]/data[1] if data[1] != 0 else "INF")

        wins = sorted([(name, wins[0]) for name, wins in player_data.items()], reverse=True, key=lambda x: x[1])
        top_wins = wins[0:5]
        w_l_ratio = sorted([(name, wins[2] if wins[2] != "INF" else 5) for name, wins in player_data.items()], reverse=True, key=lambda x: x[1])
        top_w_l_ratio = w_l_ratio[:5]

        fig, axs = plt.subplots(2, 2, figsize = (12, 10))
        # Top 5 wins
        axs[0][0].bar([data[0] for data in top_wins], [data[1] for data in top_wins])
        axs[0][0].set_title("Top 5 Players (By win count)")

        # Top 5 W/L ratio
        axs[0][1].bar([data[0] for data in top_w_l_ratio], [data[1] for data in top_w_l_ratio])
        axs[0][1].set_title("Top 5 Players (By Win/Loss ratio)")

        # wins pie chart
        axs[1][0].pie([data[1] for data in top_wins], autopct='%1.1f%%')
        axs[1][0].legend([data[0] for data in top_wins])
        axs[1][0].set_title("Percentage of Wins")

        # most played games pie chart
        axs[1][1].pie([n for n in game_freq.values()], autopct='%1.1f%%')
        axs[1][1].legend([name for name in game_freq.keys()])
        axs[1][1].set_title("Most Played Games")
        fig.savefig("plot.png")

        # back to menu or quit shown on screen
        back_to_menu = True
        # if next run post_game_loop and return true
        return back_to_menu

    def game_loop(game_name, screen):
        while True:
            command = play_game(game_name, screen)
            if command == 0: # quit
                return False
            elif command == 1: # play again
                continue
            elif command == 2: # show leaderboard
                return analysis_menu()
            elif command == 3: # back to menu
                return True
            else:
                return False
            
    # start menu
    def start_menu():
        pygame.init()
        screen = pygame.display.set_mode(screen_size)
        title_font, header_font, button_font = init_pygame(screen)
        pygame.display.set_caption("GAME HUB")
        running = True
        #images
        menu_img = pygame.image.load("./images/menu.png")
        while running:
            mouse = pygame.mouse.get_pos()

            screen.fill(BGCOLOR)
            screen.blit( menu_img ,(0,0))

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
                game_rect_list.append((game_name, make_button_icon(screen, button_font, game_name, center_i, mouse)))
            
            # quit button
            quit_center = buttons_top + (button_number) * (button_ht + button_gap) + button_ht // 2
            quit_rect = make_button_icon(screen, button_font, "Quit", quit_center, mouse)
            
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
                            running = game_loop(game_name, screen)
                            if running:
                                title_font, header_font, button_font = init_pygame(screen)
                                pygame.display.set_caption("GAME HUB")
            if not running:
                break
            pygame.display.update()

    start_menu()
    # analysis_menu()
    pygame.quit()