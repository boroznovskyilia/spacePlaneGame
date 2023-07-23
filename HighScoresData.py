from Constants import *
from pathlib import Path
import json

class HighScoresData():
    def __init__(self):
        self.BLANK_SCORES_LIST = N_HIGH_SCORES * [['-----', 0]]
        self.oFilePath = Path('HighScores.json')
        
        try:
            data = self.oFilePath.read_text()
        except FileNotFoundError:  
            self.resetScores()
            return

      
        self.scoresList = json.loads(data)

    def addHighScore(self, name, newHighScore):
       
        placeFound = False
        for index, nameScoreList in enumerate(self.scoresList):
            thisScore = nameScoreList[1]
            if newHighScore > thisScore:
               
                self.scoresList.insert(index, [name, newHighScore])
                self.scoresList.pop(N_HIGH_SCORES)
                placeFound = True
                break
        if not placeFound:
            return 

     
        self.saveScores()

    def saveScores(self):
        scoresAsJson = json.dumps(self.scoresList)
        self.oFilePath.write_text(scoresAsJson)

    def resetScores(self):
        self.scoresList = self.BLANK_SCORES_LIST.copy()
        self.saveScores()

    def getScoresAndNames(self):
        namesList = []
        scoresList = []
        for nameAndScore in self.scoresList:
            thisName = nameAndScore[0]
            thisScore = nameAndScore[1]
            namesList.append(thisName)
            scoresList.append(thisScore)

        return scoresList, namesList

    def getHighestAndLowest(self):
       
        highestEntry = self.scoresList[0]
        lowestEntry = self.scoresList[-1]
      
        highestScore = highestEntry[1]
        lowestScore = lowestEntry[1]
        return highestScore, lowestScore

