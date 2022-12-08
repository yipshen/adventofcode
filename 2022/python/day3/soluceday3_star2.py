import pprint
import string
from functools import reduce

#file = "test.txt"
file = "input.txt"

#put in memory all alphabet with respective prioryties
PriorityList = dict(zip(list(string.ascii_letters), list(range(1, 53))))


listOfOccurences = [] # list contain all badges of each team of Elves
with open(file, 'r') as fileInput:
    teamElves = []
    for i,line in enumerate(fileInput, start=1):
        #print(f"line : {line}",end='')
        teamElves.append(set(line.strip()))
        #print(f"teamElve {teamElves}")
        if i % 3 == 0:
            #search badge item
            occurences = list(reduce(set.intersection, [set(l) for l in teamElves]))
            listOfOccurences.append(occurences[0])
            print(f"occurence: {listOfOccurences}")
            teamElves.clear()
    #print(f"list occurence {listOfOccurences}")

    sumPrioryties = reduce((lambda a, b: a + b), [PriorityList[x] for x in listOfOccurences])
    print(f"sum Prioryties for set {listOfOccurences} is\n >>> {sumPrioryties} <<<<")