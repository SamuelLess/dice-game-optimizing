from diceGameOptimizing.diceGameOptimizer import optimizeDiceGame
from diceGameOptimizing.output import generatePlot

import random
import numpy

EVO_DEFAULT = {"strategyRep": 0, "populationSize": 100, "chooseBest": 0.2, "changeRate": 1, 
"generations": 50, "fitnessAgainst": "all"}

RL_DEFAULT = {"strategyRep": 0, "defaultQValue": 0.5, "alpha": 0.9, "gamma": 0.5, 
"epsilon": 0.3, "endEpsilon": 0.01, "epsilonDecay": None, "timeSteps": 100, "rewardPointDensity": 0.001}

#hier lässt sich das Spiel festlegen
PIPS = 6
SIDES = 3

#hier lässt sich festlegen, welche methode wie oft getestet werden sollen
playEvoReps = [0, 1, 2, 3]
#playEvoReps = [3]
runPerRepEvo = 10

runsRl = 10


#hier lassen sich die Argumente für die Testdurchläufe konfigurieren
evo_kwargs = {"strategyRep": 0, "populationSize" : 20, 
    "generations": 500, "gamesToPlay": 70000, "fitnessAgainst": "all"}

rl_kwargs = {"defaultQValue": 0.3 ,"alpha": 0.5, "endAlpha":0.001, "gamma": 1, 
    "epsilon": 0.8, "endEpsilon": 0.1, "epsilonDecay": 0.9995, 
    "timeSteps": 70000, "rewardPointDensity": 0.001}

EVONAMES = {0: "Liste", 1: "Vektor1", 2: "Vektor2", 3: "NN"}

def main():
    print(f"({PIPS=}, {SIDES=})")
    reps = []
    for repNum in playEvoReps:
        evo_kwargs["strategyRep"] = repNum
        random.seed(repNum)
        numpy.random.seed(repNum)
        for i in range(runPerRepEvo):
            print(i,"von",runPerRepEvo)
            print()
            reps.append(optimizeDiceGame(PIPS, SIDES, "EVO", newname=f"Evo_{EVONAMES[repNum]}", evo_kwargs=evo_kwargs))

    for i in range(runsRl):
        random.seed(i)
        numpy.random.seed(i)
        #rl_kwargs['defaultQValue'] += 0.1
        reps.append(optimizeDiceGame(PIPS, SIDES, "RL", rl_kwargs=rl_kwargs, output = False))

    generatePlot(reps)

if __name__ == "__main__":
    main()