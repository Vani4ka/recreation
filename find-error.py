import numpy as np
from sklearn import svm
from numpy import genfromtxt
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import features as f
import functions as func
import sys
import re
import datetime

config = {
    "folds":4,
    "trainingSet":"new-datasets/malicious-dataset_scaled.txt",
    "testingSet":"new-datasets/benign-dataset_scaled.txt",
    # "trainingSet": "data/malicious.txt",
    # "testingSet": "data/benign.txt",
}

dataToSplit = genfromtxt(config["trainingSet"], delimiter='\t')

benign = genfromtxt(config["testingSet"], delimiter='\t')

nF = config["folds"]

print dataToSplit

kf = KFold(n_splits=nF, shuffle=False)
dataSetList = []
for train, test in kf.split(config["trainingSet"]):
    dataSetList.append((dataToSplit[train], benign, dataToSplit[test]))
    print dataToSplit[train]