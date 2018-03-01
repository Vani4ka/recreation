import numpy as np
from sklearn.model_selection import KFold


# from ocsvm
def evaluate(clf, benignData, maliciousData):
    """Provides an enhanced evaluation function which takes labeled
    malicious as well as benign testing data and predicts it. This way,
    additional performance metrics such as false positives and true
    negatives can be calculated."""
    # start with predicting both testing sets
    benignPrediction = clf.predict(benignData)
    maliciousPrediction = clf.predict(maliciousData)

    fPos = np.count_nonzero(benignPrediction == 1)
    fNeg = np.count_nonzero(maliciousPrediction == -1)
    tPos = np.count_nonzero(maliciousPrediction == 1)
    tNeg = np.count_nonzero(benignPrediction == -1)

    fPosRate = float(fPos) / (fPos + tNeg)  # false alarm rate
    fNegRate = float(fNeg) / (fNeg + tPos)  # miss rate

    return [fPosRate, fNegRate]

def validateFold(clf, dataSetList):
    """Validates a single fold by first training and then evaluating the
    given machine learning model."""

    trainData, benignData, maliciousData = dataSetList

    # train the classifier with the train set
    clf.fit(trainData)


    # returns a list with the results of each iteration (= fold)
    return evaluate(clf, benignData, maliciousData)

# run cross-validation
def run(clf, numFolds, dataToSplit, benignTestSet):
    """Performs the cross validation by a) folding, b) training, c)
    testing. The results of each iteration are stored and finally
    returned."""
    nF = numFolds
    kf = KFold(n_splits=nF, shuffle=False)
    dataSetList = []
    for train, test in kf.split(dataToSplit):
        dataToTrain = []
        dataToTest = []
        for i in xrange(len(train)):
            dataToTrain.append(dataToSplit[train[i]])
        for i in xrange(len(test)):
            dataToTest.append(dataToSplit[test[i]])
        dataSetList.append((dataToTrain, benignTestSet, dataToTest))

    mapped = map(lambda x: validateFold(clf, x), dataSetList)

    return mapped

def calcErrorRate( l ):
	"""Calculates mean error rates out of the given single error rates of the
	individual CV folds."""

	t = zip(*l)
	fPos, fNeg = [reduce(lambda x, y: x + y, t[i]) / len(t[i]) for i in range(2)]
	return (fPos, fNeg)