import random as rand

class Game:
    """
    Diese Klasse implementiert das Würfelspiel, für welches Strategien optimiert werden sollen.
    Jede Interaktion mit dem Würfelspiel läuft über eine Intstanz dieser Klasse.
    """
    def __init__(self, pips, sides, rewardDraw=0.5):
        """
        Erstellt eine Instanz des Würfelspiels (pips, sides).
        Durch den Parameter rewardDraw lässt sich die Auszahlung bei einem Unentschieden ändern.

        Return: None
        """
        self.pips = pips
        self.sides = sides
        self.DICE =[]
        self.generateDice(0,[])
        self.gameDice = []
        self.agentDice = []
        self.atTurn = 0
        self.atDice = 0
        self.gamesPlayed = 0
        self.rewardDraw = rewardDraw

    def start(self, playInOrder=False, invisibleGame=False):
        """
        Startet ein zufälliges Spiel, außer wenn playInOrder True ist.
        In diesem Fall werden alle möglichen Würfel (inkl. Permutationen) nacheinander gespielt.

        Return: Liste mit erstem Spielzug.
        """
        if not invisibleGame:
            self.gamesPlayed += 1
        self.agentDice = []
        self.gameDice = self.DICE[rand.randint(0,len(self.DICE)-1)]
        if self.atDice == len(self.DICE):
            self.atDice = 0
        if playInOrder:
            self.gameDice = self.DICE[self.atDice]
            #print("playInOrder at", str(self.atDice), "with", str(self.gameDice))
            self.atDice += 1
        self.atTurn = 0
        #print(self.gameDice, playInOrder)
        return self.gameDice[0:self.atTurn+1]

    def finished(self):
        """
        Gibt an, ob ein angefangenes Spiel beendet wurde.
        Sollte nicht ohne gestartetes Spiel aufgerufen werden.

        Return: bool
        """
        return self.atTurn >= self.sides-1 or self.illegal()

    def illegal(self):
        """
        Hilfsfunktion.
        """
        return sum(self.agentDice) > self.pips or (self.agentDice[-1] if len(self.agentDice) > 0 else 0) < 0

    def takeAction(self, action: int, output = False):
        """
        Spielt ein bereits gestartetes Spiel weiter.
        Gibt den bisher sichtbaren Würfel des Gegeners 
        und die in diesem Zug erreichte Auszahlung zurück.
        
        Return: oppDice, reward
        """
        self.atTurn+=1#wie vieltes mal agent spielt
        self.agentDice.append(action)
        reward = 0

        if self.atTurn == self.sides-1:
            self.agentDice.append(self.pips-sum(self.agentDice))
            self.atTurn+=1
            reward = self.reward(output = output)

        if self.illegal():
            reward = -10
        return self.gameDice[0:self.atTurn+1], reward
    
    def reward(self, output = False):
        """
        Berechnet unter Beachtung des Wertes "rewardDraw" die Auszahlung 
        eines abgeschlossenen legalen Spiels für den Spieler.

        Return: reward: int
        """
        wp1 = 0
        for p1 in self.agentDice:
            for p2 in self.gameDice:
                if(p1>p2):
                    wp1+=1
                elif(p1==p2):
                    wp1+=self.rewardDraw
        if output:
            print(self.gameDice, "vs", self.agentDice, (wp1/(self.sides**2)))
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