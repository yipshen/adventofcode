import logging
import re
import sys
from pprint import pprint
import time
import numpy
import numpy as np
import pygame
from pygame.locals import *



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
scanlogger = logging.getLogger("scanMatriceSize")

def scanMatriceSize(inputFile):

    # check matrice size
    minLine, maxLine, minCol, maxCol = 10000, 0, 10000, 0
    with open(inputFile,'r') as f:
        for line in f:
            x = re.findall("([0-9]*),", line.strip())
            y = re.findall(",([0-9]*)", line.strip())
            minX, maxX, minY, maxY = int(min(x)), int(max(x)), int(min(y)), int(max(y))

            if minX < minCol:
                minCol = minX
            if maxX > maxCol:
                maxCol = maxX
            if minY < minLine:
                minLine = minY
            if maxY > maxLine:
                maxLine = maxY

        scanlogger.debug(f" x: {x} min: {minLine} max: {maxLine} y: {y} min: {minCol} max: {maxCol}")
        return minLine, maxLine, minCol, maxCol


def initMatrice(nbRow, nbCol):
    resultat = np.full((nbRow, nbCol), fill_value=".", dtype=list)
    return resultat

def loadRock(inputFile, matrice, colOrigine):
    with open(inputFile,'r') as f:
        for line in f:
            l = [eval(x) for x in line.split(' -> ')]
            print(f"l : {l}")
            previous = l[0]
            for e in l[1:]:
                print(f"cmp: {previous} vs {e}")
                if previous[0] == e[0]:
                    # vertical change ligne
                    if previous[1] > e[1]:
                        # down
                        # print(f"  down from {previous[1]} to {e[1]}")
                        for i in range(e[1], previous[1]+1):
                            # print(f"matrice {i}")
                            matrice[i, e[0] - colOrigine ] = '#'
                    else:
                        # up
                        # print(f"  up from {previous[1]} to {e[1]}")
                        for i in range(previous[1], e[1]+1):
                            # print(f"matrice {i}")
                            matrice[i, e[0] - colOrigine] = '#'
                else:
                    # horizontal change col
                    if previous[0] > e[0]:
                        # left
                        # print(f" left from {previous[0]} to {e[0]}")
                        for i in range(e[0], previous[0]+1):
                            # print(f"matrice {i}")
                            matrice[e[1], i - colOrigine] = '#'
                    else:
                        # right
                        # print(f"  right from {previous[0]} to {e[0]}")
                        for i in range(previous[0], e[0]+1):
                            # print(f"matrice {i}")
                            matrice[e[1], i - colOrigine] = '#'
                previous = e
    return matrice


def displayMap(matrice, window, sizeCase):
    # carteofsprites = pygame.sprite.Group()
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    height = window.get_height()
    width = window.get_width()
    center_x = width // 2
    center_y = height // 2

    padding_x = center_x - (colMax * sizeCase)//2
    padding_y = center_y - (rowMax * sizeCase)//2

    # myfont = pygame.font.SysFont("", 15)
    logger.debug(f"displayMap - init Display Matrice size {rowMax, colMax} sizeCaseY: {sizeCase} sizeCaseX: {sizeCase}")
    idSprite = 0
    for i in range(rowMin, rowMax):
        caseCoordY = padding_y + i * sizeCase
        for j in range(colMin, colMax):
            caseCoordX = padding_x + j * sizeCase
            # print(f"matrice[{i},{j}] {matrice[i,j]}")
            if matrice[i, j] == '.':
                pygame.draw.rect(window, (222, 184, 135), pygame.Rect(caseCoordX, caseCoordY, sizeCase, sizeCase))
            if matrice[i, j] == '#':
               pygame.draw.rect(window, (128, 0, 0), pygame.Rect(caseCoordX, caseCoordY, sizeCase, sizeCase))
            if matrice[i, j] == 'o':
                   pygame.draw.rect(window, (255, 255, 0), pygame.Rect(caseCoordX, caseCoordY, sizeCase, sizeCase))
            if matrice[i, j] == '~':
                   pygame.draw.rect(window, (30, 144, 255), pygame.Rect(caseCoordX, caseCoordY, sizeCase, sizeCase))
            if matrice[i, j] == '+':
                   pygame.draw.rect(window, (0, 255, 0), pygame.Rect(caseCoordX, caseCoordY, sizeCase, sizeCase))
    pygame.display.flip()

def printMatrice(matrice: np.array , zone: (int, int, int, int) )-> None:
    rowMin, colMin, rowMax, colMax = zone
    rowNewMatrice = rowMax - rowMin
    colNewMatrice = colMax - colMin
    matriceShape = matrice[rowMin:rowMax,colMin:colMax]
    m = np.full((rowNewMatrice,colNewMatrice), '.', dtype=str)
    for i in range(0,rowNewMatrice-1):
        for j in range(0,colNewMatrice-1):
            if isinstance(matriceShape[i, j], list):
                if 'H' in matriceShape[i,j]:
                    m[i, j] = 'H'
                elif 'T' in matriceShape[i,j]:
                    m[i, j] = 'T'
                elif 'S' in matriceShape[i,j]:
                    m[i, j] = 'S'
            else:
                m[i, j] = matriceShape[i, j]
    print(f"{m}")


def isBlocked(matrice: np.array, point: (int, int), minCol: int) -> bool:
    lig_y = point[0]
    col_x = point[1]
    matriceSize = matrice.shape
    maxColMatrice = matriceSize[1] - 1


    if col_x == minCol:
        # grain sur le bord gauche
        if ((matrice[lig_y + 1, col_x - minCol] == '#' or matrice[lig_y + 1, col_x - minCol] == 'o') and (matrice[lig_y + 1, col_x+1 - minCol] == '#' or matrice[lig_y + 1, col_x+1 - minCol] == 'o')):
            return True

    if col_x == minCol+maxColMatrice:
        # grain sur la bord droit
        if ((matrice[lig_y + 1, col_x - minCol] == '#' or matrice[lig_y + 1, col_x - minCol] == 'o')
                and (matrice[lig_y + 1, col_x-1 - minCol] == '#' or matrice[lig_y + 1, col_x-1 - minCol] == 'o')):
            return True

    if col_x > minCol and col_x < minCol + maxColMatrice:
        # test si le grain est plat
        if ((matrice[lig_y + 1, col_x - minCol] == '#' or matrice[lig_y + 1, col_x - minCol] == 'o')
            and (matrice[lig_y + 1, col_x-1 - minCol] == '#' or matrice[lig_y + 1, col_x-1 - minCol] == 'o')
            and (matrice[lig_y + 1, col_x+1 - minCol] == '#' or matrice[lig_y + 1, col_x+1 - minCol] == 'o')):
            return True

    return False

def getNextCoord(matrice: np.array, point: (int, int), minCol: int) -> (int,int):

    lig_y = point[0]
    col_x = point[1]
    matriceSize = matrice.shape
    maxColMatrice = matriceSize[1] - 1
    if not isBlocked(matrice, point, minCol):
        if col_x == minCol:
            # grain sur le bord gauche
            if matrice[lig_y + 1, col_x - minCol] == '.':
                return (lig_y + 1, col_x)
            if matrice[lig_y + 1, col_x + 1 - minCol] == '.':
                return (lig_y + 1, col_x + 1)

        if col_x == minCol + maxColMatrice:
            # grain sur la bord droit
            if matrice[lig_y + 1, col_x - minCol ] == '.':
               return ( lig_y + 1, col_x)
            if matrice[lig_y + 1, col_x - 1 - minCol] == '.':
               return (lig_y + 1, col_x - 1)

        if col_x > minCol and col_x < minCol + maxColMatrice:
            # test si le grain est plat
            if matrice[lig_y + 1, col_x - minCol] == '.':
                return (lig_y + 1, col_x)
            if matrice[ lig_y + 1, col_x - 1 - minCol] == '.':
                return (lig_y + 1, col_x - 1)
            if matrice[lig_y + 1, col_x + 1 - minCol] == '.':
                return (lig_y + 1, col_x + 1)

    return point


def getElementMap(matrice: np.array, point: (int, int), minCol) -> (int, int):
    return matrice[point[0], point[1]-minCol]

def putSandOnMap(matrice: np.array, point: (int, int), minCol) -> None:
    matrice[point[0], point[1]-minCol] = 'o'

def putAirOnMap(matrice: np.array, point: (int, int), minCol) -> None:
    matrice[point[0], point[1]-minCol] = '.'

def putFlowOnMap(matrice: np.array, point: (int, int), minCol) -> None:
    matrice[point[0], point[1]-minCol] = '~'

def putSourceOnMap(matrice: np.array, point: (int, int), minCol) -> None:
    matrice[point[0], point[1]-minCol] = '+'
def allSandBlocked(matrice: np.array, sandlist, minCol) -> bool:
    for i in reversed(sandlist):
        if not isBlocked(matrice, i, minCol):
            return False
    return True


def main():

    # inputfile = "test.txt"
    inputfile = "input.txt"

    pygame.init()
    width, height = 900, 600
    caseSize = 3
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("sandFlow soluce1")
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))

    # get matrice size
    minLig, maxLig, minCol, maxCol = scanMatriceSize(inputfile)
    logger.debug(f"f minLig:{minLig} maxLig:{maxLig} minCol:{minCol} maxCol:{maxCol}")
    minCol = minCol - 1

    # allocate matrice
    map = initMatrice(maxLig + 2, (maxCol - minCol) + 1)
    map = loadRock(inputfile, map, minCol)

    displayMap(map, screen, caseSize)

    sandInit = (0, 500)
    putSourceOnMap(map, sandInit, minCol)
    sandResult = []
    doSimulate = True
    sandPath = []
    idsand = 0
    while True:
        event_list = pygame.event.get()
        for event in event_list:  # On parcours la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                sys.exit()  # On quite le programme
            # interaction avec le jeu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()  # On quite le programme
                if event.key == pygame.K_a:
                    sandCurrent = sandInit
                    sandPath.append(sandCurrent)
                    idsand += 1
                    # print(map)
                    # time.sleep(1)
                    while (not isBlocked(map, sandCurrent, minCol)) and (sandCurrent[0] < maxLig) and doSimulate:
                        sandNewPos = getNextCoord(map, sandCurrent, minCol)
                        # pour animation
                        # putAirOnMap(map, sandCurrent, minCol)
                        # putSandOnMap(map, sandNewPos, minCol)
                        # time.sleep(1)
                        # displayMap(map, screen, caseSize)

                        sandPath.append(sandNewPos)
                        sandCurrent = sandNewPos
                        # print(f"sandCurrent: {sandCurrent}")

                        if isBlocked(map, sandCurrent, minCol):
                            # print(map)
                            print(f"sandPath [{idsand}]: {sandPath}")
                            sandResult.append(sandCurrent)
                            putSandOnMap(map, sandCurrent, minCol)
                            sandPath = []
                        if sandCurrent[0] >= maxLig:
                            for e in sandPath:
                                putFlowOnMap(map, e, minCol)
                            doSimulate = False
                if event.key == pygame.K_e:

                    while doSimulate:
                        sandCurrent = sandInit
                        sandPath.append(sandCurrent)
                        idsand += 1
                        speed = 0
                        while (not isBlocked(map, sandCurrent, minCol)) and (sandCurrent[0] < maxLig) and doSimulate:
                            speed += 1
                            sandNewPos = getNextCoord(map, sandCurrent, minCol)
                            # pour animation
                            # putAirOnMap(map, sandCurrent, minCol)
                            # putSandOnMap(map, sandNewPos, minCol)
                            if speed % 20 == 0:
                                displayMap(map, screen, caseSize)

                            sandPath.append(sandNewPos)
                            sandCurrent = sandNewPos
                            # print(f"sandCurrent: {sandCurrent}")

                            if isBlocked(map, sandCurrent, minCol):
                                # print(map)
                                print(f"sandPath [{idsand}]: {sandPath}")
                                sandResult.append(sandCurrent)
                                putSandOnMap(map, sandCurrent, minCol)
                                sandPath = []
                            if sandCurrent[0] >= maxLig:
                                for e in sandPath:
                                    putFlowOnMap(map, e, minCol)
                                doSimulate = False


            displayMap(map, screen, caseSize)
            # clock.tick(10)
    print(f"count sand: {len(sandResult)}")

# main
if __name__ == '__main__':
    main()

# p1 = (0, 500)
# test1 = isBlocked(map, p1, minCol)
# nextPos1 = getNextCoord(map, p1, minCol)
# print(f"map{p1}: {getElementMap(map, p1, minCol)}")
# print(f"test1: {test1} nextposition of {p1} :  {nextPos1}")
#
# p2 = (0, minCol)
# test2 = isBlocked(map, p2, minCol)
# nextPos2 = getNextCoord(map, p2, minCol)
# print(f"map{p2}: {getElementMap(map, p2, minCol)}")
# print(f"test2: {test2} nextposition of {p2} :  {nextPos2}")
#
# p3 = (8, minCol)
# test3 = isBlocked(map, p3, minCol)
# nextPos3 = getNextCoord(map, p3, minCol)
# print(f"map{p3}: {getElementMap(map, p3, minCol)}")
# print(f"map(9,494): {getElementMap(map, (9,494), minCol)}")
# print(f"test3: {test3} nextposition of {p3} :  {nextPos3}")
#
# p4 = (4, 498)
# test4 = isBlocked(map, p4, minCol)
# nextPos4 = getNextCoord(map, p4, minCol)
# print(f"map{p4}: {getElementMap(map, p4, minCol)}")
# print(f"map(5,498): {getElementMap(map, (5,498), minCol)}")
# print(f"test3: {test4} nextposition of {p4} :  {nextPos4}")