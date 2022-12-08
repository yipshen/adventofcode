from pprint import pprint

file = "input.txt"
#file = "../inputs/test.txt"

listOfElves = []
elvesNumber = 0
calories = 0
maxCalorie = 0
maxElves = 0

with open(file, "r") as f:
    for line in f:
        #print(line, end = '')
        if line in "\n" :
            elvesNumber += 1
            if maxCalorie < calories :
                maxCalorie = calories
                maxElves = elvesNumber
            listOfElves.append([elvesNumber,calories])
            calories = 0
        else:
            calories += int(line)

pprint(listOfElves)
print(f"elve {maxElves} calorie {maxCalorie}")


def elveMax (listofelve):
    maxCal = listofelve[0][1]
    elve = listOfElves[0][0]

    #print(f"elv: ({elve}, {maxCal} {type(maxCal)} {type(elve)})")
    for i in listofelve[1:]:
        if maxCal < i[1]:
            maxCal = i[1]
            elve = i[0]
    #print(f"elv: ({elve},{maxCal})")
    return [elve, maxCal]

#result = elveMax(listOfElves)

#print(f"result {result}")

def sumOfCalories (listOfElves):
    resultSum = 0
    for i in listOfElves:
        resultSum += i[1]
    return resultSum


podium = []
for i in range(0,3):
    result = elveMax(listOfElves)
    podium.append(result)
    listOfElves.remove(result)

pprint(podium)

print(f"{sumOfCalories(podium)}")