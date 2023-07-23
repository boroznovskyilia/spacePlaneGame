import pygame
import pygwidgets
import random
from pygame.locals import *
from Constants import *

class Bullet():
    SPEED =  13
    
    def __init__(self,window,PlayerLoc):
        self.window = window
        self.speed = Bullet.SPEED
        self.image = pygwidgets.Image(self.window,(-100,-100),'images/bullet.png')
        self.x,self.y = PlayerLoc

    def getRect(self):
        return self.image.getRect()
    
    def update(self):
        self.y -= self.speed
        self.image.setLoc((self.x,self.y)) 
        if self.y < 0:
            return True
        else:
            return False

    def draw(self):
        return self.image.draw()
    
    def collideMeteorite(self,meteoriteRect):
        collideWithMeteorite = self.image.overlaps(meteoriteRect)
        return collideWithMeteorite
    

    
class BullerMgr():
    def __init__(self,window):
        self.window = window
        self.reset()
    
    def reset(self):
        self.bulletList = []
    
    def update(self):
        bulletListCopy = self.bulletList.copy()
        for oBullet in bulletListCopy:
            deleteMe = oBullet.update()
            if deleteMe: #or self.hasBulletHitMeteorite(meteoriteRect):
                self.bulletList.remove(oBullet)

    def getBulletList(self):
        return self.bulletList
    
    def appendBullet(self,oPlayerLoc):
        oBullet = Bullet(self.window,oPlayerLoc)
        self.bulletList.append(oBullet)

    
    def draw(self):
        for oBullet in self.bulletList:
            oBullet.draw()

    # def hasBulletHitMeteorite(self,meteoriteRect):
    #     for oBullet in self.bulletList:
    #         if oBullet.collideMeteorite(meteoriteRect):
    #             return True
    #     return False

    