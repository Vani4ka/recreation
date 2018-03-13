from sklearn import svm
from numpy import genfromtxt
import features as f
import functions as func
import sys
import datetime
import math


def findBestErrorRate(d):
    """Determines the best error rates by first selecting the lowest false
    alarm rate and then selecting the lowest miss rate if there are several
    pairs with an equal FAR."""

    lowest = ((1, 1), (1, 1))

    def fPos(p):
        return p[0][0]

    def fNeg(p):
        return p[0][1]

    for pair in d.iteritems():
        # new lowest FAR found
        if fPos(pair) < fPos(lowest):
            lowest = pair
        # equal FAR - take a look at MR
        elif fPos(pair) == fPos(lowest):
            if fNeg(pair) < fNeg(lowest):
                lowest = pair
    return lowest


def findBestErrorRateM(d):
    """Determines the best error rates by first selecting the lowest false
    alarm rate and then selecting the lowest miss rate if there are several
    pairs with an equal FAR."""

    lowest = ((1, 1), (1, 1))

    def fPos(p):
        return p[0][0]

    def fNeg(p):
        return p[0][1]

    for pair in d.iteritems():
        # new lowest MR found
        if fNeg(pair) < fNeg(lowest):
            lowest = pair
        # equal MR - take a look at FAR
        elif fNeg(pair) == fNeg(lowest):
            if fPos(pair) < fPos(lowest):
                lowest = pair
    return lowest


def compute(tpl):
    """Takes a combination of gamma and nu value and trains and
    evaluates a OC-SVM using the current feature set"""

    g = tpl[0]
    n = tpl[1]

    ocsvm = svm.OneClassSVM(nu=n, kernel="rbf", gamma=g, cache_size=1000)
    errorRate = func.calcErrorRate(func.run(ocsvm, config["folds"], malicious, benign))
    tmpResults[errorRate] = (g, n)
    print str(format(errorRate[0], '.20f')) + " " + str(format(errorRate[1], '.20f')) + " : gamma= " + str(
        g) + " nu= " + str(n)


def createCombos():
    """Creates all combinations of gamma and nu values"""

    combos = []
    for gamma in gammaVal:
        for nu in nuVal:
            combos.append((gamma, nu))
    return combos


def printResults(resultList):
    """Determines the best results of the given lists and prints them well
    readable."""

    # for FAR
    best = findBestErrorRate(resultList)

    # for MR
    # best = findBestErrorRateM(resultList)
    print "Best found feature subset / model parameters for " + str(config["folds"]) + "-folded CV with " + str(
        len(gammaVal)) + " gamma values and " + str(len(nuVal)) + " nu values:"
    print "gamma                    : %s" % str(best[1][0])
    print "nu                       : %s" % str(best[1][1])
    print "grid search results      : %s%% false alarm rate, %s%% miss rate" % (
    str(best[0][0] * 100), str(best[0][1] * 100))
    print "------------------------------------------------------------"


results = {}
config = {
    "folds": 8,
    "trainingSet": "data/new-datasets/original/fopt/malicious-subset.txt",
    "testingSet": "data/new-datasets/original/fopt/benign-subset.txt",
}

if __name__ == '__main__':

    started = datetime.datetime.now()

    # arrays with gamma and nu values
    gammaVal = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2,
                0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29]
    nuVal = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
             0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2,
             0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3,
             0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39]

    # training data
    malicious = genfromtxt(config["trainingSet"], delimiter='\t')
    # benign data
    benign = genfromtxt(config["testingSet"], delimiter='\t')

    subsetCnt = 0
    numFeatures = f.getFeatureAmount(config["trainingSet"])
    # lookUp = f.calculateSubsets()

    combinations = createCombos()

    # writing temporary results to a file
    orig_stdout = sys.stdout
    temp = open('data/results/optimisations/fopt-temp-' + str(config["folds"]) + '.txt', 'a+')
    temp.write("Started on " + started.strftime("%Y-%m-%d %H:%M") + "\n")
    sys.stdout = temp

    for c in combinations:

        tmpResults = {}

        compute(c)

        results.update(tmpResults)
        subsetCnt += 1

    temp.write("Finished on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n")
    sys.stdout = orig_stdout
    temp.close()

    # writing the final result to a file
    f = open('data/results/optimisations/fopt-results-' + str(config["folds"]) + '.txt', 'a+')
    sys.stdout = f

    print "Started on " + started.strftime("%Y-%m-%d %H:%M")
    print "Finished on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print "Execution time " + str(datetime.datetime.now() - started) + "\n"
    printResults(results)

    sys.stdout = orig_stdout
    f.close()
