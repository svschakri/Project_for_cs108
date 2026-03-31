import pygame 
import numpy as np 
import matplotlib
import pathlib
import sys
import os 
import time


username1 = sys.argv[1] 
username2 = sys.argv[2]


def Choose_Character():
    pass

pygame.init()
screen=pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running=True

i=1
a=1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False


    screen.fill((i%256,0,(255-i)%256))
    
    
    if  i==255 :
        a=-1
    elif i==0: 
        a=1
    i+=a


    pygame.display.flip()

    clock.tick(60)

pygame.quit()