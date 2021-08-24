import random as rand

class Game:
    def __init__(self, pips, sides, rewardDraw=0.5):
        self.pips = pips
        self.sides = sides
        self.DICE =[]
        self.generateDice(0,[])
        self.gameDice = []
        self.agentDice = []
        self.atTurn = 0
        self.atDice = 0
        self.rewardDraw = rewardDraw

    def start(self, playInOrder=False):
        """
        Startet ein zufälliges Spiel. 
        Wenn inorder == true, dann alle einmal nacheinander.

        Return: liste mit erstem Zug
        """
        self.agentDice = []
        self.gameDice = self.DICE[rand.randint(0,len(self.DICE)-1)]
        if self.atDice == len(self.DICE):
            self.atDice = 0
        if playInOrder:
            self.gameDice = self.DICE[self.atDice]
            self.atDice += 1

        self.atTurn = 0
        return self.gameDice[0:self.atTurn+1]

    def finished(self):
        return self.atTurn >= self.sides-1 or self.illegal()

    def illegal(self):
        return sum(self.agentDice) > self.pips or (self.agentDice[-1] if len(self.agentDice) > 0 else 0) < 0

    def takeAction(self, action):
        """
        Spielt ein bereits gestartetes Spiel weiter.
        Gibt oppDice und reward.
        
        Return: oppDice, reward
        """
        self.atTurn+=1#wie vieltes mal agent spielt
        self.agentDice.append(action)
        reward = 0

        if self.atTurn == self.sides-1:
            self.agentDice.append(self.pips-sum(self.agentDice))
            self.atTurn+=1
            reward = self.reward()

        if self.illegal():
            reward = -10
        return self.gameDice[0:self.atTurn+1], reward
    
    def reward(self):
        """
        print("->inreward")
        print("gameDice", self.gameDice)
        """
        wp1 = 0
        wp2 = 0
        for p1 in self.agentDice:
            for p2 in self.gameDice:
                if(p1>p2):
                    wp1+=1
                if(p1<p2):
                    wp2+=1
                if(p1==p2):
                    wp1+=self.rewardDraw
                    wp2+=self.rewardDraw
        return wp1/(self.sides*self.sides)

    def generateDice(self, usedSides, dice):
        """
        Generiert alle möglichen Würfel inklusive Permutationen in DICE.
        """ 
        if(usedSides == 0):
            for i in range(self.pips+1):    
                self.generateDice(usedSides+1,[i])
        if(self.sides-1>usedSides and usedSides != 0):
            for i in range(self.pips+1-sum(dice)):
                toAppend = dice[:]
                toAppend.append(i)
                self.generateDice(usedSides+1,toAppend)
        if(self.sides-1==usedSides):
            dice.append(self.pips-sum(dice))
            self.DICE.append(dice)