import numpy as np
from sklearn.model_selection import KFold


# from ocsvm
def evaluate(clf, benignData, maliciousData):
    """Provides an enhanced evaluation function which takes labeled
    malicious as well as benign testing data and predicts it. This way,
    additional performance metrics such as false positives and true
    negatives can be calculated."""
    # start with predicting both testing sets
    benign = clf.predict(benignData)
    malicious = clf.predict(maliciousData)

    fPos = np.count_nonzero(benign == 1)
    fNeg = np.count_nonzero(malicious == -1)
    tPos = np.count_nonzero(malicious == 1)
    tNeg = np.count_nonzero(benign == -1)

    fPosRate = float(fPos) / (fPos + tNeg)  # false alarm rate
    fNegRate = float(fNeg) / (fNeg + tPos)  # miss rate

    return [fPosRate, fNegRate]

    print "False alarm rate: " + str(fPosRate)
    print "Miss rate: " + str(fNegRate)

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
    # and shuffle the sets
    kf = KFold(n_splits=nF)
    dataSetList = []
    for train, test in kf.split(dataToSplit):
        dataSetList.append((dataToSplit[train], benignTestSet, dataToSplit[test]))
        # print "indices for train " + str(train)
        # print "indices for test " + str(test)

    # return map(validateFold, (clf, dataSetList)
    mapped = map(lambda x: validateFold(clf, x), dataSetList)

    # for entry in mapped:
    #     print entry

    return mapped

def calcErrorRate( l ):
    """Calculates mean error rates out of the given single error rates of the
	individual CV folds."""
    t = zip(*l)
    print t
    fPos, fNeg = [reduce(lambda x, y: x + y, t[i]) / len(t[i]) for i in range(2)]
    return (fPos, fNeg)