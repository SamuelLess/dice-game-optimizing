from diceGameOptimizing.diceGame import Game
from diceGameOptimizing.evolutionary.evolutionarySearch import EvolutionarySearch
from diceGameOptimizing.reinforcement.reinforcementLearning import ReinforcementLearning

def optimizeDiceGame(pips, sides, optimizerType, newname=None, evo_kwargs=None, rl_kwargs=None, output=False):
    """
    Hauptfunktion, die je nach Parametern eine Strategie optimiert.
    
    Parameters
    ---------
    pips : int
        Augenanzahl für das Spiel.
    sides : int
        Seitenanzahl für das Spiel.
    optimizerType : str
        Legt Algorithmustyp fest; Entweder "EVO" oder "RL".
    newname : str
        Name für das Diagramm.
    evo_kwargs : dict
        Parameter für EVO.
    rl_kwargs : dict
        Parameter für RL
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