import re
from resultEntry import ResultEntry

def parseLine(line):
    result = ResultEntry()
    if not line.strip():
        pass
    else:
        if "features" in line:
            mains = line.split("features= ")
            splits = mains[0].split()
            result = ResultEntry(float(splits[0]), float(splits[1]), mains[1])
    return result

def findBestFAR(result, best):

    if result.far < best.far:
        best = result
    elif result.far == best.far and result.mr < best.mr:
        best = result

    return best

def findBestMR(result, best):

    if result.mr < best.mr:
        best = result
    elif result.mr == best.mr and result.far < best.far:
        best = result

    return best




data = open("/home/vanya/Bachelor Thesis/code/recreation/data/results/optimisations/temp-8.txt", "r").readlines()
data = map(lambda l: parseLine(l), data)
bestFAR = ResultEntry()
bestMR = ResultEntry()
for i in range(len(data)):
    bestFAR = findBestFAR(data[i], bestFAR)
    bestMR = findBestMR(data[i], bestMR)

print "Best FAR:"
print str(bestFAR.far) + ", " + str(bestFAR.mr) + " with feature set: " + bestFAR.featureSet + "\n"
print "Best MR:"
print str(bestMR.far) + ", " + str(bestMR.mr) + " with feature set: " + bestMR.featureSet


