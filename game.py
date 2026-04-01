import pygame
import numpy as np 
import matplotlib
import pathlib
import sys
import os 
import time
import abc

USER1 = sys.argv[1] 
USER2 = sys.argv[2]

TURN = 0

class Player:
    def __init__(self, user_name, turn):
        self.user_name = user_name
        self.turn = TURN
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width , height))

class Game():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def switch_turn(self):
        self.player1.turn = 1 - self.player1.turn
        self.player2.turn = 1 - self.player2.turn

    @abc.abstractmethod
    def check_win(self):
        """ This would be used to check win condition """
        return
    