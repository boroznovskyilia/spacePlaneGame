import pygame
import pygwidgets
import pyghelpers
import time
from pygame.locals import *
from Constants import *
from Player import *
from Meteorite import *
from Bullet import *

def showCustomYesNoDialog(theWindow,theText):
    oDialogBackground = pygwidgets.Image(theWindow, (212, 250),
                                            'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290),
                                            theText, width=WINDOW_WIDTH,
                                            justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(theWindow, (480, 370),
                                            'images/gotoHighScoresNormal.png',
                                            over='images/gotoHighScoresOver.png',
                                            down='images/gotoHighScoresDown.png',
                                            disabled='images/gotoHighScoresDisabled.png')

    oNoButton = pygwidgets.CustomButton(theWindow, (227, 370),
                                            'images/noThanksNormal.png',
                                            over='images/noThanksOver.png',
                                            down='images/noThanksDown.png',
                                            disabled='images/noThanksDisabled.png')

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                            oDialogBackground, oPromptDisplayText,
                                            oYesButton, oNoButton)
    return choiceAsBoolean

BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH,
                                WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'
TIMER_EVENT_ID = pygame.event.custom_type()
TIMER_LENGTH = 10
class ScenePlay(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.backgroundImage = pygwidgets.Image(self.window,(0,0),'images/background.png') 
        self.quitButton = pygwidgets.CustomButton(self.window,
                                        (30, GAME_HEIGHT + 90),
                                        up='images/quitNormal.png',
                                        down='images/quitDown.png',
                                        over='images/quitOver.png',
                                        disabled='images/quitDisabled.png')

        self.highScoresButton = pygwidgets.CustomButton(self.window,
                                        (190, GAME_HEIGHT + 90),
                                        up='images/gotoHighScoresNormal.png',
                                        down='images/gotoHighScoresDown.png',
                                        over='images/gotoHighScoresOver.png',
                                        disabled='images/gotoHighScoresDisabled.png')

        self.newGameButton = pygwidgets.CustomButton(self.window,
                                        (450, GAME_HEIGHT + 90),
                                        up='images/startNewNormal.png',
                                        down='images/startNewDown.png',
                                        over='images/startNewOver.png',
                                        disabled='images/startNewDisabled.png',
                                        enterToActivate=True)

        self.soundCheckBox = pygwidgets.TextCheckBox(self.window,
                                        (430, GAME_HEIGHT + 17),
                                        'Background music',
                                        True, textColor=WHITE)

        self.gameOverImage = pygwidgets.Image(self.window, (310, 180),
                                        'images/gameOver.png')

        self.titleText = pygwidgets.DisplayText(self.window,
                                        (70, GAME_HEIGHT + 17),
                                        'Score:                                 High Score:',
                                        fontSize=24, textColor=WHITE)

        self.scoreText = pygwidgets.DisplayText(self.window,
                                        (80, GAME_HEIGHT + 47), '0',
                                        fontSize=36, textColor=WHITE,
                                        justified='right')

        self.highScoreText = pygwidgets.DisplayText(self.window,
                                        (270, GAME_HEIGHT + 47), '',
                                        fontSize=36, textColor=WHITE,
                                        justified='right')
        
        pygame.mixer.music.load('sounds/background.mp3')
        self.shootSound = pygame.mixer.Sound('sounds/shoot.mp3')
        self.explosionSound = pygame.mixer.Sound('sounds/explosion.mp3')
        self.gameoverSound = pygame.mixer.Sound('sounds/gameover.mp3')
        self.levelUpSound = pygame.mixer.Sound('sounds/levelup.mp3')

        self.oPlayer = Player(self.window)
        self.oPlayer.update(self.oPlayer.maxX//2,self.oPlayer.maxY)
        self.oMeteoriteMgr = MeteoriteMgr(self.window)
        self.oBulletMgr = BullerMgr(self.window)

        self.level = 0

        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.backgroundMusic = True
        self.score = 0
        self.playingState = STATE_WAITING
        self.koefForTimer = 0.01
        self.timerStarted = time.time()
        self.addNewMeteorite = self.oMeteoriteMgr.getAddNewMeteorite()

    def getSceneKey(self):
        return SCENE_PLAY
    
    def enter(self,data):
        self.getHighAndLowScores()
    
    def getHighAndLowScores(self):
        infoDict = self.request(SCENE_HIGH_SCORES,HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict['lowest']

    def reset(self):
        self.score = 0
        self.koefForTimer = 0.001
        self.level = 0
        self.scoreText.setValue(self.score)
        self.getHighAndLowScores()

        self.oMeteoriteMgr.reset()
        self.oBulletMgr.reset()
        self.timerForLeveUp = pygame.time.set_timer(TIMER_EVENT_ID, int(TIMER_LENGTH * 1000),False)
        if self.backgroundMusic:
            pygame.mixer.music.play(-1,0.0)
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)

    def handleInputs(self, eventList, keyPressedList):
        if self.playingState == STATE_PLAYING:
            for event in eventList:
                if event.type == MOUSEBUTTONDOWN:
                    self.oBulletMgr.appendBullet(self.oPlayer.getLoc())
                    self.shootSound.play()
              
                if event.type == TIMER_EVENT_ID:
                    self.levelUpSound.play()
                    self.koefForTimer *= 2
                    self.level += 1
                    self.addNewMeteorite = self.oMeteoriteMgr.getAddNewMeteorite()
                    if(self.addNewMeteorite>0):
                        self.addNewMeteorite -= 1
                        self.oMeteoriteMgr.setAddNewMeteorite(self.addNewMeteorite)
                    
            return
        
        for event in eventList:
            self.startTimer = False
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING
                
            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)
            if self.quitButton.handleEvent(event):
                self.quit()
            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue()

            


    def update(self):
        if self.playingState != STATE_PLAYING:
            return
        
        keys = pygame.key.get_pressed() 
        x,y = self.oPlayer.getLoc()
        if keys[pygame.K_a]:
            x -= SPEED
        if keys[pygame.K_d]:
            x+=SPEED

        if(self.oMeteoriteMgr.hasPlayerHitMeteorite(self.oPlayer.update(x,y))):
            self.playingState = False
            self.startTimer = False
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            self.gameoverSound.play()
            pygame.time.delay(1200)
            self.playingState = STATE_GAME_OVER
            self.draw()
            self.score = int(self.score)
            if self.score > self.lowestHighScore:
                scoreString = 'Your score: ' + str(self.score) + '\n'
                if self.score > self.highestHighScore:
                    dialogText = (scoreString +
                                       'is a new high score, CONGRATULATIONS!')
                else:
                    dialogText = (scoreString +
                                      'gets you on the high scores list.')

                result = showCustomYesNoDialog(self.window, dialogText)
                if result: 
                    self.goToScene(SCENE_HIGH_SCORES, self.score)  
        
        self.elapsed = time.time() - self.timerStarted
        self.score = self.score + self.elapsed*self.koefForTimer
        self.score = self.score
        self.scoreText.setValue(int(self.score))
        oBulletList = self.oBulletMgr.getBulletList()
        oMeteoriteList = self.oMeteoriteMgr.getMeteoriteList()

        for oMeteorite in oMeteoriteList:
            for oBullet in oBulletList:
                if(oBullet.collideMeteorite(oMeteorite.getRect())):
                    oMeteorite.minusHP()
                    oBulletList.remove(oBullet)
                if(oMeteorite.getHP() == 0):
                    oMeteoriteList.remove(oMeteorite)
                    self.score += Meteorite.HP[oMeteorite.getMaxKoef() - oMeteorite.getKoef()]
                    self.explosionSound.play()
                    break
                    

        self.oBulletMgr.update()
        self.oPlayer.update(x,y)
        self.oMeteoriteMgr.update(self.level)
        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()

    def draw(self):
        self.window.fill((RANDOM_COLOR))
        self.backgroundImage.draw()
      
        self.oMeteoriteMgr.draw()
        self.oBulletMgr.draw()
        self.oPlayer.draw()
    
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()
        

        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def leave(self):
        pygame.mixer.music.stop()
