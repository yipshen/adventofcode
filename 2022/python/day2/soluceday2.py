from pprint import pprint


jakenPoint = { "A":1, "B":2, "C":3, "X":1, "Y":2, "Z":3 }

#file = "test.txt"
file = "input.txt"

def getJankenScore(playerChoice, myChoice):
    # compare choices
    result = jakenPoint[playerChoice] - jakenPoint[myChoice]
    if result == 0:
        # draw
        return jakenPoint[playerChoice] + 3
    elif result == -1 or result == 2:
        # win
        return jakenPoint[myChoice] + 6
    elif result == 1 or result == -2:
        # loose
        return jakenPoint[playerChoice]


def predictJankenScore(playerChoice, myChoice):
    if myChoice == "Y":
        # need draw
        return jakenPoint[playerChoice] + 3
    elif myChoice == "X":
        # need lose
        if playerChoice == "A":
            return 3
        elif playerChoice == "B":
            return 1
        else:
            return 2
    elif myChoice == "Z":
        if playerChoice == "A":
            return 2 + 6
        elif playerChoice == "B":
            return 3 + 6
        else:
            return 1 + 6

with open(file, "r") as f:
    total = 0
    for line in f:
        #print(f" {line} : {getJankenScore(line[0], line[2])}")
        print(f" {line} : {predictJankenScore(line[0], line[2])}")
        #total += getJankenScore(line[0], line[2])
        total += predictJankenScore(line[0], line[2])
    print(f"total: {total}")

