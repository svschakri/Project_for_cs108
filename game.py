import numpy as np 
import matplotlib.pyplot as plt
import sys
import os 
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import csv
import pygame
from datetime import date
import subprocess

# FPS
MAX_FPS = 60

# dimensions
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 1024
screen_size = SCREEN_WIDTH, SCREEN_HEIGHT

# Games added : handled using games.csv
GAME_PATH = {} 
GAME_LIST = []

with open("games.csv", "r") as f:
    for line in f:
        line_arr = line.strip().split(",")
        GAME_PATH[line_arr[0]] = line_arr[1]
        GAME_LIST.append(line_arr[0])

GAME_LIST = list(GAME_PATH.keys())

button_number = len(GAME_LIST)

# Maintain aspect ratio and relative coordinates using this function
def dim(coords):
    return [((SCREEN_HEIGHT * coords[i]) // 1024 if i%2 == 1 else (SCREEN_WIDTH * coords[i] )// 1536 ) for i in range(len(coords))]

# button_name: [top_left_corner_x, top_left_corner_y, width, height]
button_dict = {
    "PLAY AGAIN": dim([607, 380, 320, 105]),
    "LEADERBOARD": dim([607, 497, 320, 100]),
    "GO TO MENU": dim([607, 605, 320, 100]),
    "QUIT": dim([607, 715, 320, 100])
}

# Assets used for "Sort by" GUI
sort_img = pygame.image.load("images/sort_dialog_box.png")
sort_img = pygame.transform.scale(sort_img, screen_size)

sort_rects = [None]*3
sort_rect_wins = pygame.Rect(647, 390, 242, 62)
sort_rect_losses = pygame.Rect(647, 540, 242, 62)
sort_rect_ratio = pygame.Rect(647, 688, 242, 62)

sort_rects = [sort_rect_wins, sort_rect_losses, sort_rect_ratio]

class Player:
    def __init__(self, user_name):
        self.user_name = user_name
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros((width , height))

# Game class: used for creating game objects in each game
class Game:
    def __init__(self, name, player1, player2, board, turn):
        self.name = name
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.turn = turn
        self.move_array = []

    def switch_turn(self): 
        self.turn = 1 - self.turn

    # Overridable function
    def check_win(self):
        """ This would be used to check win condition """
        return

    def make_rect(self, left, top, wt, ht):   
        return pygame.Rect(left, top, wt, ht)

    # Draw GUI of game over screen
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
        # Load background image of screen
        screen_img = pygame.image.load("images/game_over_screen.png")
        screen_img = pygame.transform.scale(screen_img,(SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Game Over")
        running = True

        while(running):
            clock = pygame.time.Clock()
            clock.tick(MAX_FPS)
            mouse = pygame.mouse.get_pos()
            screen.blit(screen_img, (0, 0))
            
            # Rectangles for each button
            rect_dict = {}
            for button_name, coords in button_dict.items():
                rect_dict[button_name] = self.make_rect(coords[0], coords[1], coords[2], coords[3])
            
            for rect in rect_dict.values():
                # Making hover effect on image rects using pygame surface overlay
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

    # Updates result from played game to history.csv
    def update_result(self, screen, game, win):
        user1 = game.player1.user_name
        user2 = game.player2.user_name

        if win == 1 or win == 2 or win == 0:
            pygame.display.flip()
            pygame.time.wait(1000)

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
    
    # Updates the board matrix with the latest move
    def make_move(self, move, code):
        i, j = move
        self.board.matrix[i][j] = code
        self.move_array.append(move)

    # Resets the game board
    def reset_game(self):
        self.board.matrix = np.zeros((self.board.width, self.board.height))
        self.move_array = []
        self.turn = 1

    # Reverts the last move
    def back_game(self):
        if self.move_array:
            i, j = self.move_array.pop()
            self.board.matrix[i][j] = 0
            self.switch_turn()

if __name__ == "__main__":
    # handle users
    user1 = sys.argv[1] 
    user2 = sys.argv[2]

    # Function used for running individual games
    def play_game(game_name, screen, flag=False):
        module_path = GAME_PATH[game_name]

        game_module = __import__(module_path, fromlist=['run'])

        command = game_module.run(user1, user2, screen, flag)

        return command
    
    # Drawing 
    def analysis_menu(screen):
        sort_command = 0
        if not pygame.get_init():
            pygame.init()
            screen = pygame.display.set_mode(screen_size)
            screen.blit(sort_img, (0, 0))
        pygame.display.set_caption("Sort Leaderboard")

        running = True
        while(running):
            clock = pygame.time.Clock()
            clock.tick(MAX_FPS)
            mouse = pygame.mouse.get_pos()
            screen.blit(sort_img, (0, 0))
            for rect in sort_rects:
                if rect.collidepoint(mouse):
                    hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    hover_surface.fill((0, 0, 0, 50))
                    screen.blit(hover_surface, rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = event.pos
                    for i in range(len(sort_rects)):
                        if sort_rects[i].collidepoint(mouse):
                            sort_command = sort_command + i
                            running = False
            pygame.display.flip()

        subprocess.run(["bash", "leaderboard.sh", str(sort_command)])
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
                if row[1] != "Draw":
                    player_data[row[2]][0] += 1
                    player_data[row[3]][1] += 1
        
        for data in player_data.values():
            if data[0] == 0 and data[1] == 0:
                continue
            data.append(data[0]/data[1] if data[1] != 0 else "INF")

        wins = sorted([(name, wins[0]) for name, wins in player_data.items()], reverse=True, key=lambda x: x[1])
        top_wins = wins[:5]

        w_l_ratio = []
        inf_val = 0
        for n_wins in player_data.values():
            if len(n_wins) <= 2:
                continue
            ratio = n_wins[2]
            if (ratio != "INF"):
                inf_val = max(ratio, inf_val)
        inf_val *= 2

        for name, n_wins in player_data.items():
            if len(n_wins) <= 2:
                continue
            w_l_ratio.append((name, (n_wins[2] if n_wins[2] != "INF" else inf_val)))
        w_l_ratio.sort(reverse=True, key=lambda x: x[1])

        top_w_l_ratio = w_l_ratio[:5]

        fig, axs = plt.subplots(2, 2, figsize = (12, 8))
        # Top 5 wins
        bars = axs[0][0].bar([data[0] for data in top_wins], [data[1] for data in top_wins])
        axs[0][0].bar_label(bars)
        axs[0][0].set_title("Top 5 Players (By win count)")

        # Top 5 W/L ratio
        bars = axs[0][1].bar([data[0] for data in top_w_l_ratio], [data[1] for data in top_w_l_ratio])
        labels = ["INF" if r[1] == inf_val else f"{r[1]:.2f}" for r in top_w_l_ratio]
        axs[0][1].bar_label(bars, labels=labels)
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

        bg_img = pygame.image.load("images/statistics.png")
        plot_img = pygame.image.load("plot.png")

        plot_rect = pygame.Rect(250, 205, 1038, 670)
        back_rect = pygame.Rect(249, 931, 243, 55)
        quit_rect = pygame.Rect(1048, 930, 236, 57)
        plot_img = pygame.transform.scale(plot_img, (plot_rect.width, plot_rect.height))

        running = True
        pygame.display.set_caption("Leaderboard")
        while(running):
            mouse = pygame.mouse.get_pos()
            screen.blit(bg_img, (0, 0))
            screen.blit(plot_img, plot_rect)
            for rect in back_rect, quit_rect:
                if rect.collidepoint(mouse):
                    hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    hover_surface.fill((0, 0, 0, 70))
                    screen.blit(hover_surface, rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cur_pos = event.pos
                    # print(cur_pos)
                    if back_rect.collidepoint(cur_pos):
                        return 1
                    if quit_rect.collidepoint(cur_pos):
                        return 0
            pygame.display.flip()
        return 1
        

    def game_loop(game_name, screen):
        # Return True --> Back to menu
        # Return False --> Quit
        flag = False
        while True:
            command = play_game(game_name, screen, flag)
            if command == 0: # quit
                return False
            elif command == 1: # play again
                flag = False
                continue
            elif command == 2: # show leaderboard
                action = analysis_menu(screen)
                if action == 0:
                    return False
                else:
                    # play_game runs again after this, which directly redirects to game over screen when flag = True
                    flag = True
                    continue

            elif command == 3: # back to menu
                return True
            else:
                return False # quit
            
    # Write name on a specified rectangle
    def write_name(screen,text,rect,font) :
        rendered_font = font.render(text, True, "#DCBE78")
        text_rect = rendered_font.get_rect()
        text_rect.center = rect.center
        screen.blit(rendered_font, text_rect)
        
    def start_menu():
        pygame.init()
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("GAME HUB")
        running = True
        #Font
        font = pygame.font.Font("./fonts/Cinzel-VariableFont_wght.ttf", 48)

        # Rects for holding player names
        player1_rect = pygame.Rect(322, 765, 280, 90)
        player2_rect = pygame.Rect(929, 765, 280, 90)

        # Menu background image
        menu_img = pygame.image.load("./images/Game_hub_menu.png")
        while running:
            clock = pygame.time.Clock()
            clock.tick(MAX_FPS)
            mouse = pygame.mouse.get_pos()

            screen.blit( menu_img ,(0,0))

            # Write player names
            write_name(screen,sys.argv[1].capitalize(),player1_rect,font)
            write_name(screen,sys.argv[2].capitalize(),player2_rect,font)

            # game buttons
            game_rect_list = {  "Tic-Tac-Toe" : pygame.Rect(120, 350, 350, 350),
                                "Othello"    : pygame.Rect(590, 320, 360, 360),
                                "Connect Four"    : pygame.Rect(1060, 320, 360, 360)}
            # quit button
            quit_rect = pygame.Rect(660, 920, 220, 63)
            for rect in *game_rect_list.values(), quit_rect:
                if rect.collidepoint(mouse):
                    # Add hover effect by adding overlay to surface
                    hover_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    hover_surface.fill((0, 0, 0, 45))
                    screen.blit(hover_surface, rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_rect.collidepoint(mouse):
                        running = False

                    for game_name in game_rect_list:
                        if game_rect_list[game_name].collidepoint(mouse):
                            while True:
                                e = pygame.event.wait()
                                if e.type == pygame.MOUSEBUTTONUP:
                                    break
                            running = game_loop(game_name, screen)
                            pygame.display.set_caption("GAME HUB")
            if not running:
                # Breaks when game_loop() returns False to quit
                break
            pygame.display.update()

    start_menu()
    pygame.quit()