# Vergleich von Strategieoptimierungsalgorithmen für ein Würfelspiel 🧊

## Zielstellung
Das Ziel ist es, verschiedene Optimierungsalgorithmen zu vergleichen und schöne Diagramme zu erstellen. :octocat:

## Programm-Struktur
```
main.py

diceGameOptimizing/diceGame.py -> einheitliches Environment für das alle Algorithmen optimieren
diceGameOptimizing/diceGameOptimizer -> Handler für alles, je nach kwargs des Aufrufs
diceGameOptimizing/output.py -> einheitliche Ausgabe in Form von Diagrammen

diceGameOptimizing/evolutionary/evolutionarySearch.py
diceGameOptimizing/evolutionary/agent.py
diceGameOptimizing/evolutionary/strat/...

diceGameOptimizing/reinforcement/reinforcementLearning.py
diceGameOptimizing/reinforcement/agent.py
diceGameOptimizing/reinforcement/strat/...
```
