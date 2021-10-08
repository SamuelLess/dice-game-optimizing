from diceGameOptimizing.diceGame import Game
from diceGameOptimizing.evolutionary.evolutionarySearch import EvolutionarySearch
from diceGameOptimizing.reinforcement.reinforcementLearning import ReinforcementLearning

def optimizeDiceGame(pips, sides, optimizerType, newname=None, evo_kwargs=None, rl_kwargs=None, output=False):
    """
    pips, sides: p, s
    
    optimizeType: str mit "RL" oder "EVO"
    
    
    
    """
    rewards = 0
    name = "nameOfGraph"
    if optimizerType == "EVO":
        evo = EvolutionarySearch(Game(pips, sides), **evo_kwargs, output=output)
        rewardPoints = evo.train()
        name = newname if newname is not None else optimizerType

    if optimizerType == "RL":
        rl = ReinforcementLearning(Game(pips, sides), **rl_kwargs, output=output)
        rewardPoints = rl.train()
        name = newname if newname is not None else optimizerType
        #name = ("RL_" + "dqv" + str(rl_kwargs["defaultQValue"]) + "α" + str(rl_kwargs["alpha"]) +
        #    "_γ" + str(rl_kwargs["gamma"]) + "_ε" + str(rl_kwargs["epsilon"]))

    return (name, rewardPoints)