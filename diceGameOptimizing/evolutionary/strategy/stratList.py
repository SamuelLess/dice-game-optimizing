from itertools import repeat
import numpy as np
import statistics as stat
import random
from diceGameOptimizing.evolutionary.strategy.strat import StrategyAbstact

'''
Diese Klasse ist für die Strategiedarstellgung über Listen zuständig.
'''
class StratList(StrategyAbstact):
    def __init__(self, pips, sides):
        self.STATES = []
        self.pips = pips
        self.sides = sides
        self.createStates(0, 0)
        #bei p=s=3 sind es 14 Zustände

        #print("Mit " + str(self.pips) + " pips und " + str(self.sides) + " sides gibt es " + str(len(DICE)) + " Würfel (inkl. Permutationen) und " + str(len(STATES)) + " States.")

    def numOfState(self, state):
        """
        Für die den Index eines states in der STATES Liste.
    
        Zuständig: Paul

        Argumente: self, state (Liste)

        Return: Zahl
        """
        for i in range(len(self.STATES)):
            if(self.STATES[i]==state):
               return i
        #Kommt vor, wird aber nicht für Zugriff auf self.STATES verwendet.
        return -1#"Should not be used."

    def createStates(self, usedSides, state):
        """
        Erstellt alle states für die mit pips und sides in STATES Liste.

        Zuständig: Paul

        Argumente: self, 0, 0 (für rekursiven Aufruf)

        Return: nichts
        """
        if(0==usedSides):
            for i in range(self.pips+1):
                self.createStates(usedSides+1,[i])
        if(self.sides-1>usedSides and usedSides != 0):
            self.STATES.append(state)
            for i in range(self.pips+1-sum(state)):
                toAppend = state[:]
                toAppend.append(i)
                self.createStates(usedSides+1,toAppend)
        if(self.sides-1==usedSides):
            self.STATES.append(state)

    def randStrategyRecursive(self, usedSides, usedPips, strategy, strategy_usedPips, startingPlayer, alreadyUsedPips):
        """
        Erstellt eine zufällige legale Strategie

        Zuständig: Paul

        Argumente: 

        Return: zufällige Strategie
        """
        if(0==usedSides):
            for i in range(self.pips+1):
                if(startingPlayer==True):
                    strategy.append(alreadyUsedPips)
                    self.randStrategyRecursive(usedSides+1, i, strategy, alreadyUsedPips, False, 0)
                else:
                    add = random.randint(0,self.pips)
                    strategy.append(add)
                    self.randStrategyRecursive(usedSides+1, i, strategy, add,False,0)
        if(self.sides-1>usedSides and usedSides > 0):
            for i in range(self.pips+1-usedPips):
                add = random.randint(0,self.pips-strategy_usedPips)
                strategy.append(add)
                self.randStrategyRecursive(usedSides+1, usedPips+i, strategy, strategy_usedPips+add,False,0)
        return strategy

    def randomStrategy(self):# startingPlayer, alreadyUsedPips):
        """
        Ruft das Erstellen einer Random Strategie auf und gibt diese zurück.

        Zuständig: Paul

        Argumente: für den Fall das man eine Seite bereits gesetzt, startingPlayer=True, alreadyUsedPips = anzahl an auf die genutzte Seite gemalte Pips 

        Return: zufällige Strategie
        """
        return self.randStrategyRecursive(0,0,[],0,False, 0)

    def changedStrategy(self, strategy, changeRate):
        """
        Verändert eine gegebene Strategie

        Zuständig: Paul

        Argumente: zu verändernde Strategie

        Return: veränderte Strategie
        """
        stratSave = strategy[:]
        numberOfChanges = 0
        while True:
            strategy = stratSave[:]
            pointOfEdit = random.randint(0, len(strategy)-1)
            changedState = self.STATES[pointOfEdit]
            changedStateLen = len(changedState)
            #eigentliche zufällige Bearbeitung
            if(strategy[pointOfEdit]>0 and strategy[pointOfEdit]<self.pips):
                strategy[pointOfEdit] += (1 if random.randint(0,1) == 1 else -1)
            else:
                if(strategy[pointOfEdit]>0):
                    strategy[pointOfEdit]-=1
                elif(strategy[pointOfEdit]<self.pips):
                    strategy[pointOfEdit]+=1

            works = True
            for state in self.STATES:
                if(len(state) == self.sides-1 and changedState == state[0:changedStateLen]):
                    #wenn abhängig von der Veränderung
                    if(self.traceState(self.numOfState(state), strategy) != True):
                        works = False
            if(works == True):
                numberOfChanges+=1
            if(numberOfChanges >= changeRate):
                break
        return strategy
                         

    def traceState(self, stateNum, strategy):
        """
        Schauf ob eine Strategie, die an einer bestimmten Stelle bearbeitet wurde legal ist.
        
        Zuständig: Samuel

        Argumente: postition der Veränderung, veränderte Strategie

        Return: ob Legale Änderung
        """
        sum = 0
        for i in range(1,self.sides-1):
            sum += strategy[stateNum]
            stateNum = self.numOfState(self.STATES[stateNum][0:-i])
        return (sum <= self.pips)



    def nextMove(self, opponentsMoves, strategy):
        return strategy[self.numOfState(opponentsMoves)]