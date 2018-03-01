import re

def clean(line):
    line = line.strip()
    line = re.sub('([1-9]):', '', line)
    line = re.sub(' ', '\t', line)
    line = re.sub('(0[ \t])', '', line)
    return line

data = open('old-datasets/benign-dataset_scaled.txt', 'r').readlines()
new_data = map(lambda l: clean(l), data)
new  = open('new-datasets/benign-dataset_scaled.txt', 'w')
for l in new_data:
    new.write(l)
    new.write('\n')
