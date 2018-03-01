import re

s = open('temp-8.txt').read()
s = re.sub(r"\Wopen file '<stderr>', mode 'w' at [a-z, A-Z, 0-9]+\W ", "", s)
s = re.sub(r"\Wopen file '<stderr>', mode 'w' at [a-z, A-Z, 0-9]+\W ", "", s)
t = open('temp-8.txt', 'w')
t.write(s)
t.close()