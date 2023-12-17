
import re
from pprint import pprint

import numpy as np
import threading
import time

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

def loadmatrice2(matrice, minCol, minLig, maxLig, maxCol, file):
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
            if sensorX >= minCol and sensorX < maxLig and sensorY >= minCol and sensorY < maxCol:
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

def putListSignalOnMap(matrice, listSignal, minCol, minLig, maxCol, maxLig):
    for e in listSignal:
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

# test si le point est dans le losange du sensor
def isinSensor(sensor, beacon, point):
    px, py = point
    sx, sy = sensor
    manhattan = getManhattanDistance(sensor, beacon)
    return abs(px-sx) + abs(py-sy) <= manhattan



def whichSensor(intervall, listsensors, listbeacons):
    nbSensor = len(listsensors)
    minCol, minLig, maxCol, maxLig = intervall
    sensorList = []
    beaconList = []
    for e in range(nbSensor):
        manhattan = getManhattanDistance(listsensors[e], listbeacons[e])
        if isinSensor(listsensors[e], listbeacons[e], (minCol, minLig)) or \
            isinSensor(listsensors[e], listbeacons[e], (maxCol, maxLig))  :
            # print(f"sensor: {listsensors[e]} beacon: {listbeacons[e]}")
            sensorList.append(listsensors[e])
            beaconList.append(listbeacons[e])

    return sensorList, beaconList


def testInterval(intervall, listsensors, listbeacons,limite):
    nbSensor = len(listsensors)
    minCol, minLig, maxCol, maxLig = intervall
    nextCase = False
    cellToPath = []

    for i in range(minCol,maxCol):
        for j in range(minLig, maxLig):
            cellToPath.append((i,j))
    # print(f"celltopath: {cellToPath}")
    while len(cellToPath)>0:
        cpt = 0
        for e in range(nbSensor):
            c = cellToPath[0]
            test = isinSensor(listsensors[e], listbeacons[e], c)
            # print(f"--sensor: {listsensors[e]} cell:{c} test:{test} celltopathlen:{len(cellToPath)}")
            if isinSensor(listsensors[e], listbeacons[e], c):
                cellToPath.remove(c)
                # print(f"celltopath after remove:{len(cellToPath)}")
                if len(cellToPath) == 0:
                     break
            else:
                cpt += 1
            if (cpt == nbSensor) and (c[0]<= limite and c[1] <=limite):
                # print(f"solute {c}")
                return (c)


def getBoundSensor(sensor, beacon, mincol, maxcol, minlig, maxlig):
    result = []
    manhattan = getManhattanDistance(sensor, beacon)+1
    sX, sY = sensor
    j = manhattan
    #premier quart ++ second quart -+
    for i in range(manhattan+1):
        rX1 = sX + i
        rY1 = sY + j
        # print(f"++ {rX1,rY1}")
        if rX1 >= mincol and rX1 <= maxcol and rY1 >= minlig and rY1 <= maxlig:
            result.append((rX1,rY1))
        rX2 = sX - j
        rY2 = sY + i
        # print(f"-+ {rX2,rY2}")
        if rX2 >= mincol and rX2 <= maxcol and rY2 >= minlig and rY2 <= maxlig:
            result.append((rX2,rY2))

        rX3 = sX - j
        rY3 = sY - i
        # print(f"-- {rX3, rY3}")
        if rX3 >= mincol and rX3 <= maxcol and rY3 >= minlig and rY3 <= maxlig:
            result.append((rX3,rY3))
        rX4 = sX + i
        rY4 = sY - j
        # print(f"+- {rX4, rY4}")
        if rX4 >= mincol and rX4 <= maxcol and rY4 >= minlig and rY4 <= maxlig:
            result.append((rX4,rY4))
        j -= 1
    return set(result)


def isInSensorList(listSensors, listBeacons, point):
    listSize = len(listSensors)
    result = False
    for e in range(listSize):
        if isinSensor(listSensors[e], listBeacons[e], point):
            return True
    return False


def main():
    # inputfile = "test.txt"
    inputfile = "input.txt"


    minCol, maxCol, minLig, maxLig = scanMatriceSize(inputfile)
    #
    # minCol = minCol-2
    minCol = 0
    # minLig = minLig-4
    minLig = 0
    # maxLig = maxLig+1
    # maxCol = maxCol+1
    maxLig = 4000000
    maxCol = 4000000
    # maxCol = 20
    # maxLig = 20
    #
    # print(f"minCol:{minCol}, maxCol:{maxCol}, minLig:{minLig} maxLig:{maxLig}")
    # map = initMatrice(abs(minLig) + abs(maxLig), abs(minCol) + abs(maxCol))
    # nbLig, nbCol = map.shape
    # print(f"taille matrice: nbligne:{nbLig} nbcol:{nbCol}")
    # loadmatrice(map, minCol, minLig, inputfile)
    # loadmatrice2(map, minCol, minLig, maxLig, maxCol, inputfile)

    # listSensors, listBeacons = extracData(inputfile)
    #
    # nbElement = len(listSensors)
    # print(f"listSensors: {listSensors}\nlistBeacons: {listBeacons}")
    # listFinale = []
    #
    # for i in range(nbElement):
    #     sensor = listSensors[i]
    #     beacon = listBeacons[i]
    #     listCoord = getListCoordManhattan1(sensor, beacon, 25)
    #     putListSignalOnMap(map, listCoord, minCol, minLig, maxCol, maxLig)
    #
    # afficheMatrice2(map, minCol, minLig, maxCol, maxLig)

    listSensors, listBeacons = extracData(inputfile)
    # afficheMatrice2(map, minCol, minLig, maxCol, maxLig)
    nbElement = len(listSensors)
    final = []

    # measure duration
    start = time.time()

    for e in range(nbElement):
        print(f"{e} sensor:{listSensors[e]} beacon:{listBeacons[e]}")
        r = getBoundSensor(listSensors[e], listBeacons[e], minCol, maxCol, minLig, maxLig)

        for point in r:
            if not isInSensorList(listSensors, listBeacons, point):
                print(f"pottential beacon detected")
                final.append(point)
        print(f"size final: {len(final)}")
    #
    #
    #     putListSignalOnMap(map, r, minCol, minLig, maxCol, maxLig)
    #     afficheMatrice2(map, minCol, minLig, maxCol, maxLig)
    #     final += list(r)
    final = set(final)
    print(f"final: {list(final)[0]}")
    soluce2X, soluce2Y = list(final)[0]
    soluce2 = soluce2X * 4000000 + soluce2Y
    #
    print(f"soluce2: {soluce2}")
    end = time.time()
    print(end - start)  # time in seconds

if __name__ == '__main__':
    main()