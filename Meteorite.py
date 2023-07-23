import pygame
import pygwidgets
import random
from pygame.locals import *
from Constants import *

class Meteorite():
    BASE_SPEED = 1
    SIZE = [50,100,200]
    SPEED_KOEF = [10,5,2]
    HP = [1,2,3]
    METEORITE_IMAGE = pygame.image.load('images/meteorite.png')
    def __init__(self,window,level = 0):
        self.window = window
        self.koef = random.randrange(0,3)
        self.speed = (Meteorite.BASE_SPEED + level)*Meteorite.SPEED_KOEF[self.koef]
        self.size = Meteorite.SIZE[self.koef]
        self.hp = Meteorite.HP[self.koef]
        self.x = random.randrange(0,WINDOW_WIDTH-self.size)
        self.y = 0 - self.size
        self.image = pygwidgets.Image(self.window,(self.x,self.y),Meteorite.METEORITE_IMAGE)
        self.image.scale(self.size,False)
        self.maxKoef = len(Meteorite.SIZE) - 1

    def update(self,level = 0):
        self.y += self.speed
        self.image.setLoc((self.x,self.y))
        if self.y > GAME_HEIGHT:
            return True
        else:
            return False
        
    def getRect(self):
        return self.image.getRect()
    
    def getHP(self):
        return self.hp
    
    def getKoef(self):
        return self.koef
    
    def getMaxKoef(self):
        return self.maxKoef
    
    def minusHP(self):
        self.hp = self.hp - 1

    def draw(self):
        return self.image.draw()
    
    def collidePlayer(self,playerRect):
        collideWithPlayer = self.image.overlaps(playerRect)
        return collideWithPlayer
    
    # def collideBullet(self,bulletRect):
    #     collideWithBullet = self.image.overlaps(bulletRect)
    #     return collideWithBullet
    
class MeteoriteMgr():
    ADD_NEW_METEORITES = 20
    def __init__(self,window):
        self.window = window
        self.reset()

    def reset(self):
        self.meteoriteList = []
        self.nFramesTimeTilNextMeteorites = MeteoriteMgr.ADD_NEW_METEORITES
    
    def update(self,level = 0):
        nMeteoritesRemove = 0
        meteoriteListCopy = self.meteoriteList.copy()
        for oMeteorite in meteoriteListCopy:
            deleteMe = oMeteorite.update(level)
            if deleteMe:
                self.meteoriteList.remove(oMeteorite)
                nMeteoritesRemove += 1
        self.nFramesTimeTilNextMeteorites -= 1
        if self.nFramesTimeTilNextMeteorites == 0:
            oMeteorite = Meteorite(self.window,level)
            self.meteoriteList.append(oMeteorite)
            self.nFramesTimeTilNextMeteorites = MeteoriteMgr.ADD_NEW_METEORITES

        return nMeteoritesRemove
    
    def getMeteoriteList(self):
        return self.meteoriteList
    
    def draw(self):
        for oMeteorite in self.meteoriteList:
            oMeteorite.draw()

    def hasPlayerHitMeteorite(self,playerRect):
        for oMeteorite in self.meteoriteList:
            if oMeteorite.collidePlayer(playerRect):
                return True
        return False
    
    # def hasBulletHitMeteorite(self,bulletRect):
    #     for oMeteorite in self.meteoriteList:
    #         if oMeteorite in self.meteoriteList:
    #             if oMeteorite.collideBulle(bulletRect):
    #                 self.meteoriteList.remove(oMeteorite)
    #                 return True
    #     return False
