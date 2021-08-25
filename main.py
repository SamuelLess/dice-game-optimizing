from diceGame.diceGameOptimizer import optimizeDiceGame
from diceGame.output import generatePlot

import random
import numpy

EVO_DEFAULT = {"strategyRep": 0, "populationSize": 100, "chooseBest": 0.2, "changeRate": 1, 
"generations": 50, "fitnessAgainst": "all"}

RL_DEFAULT = {"strategyRep": 0, "alpha": 0.9, "gamma": 0.5, "epsilon": 0.3, "epsilonDecay": 0.999}


def main():
    evo_reps = []
    evo_kwargs = {"strategyRep": 0, "populationSize" : 200, "generations": 50, "fitnessAgainst": 0.8}
    for i in range(0,4):
        random.seed(i)
        numpy.random.seed(i)
        evo_kwargs["strategyRep"] = i
        evo_reps.append(optimizeDiceGame(6, 3, "EVO", evo_kwargs))
    #print(rewards)
    generatePlot(evo_reps)

        



if __name__ == "__main__":
    main()
