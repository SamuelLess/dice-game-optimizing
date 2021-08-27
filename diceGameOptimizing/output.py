import matplotlib.pyplot as plt

def generatePlot(testRuns: (str, [(int, float)])):
	#print(testRuns)
	plt.xlabel("Ausgewertete Spiele")
	plt.ylabel("Fitness")
	#plt.gca().set_ylim([0.5,0.65])

	plt.title("Vergleich von Strategieoptimierungsalgorithmen")
	#TODO: wenn mehrere mit **gleichem Namen**, dann als Wiederholungen sammeln und Varianz/Abweichung einzeichenen
	for name, rewards in testRuns:
		x, y = zip(*rewards[1::])
		plt.plot(x, y, label=name, linewidth=1)
		print(f"{name}: {str(rewards[-1])} rewardPoints: {len(rewards)}")
	plt.legend()
	plt.show()