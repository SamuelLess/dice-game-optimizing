from diceGameOptimizing.diceGameOptimizer import optimizeDiceGame
from diceGameOptimizing.output import generatePlot

import random
import numpy

EVO_DEFAULT = {"strategyRep": 0, "populationSize": 100, "chooseBest": 0.2, "changeRate": 1, 
"generations": 50, "fitnessAgainst": "all"}

RL_DEFAULT = {"strategyRep": 0, "defaultQValue": 0.5, "alpha": 0.9, "gamma": 0.5, 
"epsilon": 0.3, "endEpsilon": 0.01, "epsilonDecay": None, "timeSteps": 100, "rewardPointDensity": 0.001}

PIPS = 6
SIDES = 3

runPerRepEvo = 2

runsRl = 10
    
evo_kwargs = {"strategyRep": 0, "populationSize" : 50, "generations": 50, 
    "fitnessAgainst": "all"}

rl_kwargs = {"defaultQValue": float(0.0) ,"alpha": 0.5, "gamma": 0.7, 
    "epsilon": 0.8, "endEpsilon": 0.01, "epsilonDecay": 0.9995, 
    "timeSteps": 70000, "rewardPointDensity": 0.0005}

playEvoReps = [0]

def main():
    print(f"({PIPS=}, {SIDES=})")
    reps = []
    for repNum in playEvoReps:
        evo_kwargs["strategyRep"] = repNum
        random.seed(repNum)
        numpy.random.seed(repNum)
        for _ in range(runPerRepEvo):
            reps.append(optimizeDiceGame(PIPS, SIDES, "EVO", evo_kwargs=evo_kwargs))

    for i in range(runsRl):
        random.seed(i)
        numpy.random.seed(i)
        reps.append(optimizeDiceGame(PIPS, SIDES, "RL", rl_kwargs=rl_kwargs, output = False))


    generatePlot(reps)

if __name__ == "__main__":
    main()
