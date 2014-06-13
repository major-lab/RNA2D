"""small test script"""
from shapedistance import *
from utility import *

data = fastaRead("r2.txt")
allData = []
for (name, subopts) in data:
    allData += subopts

S = ShapeSet()

for subopt in allData:
    S.add(subopt)

keys = S.get_keys()

keys.sort(key=lambda x: x[1], reverse=True)