import pygame
import pygwidgets
from Constants import *

class Player():

    def __init__(self,window):
        self.window = window
        self.image = pygwidgets.Image(window,(-100,-100),'images/spaceship.png')
        playerRect = self.image.getRect()
        self.maxX = WINDOW_WIDTH - playerRect.width
        self.maxY = GAME_HEIGHT - playerRect.height

    def update(self,x,y):
        if x < 0:
            x = 0
        elif x >= self.maxX:
            x = self.maxX
        
        self.image.setLoc((x,y))
        return self.image.getRect()
    
    def draw(self):
        self.image.draw()
    
    def getLoc(self):
        return self.image.getLoc()

