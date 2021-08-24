from diceGame.diceGameOptimizer import optimizeDiceGame
from diceGame.output import generatePlot

import random
random.seed(42)
import numpy
numpy.random.seed(42)

EVO_DEFAULT = {"strategyRep": 0, "populationSize": 100, "chooseBest": 0.2, "changeRate": 1, 
"generations": 50, "iifitnessAgainst": "all"}

RL_DEFAULT = {"strategyRep": 0, "alpha": 0.9, "gamma": 0.5, "epsilon": 0.3, "epsilon_decay1": 0.999}


def main():
    evo_reps = []
    evo_kwargs = {"strategyRep": 0, "populationSize" : 100, "generations": 20}
    for i in range(4):
        evo_kwargs["strategyRep"] = i
        evo_reps.append(optimizeDiceGame(6, 3, "EVO", evo_kwargs))
    #print(rewards)
    generatePlot(evo_reps)



if __name__ == "__main__":
    main()
