import pygwidgets
import pyghelpers
from Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self,window):
        self.window = window
        self.backgroundImage = pygwidgets.Image(self.window,(0,0),'images/background.png') 
        self.textRulesHeader = pygwidgets.DisplayText(self.window,(180,100),
                                                      fontName = None,fontSize=60,textColor = RANDOM_COLOR)
        self.textRulesHeader.setValue("Rules Of the Game")
        self.textOfRules = pygwidgets.DisplayText(self.window,(50,250),fontSize=30,textColor = WHITE)
        self.textOfRules.setValue("You are a spaceship.Your mission is destroing meteorites and survive.\nYou are given points for destroying meteorites and duration of your space journey.\nGood luck!")
        self.startButton = pygwidgets.CustomButton(self.window, (400, 550),
                                                up='images/startNormal.png',
                                                down='images/startDown.png',
                                                over='images/startOver.png',
                                                disabled='images/startDisabled.png',
                                                enterToActivate=True)

        self.quitButton = pygwidgets.CustomButton(self.window, (100, 550),
                                                up='images/quitNormal.png',
                                                down='images/quitDown.png',
                                                over='images/quitOver.png',
                                                disabled='images/quitDisabled.png')

        self.highScoresButton = pygwidgets.CustomButton(self.window, (700, 550),
                                                up='images/gotoHighScoresNormal.png',
                                                down='images/gotoHighScoresDown.png',
                                                over='images/gotoHighScoresOver.png',
                                                disabled='images/gotoHighScoresDisabled.png')
        
    def getSceneKey(self):
        return SCENE_SPLASH
    
    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self.quitButton.handleEvent(event):
                self.quit()     
            # elif self.highScoresButton.handleEvent(event):
            #     self.goToScene(SCENE_HIGH_SCORES)
    
    def draw(self):
        self.backgroundImage.draw()
        self.textRulesHeader.draw()
        self.textOfRules.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        

if __name__ == '__main__':
    import pygame
    import sys
    from pygame.locals import *
    FRAMES_PER_SECOND = 30
    clock = pygame.time.Clock()
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    oSceneSplash = SceneSplash(window)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        oSceneSplash.draw()
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)



