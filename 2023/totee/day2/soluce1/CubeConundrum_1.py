


bag = {'red':12, 'green':13, 'blue':14}


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


def loadFile(inputFile):
    sumIDGame = 0
    with open(inputFile, 'r') as f:
        for line in f:
            a = line.split(':')
            idGame = int(a[0].split(' ')[1])
            setGame = a[1].strip('\n').split(';')
            if isPossible(bag, setGame):
                print(f"game {idGame} {setGame} {isPossible(bag, setGame)}")
                sumIDGame += idGame

        print(f"sumIDGame: {sumIDGame}")




def main():
    # inputfile = "test.txt"
    inputfile = "input.txt"
    loadFile(inputfile)



# main
if __name__ == '__main__':
    main()