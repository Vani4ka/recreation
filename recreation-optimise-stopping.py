from sklearn import svm
from numpy import genfromtxt
import features as f
import functions as func
import sys
import datetime
import math


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


def findBestErrorRateM( d ):
    """Determines the best error rates by first selecting the lowest false
    alarm rate and then selecting the lowest miss rate if there are several
    pairs with an equal FAR."""

    lowest = ((1,1),(1,1))
    def fPos( p ): return p[0][0]
    def fNeg( p ): return p[0][1]
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
    global counter
    global threshold

    g = tpl[0]
    n = tpl[1]
    counter = counter + 1

    ocsvm = svm.OneClassSVM(nu=n, kernel="rbf", gamma=g, cache_size=1000)
    errorRate = func.calcErrorRate(func.run(ocsvm, config["folds"], trS, teS))
    tmpResults[errorRate] = (g, n, lookUp[subsetCnt])
    print str(format(errorRate[0], '.20f')) + " " + str(format(errorRate[1], '.20f')) + " : gamma= " + str(g) + " nu= " + str(n) + " features= " + str(lookUp[subsetCnt])


    if counter == rejected:
        threshold = findBestErrorRate(results)
        t = open('results/stopping-rule-comparison/results-' + str(config["folds"]) + '.txt', 'a+')
        sys.stdout = t
        print "Started on " + started.strftime("%Y-%m-%d %H:%M")
        print "Finished on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print "Execution time " + str(datetime.datetime.now() - started) + "\n"
        print "Results for feature subset / model parameters for " + str(config["folds"]) + "-folded CV with " + str(
            len(gammaVal)) + \
              " gamma values and " + str(len(nuVal)) + " nu values:\n"
        print "Stopping rule threshold:"
        print "gamma                    :" + str(threshold[1][0])
        print "nu                       :" + str(threshold[1][1])
        print "feature subset           :" + str(threshold[1][2])
        print "threshold      : %s%% false alarm rate, %s%% miss rate" % (
            str(threshold[0][0] * 100), str(threshold[0][1] * 100)) + "\n"
        sys.stdout = temp
        t.close()

    elif counter > rejected:
        t = open('results/stopping-rule-comparison/results-' + str(config["folds"]) + '.txt', 'a+')
        sys.stdout = t
        if (threshold[0][0] > errorRate[0]) or (threshold[0][0] == errorRate[0] and threshold[0][1] > errorRate[1]):

            print "Best result found:"
            print "gamma                    :" + str(g)
            print "nu                       :" + str(n)
            print "feature subset           :" + str(lookUp[subsetCnt])
            print "grid search results      : %s%% false alarm rate, %s%% miss rate" % (
                str(errorRate[0] * 100), str(errorRate[1] * 100))
            print "------------------------------------------------------------"
            sys.exit("Stopping rule")
        elif counter == candidates:
            print "Best result found (not better than the threshold):"
            print "gamma                    :" + str(g)
            print "nu                       :" + str(n)
            print "feature subset           :" + str(lookUp[subsetCnt])
            print "grid search results      : %s%% false alarm rate, %s%% miss rate" % (
                str(errorRate[0] * 100), str(errorRate[1] * 100))
            print "------------------------------------------------------------"
        sys.stdout = temp
        t.close()


def createCombos():
    """Creates all combinations of gamma and nu values"""
    combos =[]
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
    print "best found feature subset / model parameters for " + str(config["folds"]) + "-folded CV with " + str(
        len(gammaVal)) + " gamma values and " + str(len(nuVal)) + " nu values:"
    print "gamma                    : %s" % str(best[1][0])
    print "nu                       : %s" % str(best[1][1])
    print "feature subset           : %s" % str(best[1][2])
    print "grid search results      : %s%% false alarm rate, %s%% miss rate" % (
    str(best[0][0] * 100), str(best[0][1] * 100))
    print "------------------------------------------------------------"




results = {}
config = {
    "folds":8,
    "trainingSet":"new-datasets/malicious-dataset_scaled.txt",
    "testingSet":"new-datasets/benign-dataset_scaled.txt",
}


if __name__ == '__main__':

    subsetCnt = 0
    numFeatures = f.getFeatureAmount(config["trainingSet"])

    started = datetime.datetime.now()

    gammaVal = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]
    nuVal = [0.001, 0.201, 0.401, 0.601, 0.801]

    # training data
    malicious = genfromtxt(config["trainingSet"], delimiter='\t')

    # benign data
    benign = genfromtxt(config["testingSet"], delimiter='\t')

    combinations = createCombos()


    # stopping rule
    counter = 0
    threshold = 0.0
    shuffled = f.shuffling(malicious, benign)
    lookUp = shuffled[0]
    # calculate number of candidates
    candidates = len(gammaVal) * len(nuVal) * len(lookUp)
    # calculate the number of candidates to be rejected
    rejected = int(candidates / math.exp(1))

    orig_stdout = sys.stdout
    temp = open('results/stopping-rule-comparison/temp-' + str(config["folds"]) + '.txt', 'a+')
    temp.write("Started on " + started.strftime("%Y-%m-%d %H:%M") + "\n")
    temp.write("Finished on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n")
    sys.stdout = temp

    for trS, teS in shuffled[1]:
        print "starting model selection with feature subset " + str(subsetCnt + 1) + " of " + str(2**numFeatures -1)

        tmpResults = {}

        map(compute, combinations)
        results.update(tmpResults)
        subsetCnt += 1

    sys.stdout = orig_stdout
    temp.write("\n")
    temp.close()
