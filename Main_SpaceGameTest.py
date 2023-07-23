from Player import *
from Meteorite import *
from Bullet import *
from pygame.locals import *
from pygame import mixer
import sys

FRAMES_PER_SECOND = 40
SPEED = 10
clock = pygame.time.Clock()

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

oPlayer = Player(window)
oMeteoriteMgr = MeteoriteMgr(window)
oBulletMgr = BullerMgr(window)

background = pygame.image.load('images/background.png')
mixer.init()
mixer.music.load('sounds/background.mp3')
mixer.music.play(-1)
shootSound = pygame.mixer.Sound('sounds/shoot.mp3')
explosionSound = pygame.mixer.Sound('sounds/explosion.mp3')
gameoverSound = pygame.mixer.Sound('sounds/gameover.mp3')
oPlayer.update(oPlayer.maxX//2,oPlayer.maxY)
while True:
    # pygame.mixer.music.load('sounds/background.mid')
    found = False
    window.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            oBulletMgr.appendBullet(oPlayer.getLoc())
            shootSound.play()
            
    keys = pygame.key.get_pressed() 
    x,y = oPlayer.getLoc()
    if keys[pygame.K_a]:
        x -= SPEED
    if keys[pygame.K_d]:
        x+=SPEED
    if(oMeteoriteMgr.hasPlayerHitMeteorite(oPlayer.update(x,y))):
        pygame.mixer.music.stop()
        gameoverSound.play()
        pygame.time.delay(1200)
        pygame.quit()
        sys.exit()
    oBulletList = oBulletMgr.getBulletList()
    oMeteoriteList = oMeteoriteMgr.getMeteoriteList()
    for oBullet in oBulletList:
        for oMeteorite in oMeteoriteList:
            if(oBullet.collideMeteorite(oMeteorite.getRect())):
                oMeteorite.minusHP()
                oBulletList.remove(oBullet)            
            if(oMeteorite.getHP() == 0):
                oMeteoriteList.remove(oMeteorite)
                explosionSound.play()
       
    oBulletMgr.update()
    oMeteoriteMgr.update()
    oPlayer.update(x,y)
    oMeteoriteMgr.draw()
    oBulletMgr.draw()
    oPlayer.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)




