import matplotlib.pyplot as plt

def generatePlot(testRuns: (str, list)):
	plt.xlabel("Generationen")
	plt.ylabel("Fitness")
	plt.title("Vergleich von Strategierepräsentationen mit evolutionärer Suche")
	#TODO: wenn mehrere mit **gleichem Namen**, dann als Wiederholungen sammeln und Varianz/Abweichung einzeichenen
	for name, rewards in testRuns:
		plt.plot(rewards[1:-1], label=name)
		print(name+":", str(rewards[-1]))
	plt.legend()
	plt.show()