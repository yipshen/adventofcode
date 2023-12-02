


# bag = {'red':12, 'green':13, 'blue':14}

# minBag = {'red':0, 'green':0, 'blue':0}

def isPossible(bag, setGame) -> bool:
    # result = True
    for e in setGame:
        setofCube = e.split(',')
        # print(f"e:{setofCube}")
        for dice in setofCube:
            des = dice.strip(' ').split()
            # print(f"des:{des}")
            numberDice = int(des[0])
            colorDice = des[1]
            # print(f"numberDice:{numberDice} colorDice:{colorDice}")
            if numberDice > bag[colorDice]:
                return False
    return True

def findMinBag(setGame):
    bag = {'red': 0, 'green': 0, 'blue': 0}
    for e in setGame:
        setofCube = e.split(',')
        # print(f"e:{setofCube}")
        for dice in setofCube:
            des = dice.strip(' ').split()
            # print(f"des:{des}")
            numberDice = int(des[0])
            colorDice = des[1]
            # print(f"numberDice:{numberDice} colorDice:{colorDice}")
            if numberDice > bag[colorDice]:
                bag[colorDice] = numberDice
    print(f"minBag: {bag}")
    return  bag

def loadFile(inputFile):
    sumPower = 0

    minBag = None
    with open(inputFile, 'r') as f:
        for line in f:
            power = 1
            a = line.split(':')
            idGame = int(a[0].split(' ')[1])
            setGame = a[1].strip('\n').split(';')
            minBag = findMinBag(setGame)
            for k in minBag:
                power = power * minBag[k]
            print(f"idGame {idGame} power: {power}")
            sumPower += power
        print(f"sumPower: {sumPower}")

def main():
    # inputfile = "test.txt"
    inputfile = "input.txt"
    loadFile(inputfile)



# main
if __name__ == '__main__':
    main()