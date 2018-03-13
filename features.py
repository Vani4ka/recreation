import itertools
import numpy as np
import random

def calculateSubsets( ):
	"""Builds lookup table which is used for checking to which feature subset
	an index value maps to."""

	lookUp = ["undef"] * 127
	subsetCnt = 0
	features = [
		"packets", "octets", "duration", "srcport",
		"dstport", "tcpflags", "protocol"
	]

	for r in xrange(1, len(features) + 1):
		for subset in itertools.combinations(features, r):
			lookUp[subsetCnt] = subset
			subsetCnt += 1
	return lookUp


def possibleFeatureSubsets(trainingSet, testingSet):
	trDataset = trainingSet
	trDataset = map(list,zip(*trDataset))
	teDataset = testingSet
	teDataset = map(list, zip(*teDataset))

	featureSubsetsTr = []
	featureSubsetsTe = []

    # determine possible feature sets for training
	for r in xrange(1, len(trDataset) + 1):
		featureSubsetsTr += itertools.combinations(trDataset, r)
	# transpose to receive tuples corresponding to every line in the original file and the feature subset
	# and transform the tuples into lists as the original format of the file
	for i in xrange(len(featureSubsetsTr)):
		featureSubsetsTr[i] = zip(*featureSubsetsTr[i])
		for j in xrange(len(featureSubsetsTr[i])):
			featureSubsetsTr[i][j] = np.asarray(list(featureSubsetsTr[i][j]))

	# determine possible feature sets for testing
	for r in xrange(1, len(teDataset) + 1):
		featureSubsetsTe += itertools.combinations(teDataset, r)
	for i in xrange(len(featureSubsetsTe)):
		featureSubsetsTe[i] = zip(*featureSubsetsTe[i])
		for j in xrange(len(featureSubsetsTe[i])):
			featureSubsetsTe[i][j] = np.asarray(list(featureSubsetsTe[i][j]))

	setPairs = []
	for i in xrange(len(featureSubsetsTr)):
		setPairs.append((featureSubsetsTr[i], featureSubsetsTe[i]))

	return setPairs



def getFeatureAmount( fileName ):
	"""Determines the amount of features of the given file by taking a look at
	the first line."""

	f = open(fileName)
	line = f.readline()
	f.close()
	return len(line.strip().split())

# addition for the secretary problem
def shuffling(trainingSet, testingSet):
	lU = calculateSubsets()
	sP = possibleFeatureSubsets(trainingSet, testingSet)

	combined = list(zip(lU, sP))
	random.shuffle(combined)
	lU[:], sP[:] = zip(*combined)
	return lU, sP
