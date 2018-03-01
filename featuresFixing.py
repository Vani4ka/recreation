import string, itertools, re


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


def possibleFeatureSubsets( *dataSets ):
	"""Iterates over all possible feature subsets of the given data sets. For a
	data set with 7 features, there are 2^7 - 1 i.e., 127 subsets. All given
	data sets must exhibit the same amount of features. Thus a patch for
	svm-scale(1) was written which prevents the skipping of zero-valued fields.
	The given data sets are file names."""

	mergedSet = []
	lenList = [0]

	# read all data sets at once from the respective files
	dataSets = map(lambda fileName: open(fileName).readlines(), dataSets)

	# save length of each data sets (later needed for splitting)
	map(lambda dataSet: lenList.append(len(dataSet)), dataSets)

	# merge data sets to a single one
	map(lambda dataSet: map(lambda line: mergedSet.append(line), dataSet), dataSets)
	print '!!!DO NOT FORGET TO ADJUST THE FEATURES!!! '

	# clean merged data set (strip()) and split it into its
	# single features (split())
	mergedSet = map(lambda line: line.strip().split(), mergedSet)

	# transpose merged data set to lists instead of tuples
	# (for reordering the indices)
	transposedDataSet = map(lambda element: list(element), zip(*mergedSet))

	# now build all possible combinations (2**len(features) - 1)
	# and yield temporary results
	for r in xrange(0, len(transposedDataSet) +1):
		for featureSubset in itertools.combinations(transposedDataSet, r):
			# reorder indices - they have to start with 0 and increment
			# with each feature
			# should the index be 1 or 0? (original 1)
			index = 0
			# print 'not sure about this'
			for i in xrange(len(featureSubset)): # iterate over columns
				for j in xrange(len(featureSubset[i])): # iterate over lines of columns
					featureSubset[i][j] = re.sub(".:", "%d:" % index, featureSubset[i][j])
				index += 1
			# transpose merged data set back
			tempSubset = map(lambda line: string.join(line, "\t"), zip(*featureSubset))
			tempSubset = map(lambda line: line, tempSubset)
			# split merged data set back to the original data sets
			yield [tempSubset[lenList[i] : (lenList[i] + lenList[i+1])] for i in xrange(len(lenList[:-1]))]


def getFeatureAmount( fileName ):
	"""Determines the amount of features of the given file by taking a look at
	the first line."""

	f = open(fileName)
	line = f.readline()
	f.close()
	# changed because the data format has been changed
	return len(line.strip().split())
