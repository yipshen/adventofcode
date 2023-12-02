
import re
from pprint import pprint

import numpy as np


def scanMatriceSize(inputFile):

    # check matrice size
    minLine, maxLine, minCol, maxCol = 10000, 0, 10000, 0
    with open(inputFile,'r') as f:
        for line in f:
            # result = re.search("x=(-?[0-9]*), y=(-?[0-9]*)", line.strip())
            x = re.findall("x=(-?[0-9]*)", line.strip())
            y = re.findall("y=(-?[0-9]*)", line.strip())
            # print(f"x: {x} y: {y}")
            minX, maxX, minY, maxY = int(min(x)), int(max(x)), int(min(y)), int(max(y))
            # result = re.match("x=(-?[0-9]*), y=(-?[0-9]*)", line.strip())
            # pattern = re.compile(r"x=(-?[0-9]*), y=(-?[0-9]*)")
            # for match  in pattern.finditer(line.strip()):
            #     x = eval(match.group(1))
            #     y = eval(match.group(2))
            #     # print(f"x= {x} {type(x)} y= {y} {type(y)}")

            if minX < minCol:
                minCol = minX
            if maxX > maxCol:
                maxCol = maxX
            if minY < minLine:
                minLine = minY
            if maxY > maxLine:
                maxLine = maxY

        # print(f" x: {x} minline: {minLine} maxline: {maxLine} y: {y} mincol: {minCol} maxcol: {maxCol}")
        # print(f"min: {min(minCol,minLine)} max: {max(maxLine,maxCol)}")

        return minCol, maxCol, minLine, maxLine

def initMatrice(nbRow, nbCol):
    resultat = np.full((nbRow, nbCol), fill_value=".", dtype=list)
    return resultat



def afficheMatrice(matrice: np.array, minCol, minLig):
    nbLig,nbCol = matrice.shape

    metricX = minCol
    metricY = minLig
    result = ""
    titre = []
    for e in range(metricX, nbCol):
        # print(f"e: {e}")
        if e % 5 == 0:
            titre.append(e)
        else:
            titre.append('-')

    # print(f"e: {titre}")
    l1 = []
    l2 = []
    for k in titre:
        if isinstance(k, str):
            l1.append(' ')
            l2.append(' ')
        else:
            if k >= 10:
                l1.append(str(k // 10))
                l2.append(str(k % 10))
            else:
                l1.append(' ')
                l2.append(str(k))


    # print(f"l1: {l1} \nl2: {l2}")
    str1 = ''.join(l1)
    str2 = ''.join(l2)
    print(f"   {str1}\n   {str2}")

    for i in range(nbLig):
        if metricY < 0 or metricY > 9:
            result += str(metricY) + ' '
        else:
            result += ' ' + str(metricY) + ' '
        for j in range(nbCol):
            result += matrice[i,j]
        result += '\n'
        metricY += 1
    print(f"{result}")

def afficheMatrice2(matrice: np.array, minCol, minLig, maxCol, maxLig):


    metricX = minCol
    metricY = minLig
    result = ""
    titre = []
    for e in range(metricX, maxCol):
        # print(f"e: {e}")
        if e % 5 == 0:
            titre.append(e)
        else:
            titre.append('-')

    # print(f"e: {titre}")
    l1 = []
    l2 = []
    for k in titre:
        if isinstance(k, str):
            l1.append(' ')
            l2.append(' ')
        else:
            if k >= 10:
                l1.append(str(k // 10))
                l2.append(str(k % 10))
            else:
                l1.append(' ')
                l2.append(str(k))


    # print(f"l1: {l1} \nl2: {l2}")
    str1 = ''.join(l1)
    str2 = ''.join(l2)
    print(f"   {str1}\n   {str2}")

    for i in range(maxLig):
        if metricY < 0 or metricY > 9:
            result += str(metricY) + ' '
        else:
            result += ' ' + str(metricY) + ' '
        for j in range(maxCol):
            result += matrice[i,j]
        result += '\n'
        metricY += 1
    print(f"{result}")


def loadmatrice(matrice, minCol, minLig, file):
    with open(file, 'r') as f:
        for line in f:
            x = re.findall("x=(-?[0-9]*)", line.strip())
            y = re.findall("y=(-?[0-9]*)", line.strip())
            #print(f"x: {x} y: {y}")
            sensorX = eval(x[0])
            sensorY = eval(y[0])
            beaconX = eval(x[1])
            beaconY = eval(y[1])
            # print(f"sensorY: {sensorY} sensorX: {sensorX} -> matrice[{sensorY - minLig}, {sensorX - minCol}]")
            # print(f"beaconY: {beaconY} beaconX: {beaconX} -> matrice[{beaconY - minLig}, {beaconX - minCol}]")

            matrice[sensorY - minLig, sensorX - minCol] = 'S'
            matrice[beaconY - minLig, beaconX - minCol] = 'B'

def extracData(file):
    listSensors = []
    listBeacons = []
    with open(file, 'r') as f:
        for line in f:
            x = re.findall("x=(-?[0-9]*)", line.strip())
            y = re.findall("y=(-?[0-9]*)", line.strip())
            #print(f"x: {x} y: {y}")
            sensorX = eval(x[0])
            sensorY = eval(y[0])
            beaconX = eval(x[1])
            beaconY = eval(y[1])
            listSensors.append((sensorX, sensorY))
            listBeacons.append((beaconX, beaconY))
    return  listSensors, listBeacons

def resetMap(matrice):
    nbLig, nbCol = matrice.shape
    for i in range(nbLig):
        for j in range(nbCol):
            # print(f"{matrice[i, j]}")
            if matrice[i, j] == '#':
                matrice[i, j] = '.'

def putSignalOnMap(matrice, point, minCol, minLig, maxCol, maxLig):
    # print(f"putSignalPoint: {point} lig: {point[1] - minLig} col:{point[0] - minCol}")

    if point[0] <= maxCol-1 and point[0] >= minCol and point[1] <= maxLig-1 and point[1] >= minLig:
        if matrice[(point[1] - minLig), (point[0] - minCol)] == '.':
            # print(f"putSignalPoint: {point} replace matrice: {matrice[(point[1] - minLig), (point[0] - minCol)]}")
            matrice[point[1] - minLig, point[0] - minCol] = '#'

def putListSignalOnMap(matrice, listSigal, minCol, minLig, maxCol, maxLig):
    for e in listSigal:
        putSignalOnMap(matrice, e, minCol, minLig, maxCol, maxLig)

def getManhattanDistance(sensor, beacon) -> int:
    sX, sY = sensor
    bX, bY = beacon
    return abs(bX - sX) + abs(sY - bY)

def getListCoordManhattan1(sensor, beacon, limit):
    result = []
    sX, sY = sensor # col, lig
    manhattan_lenght = getManhattanDistance(sensor, beacon)
    i = 0
    # print(f"sensor: {sensor} manhattant:{manhattan_lenght}")
    for j in range(-manhattan_lenght, manhattan_lenght+1):
        # print(f"j: {j} i: {i}")
        if j == 0 :
            for k in range(-i, i + 1):
                if (sY+j >= 0) and (sY+j <= limit) and (k+sX >= 0) and (k+sX <= limit):
                    result.append((k + sX, sY + j))
            # print(f"lig: {j} cells: {result}")
            i = manhattan_lenght - 1
        elif j < 0 :
            for k in range(-i, i+1):
                if (sY + j >= 0) and (sY + j <= limit) and (k + sX >= 0) and (k + sX <= limit):
                    result.append((k+sX, sY+j ))
            # print(f"lig: {j} cells: {result}")
            i += 1
        elif j > 0 :
            for k in range(-i, i + 1):
                if (sY + j >= 0) and (sY + j <= limit) and (k + sX >= 0) and (k + sX <= limit):
                    result.append((k + sX, sY + j))
            # print(f"lig: {j} cells: {result}")
            i -= 1
        # print(f"result len: {len(result)}")
    return result


def getListCoordManhattan2(sensor, beacon, line):
    result = []
    sX, sY = sensor # col, lig
    manhattan_lenght = getManhattanDistance(sensor, beacon)
    i = 0
    # print(f"manhattan: {manhattan_lenght} line: {line - sY}")
    if line - sY < 0:
        i = manhattan_lenght + (line - sY)
        for k in range(-i, i+1):
            # print(f"k : {k}")
            result.append((k + sX, line))
    else:
        i = manhattan_lenght - (line - sY)
        for k in range(-i, i+1):
            # print(f"k : {k}")
            result.append((k + sX, line))
    return result

def getListCoordManhattan3(sensor, beacon, line, limite):
    result = []
    sX, sY = sensor # col, lig
    manhattan_lenght = getManhattanDistance(sensor, beacon)
    i = 0
    # print(f"manhattan: {manhattan_lenght} line: {line - sY}")
    if line - sY < 0:
        i = manhattan_lenght + (line - sY)
        for k in range(-i, i+1):
            # print(f"k : {k}"
            if k+sX >= 0 and  k+sX <= limite:
                result.append((k + sX, line))

    else:
        i = manhattan_lenght - (line - sY)
        for k in range(-i, i+1):
            # print(f"k : {k}")
            if k+sX >= 0 and  k+sX <= limite:
                result.append((k + sX, line))
    return result

def getListCoordManhattan4(sensor, beacon, col, limit):
    result = []
    sX, sY = sensor # col, lig
    manhattan_lenght = getManhattanDistance(sensor, beacon)
    i = 0
    # print(f"manhattan: {manhattan_lenght} line: {line - sY}")
    if col - sX < 0:
        i = manhattan_lenght + (col - sX)
        for k in range(-i, i+1):
            # print(f"k : {k}"
            if k+sY >= 0 and  k+sY <= limit:
                result.append((col, k+sY))
    else:
        i = manhattan_lenght - (col - sX)
        for k in range(-i, i+1):
            # print(f"k : {k}")
            if k+sY >= 0 and  k+sY <= limit:
                result.append((col, k+sY))
    return result


def filterSig(listeSig, filter):
    result = []
    for e in listeSig:
        if e[1] == filter:
            result.append(e)
    return result

def addRespond(result, listetobefilter):
    resultat = result
    for e in listetobefilter:
        if not e in resultat:
            resultat.append(e)

    return resultat


def main():
    inputfile = "test.txt"
    # lineToCount = 10
    # inputfile = "input.txt"
    # lineToCount = 2000000

    # minCol, maxCol, minLig, maxLig = scanMatriceSize(inputfile)

    # minCol = minCol-2
    # minCol = 0
    # minLig = minLig-2
    # minLig = 0
    # maxLig = maxLig+1
    # maxCol = maxCol+1
    # print(f"minCol:{minCol}, maxCol:{maxCol}, minLig:{minLig} maxLig:{maxLig}")
    # map = initMatrice(abs(minLig) + abs(maxLig), abs(minCol) + abs(maxCol))
    # nbLig, nbCol = map.shape
    # print(f"taille matrice: nbligne:{nbLig} nbcol:{nbCol}")
    # loadmatrice(map, minCol, minLig, inputfile)

    listSensors, listBeacons = extracData(inputfile)

    cellX, cellY = 0,0

    nbElement = len(listSensors)
    print(f"listSensors: {listSensors}\nlistBeacons: {listBeacons}")
    listFinale = []
    limite = 20
    listFinaleLig =[]
    for i in range(nbElement):
        sensor = listSensors[i]
        beacon = listBeacons[i]
        manhattan_lenght = getManhattanDistance(sensor, beacon)
        print(f"sensor: {sensor} beacon: {beacon} manhattan: {manhattan_lenght}")
        listCoordLine = getListCoordManhattan1(sensor, beacon, limite)
        # listCoordCol = getListCoordManhattan4(sensor, beacon, lineToCount, limite)
        print(f'listCoordline: {len(listCoordLine)}')
        listFinaleLig += set(listCoordLine)
        # listFinaleCol += listCoordCol

    setfinalLig = set(listFinaleLig)
    for l in range(limite+1):
        for k in range(limite+1):
            if not ((l,k) in setfinalLig):
                print(f"toto : {l} {k}")
    # print(f"setfinal: {sorted(setfinalLig)}")
    print(f"setfinalLig len:{len(setfinalLig)}")
        # setfinalCol = set(listFinaleCol)
        # if len(setfinalLig) != limite+1 :
        #     print(f"line: {lineToCount} len: {len(setfinalLig)} ")
        #     # print(f"{sorted(setfinalLig)}\n")
        #     cellY = lineToCount
        # if len(setfinalCol) != limite+1 :
        #     print(f"col: {lineToCount} len: {len(setfinalCol)} ")
        #     # print(f"{sorted(setfinalCol)}\n")
        #     cellX = lineToCount
    print(f"fin")
    # print(f"solution2 :{cellX*4000000+cellY}")

        # putListSignalOnMap(map, sorted(listCoord), minCol, minLig, maxCol, maxLig)
            # afficheMatrice(map, minCol, minLig)
            # resetMap(map)
    # afficheMatrice2(map, 0, 0, 20, 20)

    #
    # sensor1 = (8, 7) # (col, ligne)
    # sensor2 = (2, 0)
    # sensor3 = (0, 11)
    #
    # beacon1 = (2, 10)  # (col, ligne)
    # print(f"manhattan distance beacon: {beacon} - sensor: {sensor} = {getManhattanDistance(sensor,beacon)}")
    # listCoordSig1 = getListCoordManhattan(sensor1, beacon1)
    # listCoordSig2 = getListCoordManhattan(sensor2, beacon1)
    # listCoordSig3 = getListCoordManhattan(sensor3, beacon1)
    #
    # # print(f"manhatan coord: {listCoordSig2}")
    # putListSignalOnMap(map, listCoordSig1, minCol, minLig, maxCol, maxLig)
    # putListSignalOnMap(map, listCoordSig2, minCol, minLig, maxCol, maxLig)
    # putListSignalOnMap(map, listCoordSig3, minCol, minLig, maxCol, maxLig)
    #
    # afficheMatrice(map, minCol, minLig)
    # putSignalOnMap(map, (8, 8), minCol, minLig)
    # putSignalOnMap(map, (8, 9), minCol, minLig)
    # afficheMatrice(map, minCol, minLig)
    # resetMap(map)
    # afficheMatrice(map, minCol, minLig)



if __name__ == '__main__':
    main()