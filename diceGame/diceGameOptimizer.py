from diceGame.diceGame import Game
from diceGame.evolutionary.evolutionarySearch import EvolutionarySearch
#   from diceGame.reinforcement.reinforcementLearning import ReinforcementLearning

def optimizeDiceGame(pips, sides, optimizerType, evo_kwargs=None, rl_kwargs=None, output=False):
    """
    pips, sides: p, s
    
    optimizeType: str mit "RL" oder "EVO"
    
    
    
    """
    rewards = 0
    game = Game(pips, sides)
    name = "nameOfGraph"
    if optimizerType == "EVO":
        evo = EvolutionarySearch(game, **evo_kwargs, output=output)
        rewards = evo.train()
        name = "EVO_" + str(evo_kwargs.get("strategyRep", "0"))

    return (name, rewards)