from diceGameOptimizing.diceGameOptimizer import optimizeDiceGame
from diceGameOptimizing.output import generatePlot

import random
import numpy

EVO_DEFAULT = {"strategyRep": 0, "populationSize": 100, "chooseBest": 0.2, "changeRate": 1, 
"generations": 50, "fitnessAgainst": "all"}

RL_DEFAULT = {"strategyRep": 0, "defaultQValue": 0.5, "alpha": 0.9, "gamma": 0.5, 
"epsilon": 0.3, "epsilonDecay": 0.999, "timeSteps": 100}

PIPS = 6
SIDES = 3

def main():
    print(f"({PIPS=}, {SIDES=})")
    reps = []
    evo_kwargs = {"strategyRep": 0, "populationSize" : 100, "generations": 25, "fitnessAgainst": "all"}
    for i in range(0,4):
        random.seed(i)
        numpy.random.seed(i)
        evo_kwargs["strategyRep"] = i
        #reps.append(optimizeDiceGame(PIPS, SIDES, "EVO", evo_kwargs=evo_kwargs))

    
    rl_kwargs = {"defaultQValue": float(0.0) ,"alpha": 0.5, "gamma": 0.7, 
    "epsilon": 0.8, "epsilonDecay": 0.9995, "timeSteps": 1000, "rewardPointDensity": 0.4}
    end_epsilon = 0.01
    rl_kwargs["epsilonDecay"] = (end_epsilon/rl_kwargs["epsilon"])**(1.0/rl_kwargs["timeSteps"])
    
    random.seed(42)
    numpy.random.seed(42)
    reps.append(optimizeDiceGame(PIPS, SIDES, "RL", rl_kwargs=rl_kwargs, output = False))

    generatePlot(reps)

if __name__ == "__main__":
    main()
