import re
import time


def clean(line):
    line = line.strip("\t")

    features = line.split()
    featureset = []
    featureset.append(features[3])
    featureset.append(features[4])
    featureset.append(features[5])
    featureset.append(features[6])
    newLine = "\t".join(featureset)
    return newLine

data = open('new-datasets/malicious-testingset_scaled.txt', 'r').readlines()
new_data = map(lambda l: clean(l), data)
new  = open('new-datasets/malicious-testingset-new.txt', 'w')
for l in new_data:
    new.write(l)
    new.write('\n')
