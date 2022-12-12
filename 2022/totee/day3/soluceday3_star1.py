import pprint
import string
from functools import reduce

file = "test.txt"
#file = "input.txt"

#put in memory all alphabet with respective prioryties
PriorityList = dict(zip(list(string.ascii_letters), list(range(1, 53))))


listOfOccurences = [] # list containt all elements on both compartment
with open(file, 'r') as fileInput:
    for line in fileInput:
        totalItems = len(line)
        compartment1 = line[:totalItems//2]  #  split into 2 compartments
        compartment2 = line[totalItems//2:]  #

      #  print(f"nb item : {totalItems} split into 2 compartments \n c1: {compartment1} \n c2: {compartment2}")
        occurence = list(set(compartment1).intersection(set(compartment2))) # check occurence into both compartment
        listOfOccurences.append(occurence[0])


    #calculate sum of priorytie for each occurences
    #sumPrioryties = 0
    #for i in listOfOccurences:
    #    sumPrioryties += PriorityList[i]

    #with reduce function more pythonique
    sumPrioryties = reduce((lambda a, b : a + b) ,[PriorityList[x] for x in listOfOccurences])

    print(f"sum Prioryties for set {listOfOccurences} is\n >>> {sumPrioryties} <<<<")

