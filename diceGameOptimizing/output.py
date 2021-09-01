import matplotlib.pyplot as plt

def generatePlot(testRuns: (str, [(int, float)])):
	#print(testRuns)

	names = {run[0] for run in testRuns}

	nameAssignedRewards = {}
	for name, rewards in testRuns:
		nameAssignedRewards.setdefault(name, []).append(rewards[1::])
	
	combinedRuns = {name: evalSameNameTestRuns(nameAssignedRewards[name]) 
					for name in names}
	
	plt.xlabel("Ausgewertete Spiele")
	plt.ylabel("Fitness")
	#plt.gca().set_ylim([0.5,0.65])
	for name in names:
		meanRewardPoints = combinedRuns[name]["mean"]
		x, ymean = zip(*meanRewardPoints)
		plt.plot(x, ymean, label=name, linewidth=1)
		plt.fill_between(x, combinedRuns[name]["min"], 
							combinedRuns[name]["max"], alpha=0.5)
		print(f"{name}: {str(rewards[-1])} rewardPoints: {len(rewards)} * {len(nameAssignedRewards[name])}")
	
	plt.legend()
	plt.show()

def evalSameNameTestRuns(testRunRewardPoints: [(str, float)]):
	rewardPoints = {"mean": None, "min": None, "max": None}
	rewardPoints["mean"] = meanlists(testRunRewardPoints)
	rewardPoints["min"] = varlists(testRunRewardPoints, False)
	rewardPoints["max"] = varlists(testRunRewardPoints, True)
	return rewardPoints

def varlists(lists, add):
	var = []
	for row in zip(*lists):
		rowVals = [item[1] for item in row]
		mean = sum(rowVals)/len(rowVals)
		avDelta = sum([abs(mean-rew) for rew in rowVals])/len(rowVals)
		var.append(mean + (avDelta if add else (-avDelta)))
	return var

def minlists(lists):
	mins = []
	for row in zip(*lists):
		rowVals = [item[1] for item in row]
		mins.append(min(rowVals))
	return mins

def maxlists(lists):
	maxs = []
	for row in zip(*lists):
		rowVals = [item[1] for item in row]
		maxs.append(max(rowVals))
	return maxs

def meanlists(lists):
	means = []
	for row in zip(*lists):
		rowVals = [item[1] for item in row]
		means.append((row[0][0], sum(rowVals)/float(len(rowVals))))
	return means
