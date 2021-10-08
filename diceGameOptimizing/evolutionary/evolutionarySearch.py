from diceGameOptimizing.evolutionary.agent import Agent
from diceGameOptimizing.evolutionary.strategy.stratList import StratList
from diceGameOptimizing.evolutionary.strategy.stratVec import StratVec
from diceGameOptimizing.evolutionary.strategy.stratVecComplete import StratVecComplete
from diceGameOptimizing.evolutionary.strategy.stratVecDoubleLayer import StratVecDoubleLayer

from tqdm import tqdm

class EvolutionarySearch:
    def __init__(self, game, strategyRep=0, populationSize=100, chooseBest=0.2, 
            changeRate=1, generations=50, gamesToPlay=None, fitnessAgainst="all", output=False):
        """
        Implementiert den Evolutionären Algorithmus.
        Lässt sich durch die `train()` Methode ausführen.

        Parameters
        ---------
        game : Game
            Environment, das optimiert wird.
        strategyRep : int
            Art der Strategiedarstellung. 
            0 -> Liste; 1 -> Vektor; 2 -> Vektor; 3 -> NeuronalesNetz
        populationSize : int
            Populationsgröße.
        chooseBest : float
            Anteil der Population, auf dem die Mutationen für die nächste Generation basieren.
        changeRate : float
            Wert, wie stark die Agenten verändert werden. (Änderungsrate)
        generations : int
            Anzahl der Generationen, über die trainiert wird.
        gamesToPlay : int
            Anzahl der Spiele, die zum Training gespielt werden dürfen.
        fitnessAgainst : int | str
            Spezifiziert die Fitnessbestimmung. (s. Agent)
        
        .. note::
            Wenn `gamesToPlay` nicht `None` ist wird für die Anzahl der Spiele trainiert. 
            Ansonsten nach Anzahl der Generationen.
        """
        self.game = game
        if strategyRep == 0:
            self.strategyHandler = StratList(game.pips, game.sides)
        elif strategyRep == 1:
            self.strategyHandler = StratVec(game.pips, game.sides)
        elif strategyRep == 2:
            self.strategyHandler = StratVecComplete(game.pips, game.sides)
        elif strategyRep == 3:
            self.strategyHandler = StratVecDoubleLayer(game.pips, game.sides)
        else: 
            print("ERROR: No valid strategyRep chosen!")
        self.populationSize = populationSize
        self.chooseBest = chooseBest
        self.changeRate = changeRate
        self.generations = generations
        self.gamesToPlay = gamesToPlay
        self.fitnessAgainst = fitnessAgainst
        self.output = output
        self.population = []
        for i in range(self.populationSize):
            self.population.append(Agent(game, self.strategyHandler, 0, changeRate))

    def nextGeneration(self):
        """
        Erstellt die nächste Generation an Agenten.

            - Von allen Agenten die Fitness bestimmen.
            - Die Agenten anhand ihrer Fitness sortieren.
            - Die besten `chooseBest` auswählen.
            - Fortpflanezen und mit leichten Veränderungen in die nächste Generation.
        """
        #agenten auswerten
        for agent in self.population:
            agent.evaluateFitness(self.fitnessAgainst)
        #sort
        self.population.sort(key=lambda agent: agent.fitness,reverse=True)
        self.population = self.population[:int(self.populationSize*self.chooseBest)]
        #reproduce
        newPopulation = []
        for best in self.population:
            for i in range(int((1-self.chooseBest)/self.chooseBest)):
                newPopulation.append(best.changedAgent())
        self.population.extend(newPopulation)

    def train(self):
        """
        Führt den Trainingszyklus aus.

        Returns
        ---------
        rewardPoints : [(int, float)] Punkte (insgesamt gespielte Spiele, erreichte Auszahlung)
        """
        rewardPoints = []
        if self.gamesToPlay != None:
            while self.game.gamesPlayed < self.gamesToPlay:
                self.population[0].evaluateFitness("all", invisibleGame=True)
                rewardPoints.append((self.game.gamesPlayed, self.population[0].fitness))
                print(f"Gespielte Spiele: {self.game.gamesPlayed} max reward: {rewardPoints[-1][1]}", end="\r")
                self.nextGeneration()
        else:
            for i in tqdm(range(generations)):
                self.population[0].evaluateFitness("all", invisibleGame=True)
                rewardPoints.append((self.game.gamesPlayed, self.population[0].fitness))
                print(f"Gespielte Spiele: {self.game.gamesPlayed} max reward: {rewardPoints[-1][1]}", end="\r")
                self.nextGeneration()

        return rewardPoints