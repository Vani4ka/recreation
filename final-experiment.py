from sklearn import svm
import numpy as np
from numpy import genfromtxt
import features as f
import functions as func
import sys
import datetime

config = {
    "folds":8,
    "trainingSet":"data/new-datasets/original/fopt/malicious-subset.txt",
    "testingSetMal":"data/new-datasets/original/final-experiment/malicious-testingset-new.txt",
    "testingSetBen":"data/new-datasets/original/final-experiment/benign-testingset-new.txt",
}

if __name__ == '__main__':

    nu = 0.02


    # training data
    trainingSet = genfromtxt(config["trainingSet"], delimiter='\t')
    # testing data
    maliciousTest = genfromtxt(config["testingSetMal"], delimiter='\t')
    benignTest = genfromtxt(config["testingSetBen"], delimiter='\t')

    #experimenting with gamma values
    # gamma = 0.14
    # for i in range(100):
    #     step = 0.01
    #     gamma = gamma + step
    #     ocsvm = svm.OneClassSVM(nu=nu, kernel="rbf", gamma=gamma, cache_size=1000)
    #     ocsvm.fit(trainingSet)
    #     benignPrediction = ocsvm.predict(benignTest)
    #     maliciousPrediction = ocsvm.predict(maliciousTest)
    #
    #     fPos = np.count_nonzero(benignPrediction == 1)
    #     fNeg = np.count_nonzero(maliciousPrediction == -1)
    #     tPos = np.count_nonzero(maliciousPrediction == 1)
    #     tNeg = np.count_nonzero(benignPrediction == -1)
    #
    #     fPosRate = float(fPos) / (fPos + tNeg)  # false alarm rate
    #     fNegRate = float(fNeg) / (fNeg + tPos)
    #
    #     if (fPosRate == 0.0 and fNegRate < 0.018):
    #         print "for gamma= " + str(gamma)
    #         print "MR: " + str(fNegRate * 100.0)





    #original
    gamma = 0.28

    ocsvm = svm.OneClassSVM(nu=nu, kernel="rbf", gamma=gamma, cache_size=1000)
    ocsvm.fit(trainingSet)
    benignPrediction = ocsvm.predict(benignTest)
    dfb = ocsvm.decision_function(benignTest)
    print "dfb" + str(dfb)
    maliciousPrediction = ocsvm.predict(maliciousTest)
    dfm = ocsvm.decision_function(maliciousTest)
    print "dfm" + str(dfm)

    fPos = np.count_nonzero(benignPrediction == 1)
    fNeg = np.count_nonzero(maliciousPrediction == -1)
    tPos = np.count_nonzero(maliciousPrediction == 1)
    tNeg = np.count_nonzero(benignPrediction == -1)

    fPosRate = float(fPos) / (fPos + tNeg)  # false alarm rate
    fNegRate = float(fNeg) / (fNeg + tPos)

    print "FAR: " + str(fPosRate*100.0)
    print "MR: " + str(fNegRate*100.0)