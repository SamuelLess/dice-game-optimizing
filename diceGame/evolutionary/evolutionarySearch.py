from diceGame.evolutionary.agent import Agent
from diceGame.evolutionary.strategy.stratList import StratList
from diceGame.evolutionary.strategy.stratVec import StratVec
from diceGame.evolutionary.strategy.stratVecComplete import StratVecComplete
from diceGame.evolutionary.strategy.stratVecDoubleLayer import StratVecDoubleLayer

from tqdm import tqdm

class EvolutionarySearch:
    def __init__(self, game, strategyRep=0, populationSize=100, chooseBest=0.2, 
            changeRate=1, generations=50, fitnessAgainst="all", output=False):
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
        self.fitnessAgainst = fitnessAgainst
        self.output = output
        self.population = []
        for i in range(self.populationSize):
            self.population.append(Agent(game, self.strategyHandler, 0, changeRate))

    def nextGeneration(self):
        for agent in self.population:
            agent.evaluateFitness(self.fitnessAgainst)
        #sort
        self.population.sort(key=lambda agent: agent.fitness,reverse=True)
        self.population = self.population[:int(self.populationSize*self.chooseBest)]
        #reproduce
        newPopulation = []
        for best in self.population:
            for i in range(int((1-self.chooseBest)/self.chooseBest)):
                #print(self.population)
                newPopulation.append(best.changedAgent())
        self.population.extend(newPopulation)

    def train(self):
        rewards = []
        for i in tqdm(range(self.generations)):
            rewards.append(self.population[0].fitness)
            self.nextGeneration()
        return rewards
