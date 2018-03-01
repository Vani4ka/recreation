import numpy as np
from sklearn import svm
from numpy import genfromtxt
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import featuresFixing as f
import functionsNoShuffle as func
import sys
import re
import datetime
from sklearn.externals import joblib



# should be one more similar function for MR - see tables in documentation
def findBestErrorRate( d ):
    """Determines the best error rates by first selecting the lowest false
    alarm rate and then selecting the lowest miss rate if there are several
    pairs with an equal FAR."""

    lowest = ((1,1),(1,1))
    def fPos( p ): return p[0][0]
    def fNeg( p ): return p[0][1]
    for pair in d.iteritems():
        # new lowest FAR found
        if fPos(pair) < fPos(lowest):
            lowest = pair
        # equal FAR - take a look at MR
        elif fPos(pair) == fPos(lowest):
            if fNeg(pair) < fNeg(lowest):
                lowest = pair
    return lowest


results = {}
config = {
    "folds":8,
    "trainingSet":"data/malicious.txt",
    "testingSet":"data/benign.txt",
}

started = datetime.datetime.now()

# gammaVal = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]

gammaVal = [0.1, 0.3, 0.5]

# first testing only under the conditions, which were the best according to the author

nuVal = [0.001]

# nuVal = [0.001, 0.201, 0.401, 0.601, 0.801]


# training data
malicious = genfromtxt(config["trainingSet"], delimiter='\t')

# benign data
benign = genfromtxt(config["testingSet"], delimiter='\t')

subsetCnt = 0
numFeatures = f.getFeatureAmount(config["trainingSet"])
lookUp = f.calculateSubsets()
# print 'folds: ' + str(config["folds"])
# print 'numfeatures: ' + str(numFeatures)


def printResults( resultList ):
    """Determines the best results of the given lists and prints them well
    readable."""

    best = findBestErrorRate(resultList)
    joblib.dump(ocsvm, 'test-ocsvm.pkl')
    print "best found feature subset / model parameters for " + str(config["folds"]) + "-folded CV with " + str(len(gammaVal)) + " gamma values and " + str(len(nuVal)) + " nu values:"
    print "gamma                    : %s" % str(best[1][0])
    print "nu                       : %s" % str(best[1][1])
    print "feature subset           : %s" % str(best[1][2])
    print "grid search results      : %s%% false alarm rate, %s%% miss rate" % (str(best[0][0]*100), str(best[0][1]*100))
    print "\n"


for trainingSet, testingSet in f.possibleFeatureSubsets(config["trainingSet"], config["testingSet"]):
   # print 'first for-loop'
    subsetCnt + 1, 2 ** numFeatures
    tmpResults = {}

# level 2 - iterating over all possible gamma values,
# based on 1/len(features)
    for gamma in gammaVal:
    #    print 'second for-loop'
        # level 3 - iterating over all possible nu values
        for nu in nuVal:
     #       print 'third for-loop'
            ocsvm = svm.OneClassSVM(nu=nu, kernel="rbf", gamma=gamma, cache_size=1000)
            errorRate = func.calcErrorRate(func.run(ocsvm, config["folds"], malicious, benign))
            tmpResults[errorRate] = (gamma, nu, lookUp[subsetCnt])

     # write the results of every fold and combination into a file
            print sys.stderr, ("%.20f %.20f : gamma=%s nu=%s features=%s" % (
            errorRate[0], errorRate[1], str(gamma), str(nu), str(lookUp[subsetCnt])))


        # printResults(tmpResults)
        results.update(tmpResults)
        subsetCnt += 1



printResults(results)

# print printResults(results)