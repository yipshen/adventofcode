import random
import string
import sys
import time

import pygame
import numpy as np
from pygame.locals import *
import logging
from Field import Field


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

colorList = [ (255, 255, 255),
            (1, 90, 26),
            (61, 120, 26),
            (81, 150, 26),
            (101, 200, 26),
            (131, 220, 26),
            (161, 220, 26),# level 7
            (91, 220, 26),
            (237, 240, 120),
            (237, 255, 110),
            (237, 255, 90),
            (237, 255, 70),
            (237, 255, 50),
            (237, 255, 30),
            (237, 255, 0),
            (247, 183, 56),
            (237, 183, 56),
            (227, 183, 56),
            (217, 183, 56),
            (207, 183, 56),
            (197, 183, 56),
            (187, 183, 56),
            (147, 102, 12),
            (137, 102, 12),
            (127, 102, 12),
            (117, 102, 12),
            (107, 102, 12),
            (255, 255, 255)
]

couleur = [(0,255,255),(235,235,235),(215,215,215),(205,205,205),(195,195,195),(185,185,185),(175,175,175),(165,165,165)]
colorField = dict(zip(list(range(0, 28)), colorList))
mapLetterToLevel = dict(zip(string.ascii_lowercase,list(range(1,27))))
mapLetterToLevel['S'] = 0
mapLetterToLevel['E'] = 27

mapLevelToLetter = dict(zip(list(range(1, 27)), string.ascii_lowercase))
mapLevelToLetter[0] = 'S'
mapLevelToLetter[27] = 'E'

# print(f"{colorField}")
# print(f"{mapLetterLevel}")

stack = []
cellsExplored = []
stackOfPath = []
# cellEnd = None
carte = None
cellStart = None

dictSprite = {}
def loadInput(input: str) -> np.array:

    with open(input, 'r') as f:
        firstLine = f.readline().strip()
        if 'S' in firstLine:
            lig = 0
            col = firstLine.index('S')
            global cellStart
            cellStart = (lig, col)
            stack.append((lig, col))
        if 'E' in firstLine:
            lig = 0
            col = firstLine.index('E')
            global cellEnd
            cellEnd = (lig, col)

        gridField = np.array([[Field(colorField[mapLetterToLevel[x]],mapLetterToLevel[x]) for x in firstLine]])
        cpt = 1
        for line in f:
            lineStripe = line.strip()
            if 'S' in lineStripe:
                lig = cpt
                col = lineStripe.index('S')
                cellStart = (lig, col)
                stack.append((lig, col))
            if 'E' in lineStripe:
                lig = cpt
                col = lineStripe.index('E')
                cellEnd = (lig, col)
            a = [Field(colorField[mapLetterToLevel[x]],mapLetterToLevel[x]) for x in lineStripe]
            gridField = np.vstack([gridField, a])
            cpt += 1

    return gridField

def listAPosition(matrice):
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    listAPos = []
    for i in range(rowMin, rowMax):
        for j in range(colMin, colMax):
            if (i == rowMin or i == rowMax-1 or j == colMin or j == colMax-1) and (matrice[i,j].getAltitude() == 1):
                listAPos.append((i, j))
    logger.debug(f"listAPosition - listAPos: {listAPos}")
    return listAPos

def highlightPosition(matrice, listePos):
    for e in listePos:
        matrice[e].setColor((227, 77, 175))
        matrice[e].setLabel(str(matrice[e].getAltitude()))


def displayMap(matrice, window):
    carteofsprites = pygame.sprite.Group()
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    space = 2
    marge = 2
    height = window.get_height()
    width = window.get_width()
    sizeCaseY = (height - ((2 * marge) + (space * rowMax))) // rowMax
    sizeCaseX = (width - ((2 * marge) + (space * colMax))) // colMax

    center_x = (abs(height - (rowMax * sizeCaseY + rowMax * space)) // 2 )
    center_y = (abs(width - (colMax * sizeCaseX + colMax * space)) // 2 )

    # myfont = pygame.font.SysFont("", 15)
    logger.debug(f"displayMap - init Display Matrice size {rowMax, colMax} sizeCaseY: {sizeCaseY} sizeCaseX: {sizeCaseX}")
    idSprite = 0
    for i in range(rowMin, rowMax):
        caseCoordY = ((sizeCaseY+space) * i) + center_x
        for j in range(colMin, colMax):
            caseCoordX = ((sizeCaseX+space) * j) + center_y
            logger.debug(f"displayMap - matrice[{i},{j}]: {matrice[i, j].getAltitude()}")
            matrice[i,j].image = pygame.Surface([sizeCaseX, sizeCaseY])
            matrice[i,j].image.fill(matrice[i,j].getCurrentColor())
            matrice[i,j].rect = matrice[i,j].image.get_rect()
            matrice[i,j].rect.x = caseCoordX
            matrice[i,j].rect.y = caseCoordY
            matrice[i,j].lig = i
            matrice[i,j].col = j
            # matrice[i,j].refreshLabel()
            carteofsprites.add(matrice[i, j])
            dictSprite[(i,j)] = idSprite
            idSprite += 1
    carteofsprites.draw(window)
    return carteofsprites

def printMap(matrice: np.array):
    maxRow,maxCol = np.shape(matrice)
    for i in range(0,maxRow):
        print("|",end='')
        for j in range(0,maxCol):
            print(f"{matrice[i,j].getAltitude():02d}|", end='')
        print("")

def printSoluce():
    global cellsExplored
    for s in cellsExplored:
        print(f"len: {len(s)}\n{s}")

def resetMap(matrice: np.array):
    maxRow, maxCol = np.shape(matrice)
    for i in range(0,maxRow):
        for j in range(0,maxCol):
            matrice[i,j].resetColor()
            # matrice[i,j].refreshLabel()
            matrice[i,j].resetFieldVisited()

def resetMapVisited(matrice: np.array):
    maxRow, maxCol = np.shape(matrice)
    for i in range(0,maxRow):
        for j in range(0,maxCol):
            matrice[i,j].resetFieldVisited()

def isGo(matrice:np.array, currentCase: list, nextCase: list)-> bool:
    minRow, minCol = 0,0
    maxRow, maxCol = np.shape(matrice)
    curRow, curCol = currentCase
    nextRow, nextCol = nextCase
    if matrice[nextRow, nextCol].isVisited():
        return False
    # test if isTooHigh
    if matrice[nextRow, nextCol].getAltitude() - matrice[curRow, curCol].getAltitude() > 1 :
        return False
    # test if isTooLow
    if matrice[nextRow, nextCol].getAltitude() - matrice[curRow, curCol].getAltitude() < -1 :
        return True
    # test if border
    if nextRow > maxRow or nextCol > nextCol:
        return False
    if nextRow < minRow or nextCol < minCol:
        return False
    # test if ok
    if matrice[nextRow, nextCol].getAltitude() - matrice[curRow, curCol].getAltitude() == 0:
        return True
    if matrice[nextRow, nextCol].getAltitude() - matrice[curRow, curCol].getAltitude() == -1:
        return True
    if matrice[nextRow, nextCol].getAltitude() - matrice[curRow, curCol].getAltitude() == 1:
        return True


def getCaseArround(matrice:np.array, currentCase) -> list:
    # logger.debug(f"getCaseArround - currentCase: {currentCase}")
    result = []
    minRow, minCol = 0,0
    maxRow, maxCol = np.shape(matrice)
    curRow, curCol = currentCase

    if curRow == minRow:
        if curCol == minCol:
            # coin haut gauche
            result.append((curRow + 1, curCol))
            result.append((curRow,curCol+1))
            return result
        elif curCol == (maxCol-1):
            # coin haut droite
            result.append((curRow,curCol-1))
            result.append((curRow+1, curCol))
            return result
        # au bord sans coin
        result.append((curRow,curCol-1))
        result.append((curRow+1, curCol))
        result.append((curRow, curCol+1))
        return result
    elif curRow == (maxRow-1):
        if curCol == minCol:
            # coin bas gauche
            result.append((curRow, curCol+1))
            result.append((curRow-1, curCol))
            return result
        elif curCol == (maxCol-1):
            # coin bas droite
            result.append((curRow,curCol-1))
            result.append((curRow-1,curCol))
            return result
        # au bord sans coin
        result.append((curRow,curCol-1))
        result.append((curRow-1, curCol))
        result.append((curRow, curCol+1))
        return result
    elif curCol == minCol:
        # bord gauche
        result.append((curRow-1, curCol))
        result.append((curRow, curCol+1))
        result.append((curRow + 1, curCol))
        return result
    elif curCol == maxCol-1:
        # bord droit
        result.append((curRow-1, curCol))
        result.append((curRow, curCol-1))
        result.append((curRow+1, curCol))
        return result
    result.append((curRow - 1, curCol))
    result.append((curRow, curCol-1))
    result.append((curRow+1, curCol))
    result.append((curRow, curCol+1))

    return result

def getManhattanLong(c1, c2):
    c1x,c1y = c1
    c2x,c2y = c2
    return abs(c2x -c1x) + abs(c2y - c1y)

def getListCasePossibleToGo(matrice, cellCurrent, cellsFollowed) -> list:
    listCaseArround = getCaseArround(matrice, cellCurrent)

    listCaseDispo = []
    for e in listCaseArround :
        if isGo(carte, cellCurrent, e) and (e not in cellsFollowed):
            listCaseDispo.append(e)
    return listCaseDispo


def getListCaseAdjacentToGo(matrice, cellCurrent):
    listCaseArround = getCaseArround(matrice, cellCurrent)

    listCaseDispo = []
    for e in listCaseArround :
        if isGo(carte, cellCurrent, e):
            listCaseDispo.append(e)
    return listCaseDispo

def colorisedCells(matrice, color, listCells):
    for c in listCells:
        matrice[c].setColor(color)
        # matrice[c].refreshLabel()


def choosePath(listPath: list):
    size = len(listPath)
    return listPath[round(random.random()*size) % size]


# explore random and rollback when is blocked
def exploreRandomMap(cellDebut, cellFin, cellsFollowed, spritesfield, screen):
    # go back
    logger.debug(f"exploreMap2 - cellsFollowed {cellsFollowed}")
    currentCell = cellDebut
    refresh = 0
    while currentCell != cellFin:
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255,0,0))
        else:
            carte[currentCell].setColor(couleur[0])
        # carte[currentCell].refreshLabel()
        cellsFollowed.append(currentCell)
        logger.debug(f"exploreMap2 - cellsFollowed: len : {len(cellsFollowed)}\n {cellsFollowed}")
        if refresh % 10 == 0:
            spritesfield.draw(screen)
            pygame.display.flip()
        refresh += 1
        listPossiblePaths = getListCasePossibleToGo(carte, currentCell, cellsFollowed)
        logger.debug(f"exploreMap2 - listPossiblePaths: {listPossiblePaths}")

        if len(listPossiblePaths) == 0:
            rollback = -1
            while len(listPossiblePaths) == 0:
                logger.debug(f"exploreMap2 - rollback cellsFollowed len: {len(cellsFollowed)} \n cellsFollowed \n{cellsFollowed}")
                currentCell = cellsFollowed[rollback]
                carte[currentCell].setColor(couleur[6])
                listPossiblePaths = getListCasePossibleToGo(carte, currentCell, cellsFollowed)
                rollback += -1
                spritesfield.draw(screen)
                # pygame.display.flip()

        else:
            currentCell = choosePath(listPossiblePaths)

    logger.debug(f"fini")

#Breadth-First Search
def parcoursGrapheLargeur(cellDebut, cellFin, spritesfield, screen ):
    cellsQueue = []
    cellsQueue.append(cellDebut)
    carte[cellDebut].setVisited()
    pathLength = 0
    refresh = 0
    while cellsQueue:
        currentCell = cellsQueue.pop(0)
        pathLength += 1
        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"parcoursGrapheLargeur - currentCell: {currentCell} listcaseAdja: {caseAdjacentPossible}")
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255,0,0))
        else:
            carte[currentCell].setColor(couleur[0])
        # carte[currentCell].refreshLabel()

        for e in caseAdjacentPossible:
            if not carte[e].isVisited():
                cellsQueue.append(e)
                carte[e].setVisited()
        if refresh % 10 == 0:
            spritesfield.draw(screen)
            pygame.display.flip()
        refresh += 1
        if currentCell == cellEnd:
            break
    print(f"fini")


def initDijkstra(matrice, cellDebut, color=(255,255,255)):
    infini = 10000
    maxRow, maxCol = np.shape(matrice)
    matrice[cellDebut].setColor(color)
    for i in range(0,maxRow):
        for j in range(0,maxCol):
            matrice[i,j].setDistance(infini)
    matrice[cellDebut].setDistance(0)

def initAstar(matrice, cellDebut, color=(255,255,255)):
    infini = 10000
    maxRow, maxCol = np.shape(matrice)
    matrice[cellDebut].setColor(color)
    for i in range(0,maxRow):
        for j in range(0,maxCol):
            matrice[i,j].setDistance(infini)
    matrice[cellDebut].setDistance(0)

def getCellMinDistance(listcell):
    listSorted = sorted(listcell,key=lambda x: carte[x].getDistance())
    logger.debug(f"getCellMinDistance - listcell: {listcell} \n listSorted: {listSorted}")
    return listSorted.pop(0)

# def buildpath(listcell):
#     listSorted = sorted(listcell,key=lambda x: carte[x].getDistance(),reverse=True)
#     logger.debug(f"buildpath - listcell: {listcell} \n listSorted: {listSorted}")
#     return listSorted.pop(0)

def dijkstraFX(cellDebut, cellFin, spritesfield, screen):
    initDijkstra(carte, cellDebut)
    logger.debug(f"dijkstraFX - cellDebut distance = {carte[cellDebut].getDistance()}")
    stackPriority = [cellDebut]
    refresh = 0
    nbCaseVisited = 0
    while stackPriority:

        # logger.debug(f"dijkstraFX - stackPriority: {stackPriority}")
        currentCell = stackPriority.pop(0)
        nbCaseVisited += 1
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255, 255, 255))
        else:
            carte[currentCell].setColor(couleur[0])
        #   carte[currentCell].refreshLabel()

        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"dijkstraFX - caseAdjacentPossible: {caseAdjacentPossible}")
        for e in caseAdjacentPossible:
            if (carte[currentCell].getDistance() + carte[e].getPoids()) < carte[e].getDistance():
                carte[e].setDistance(carte[currentCell].getDistance() + carte[e].getPoids())
                # logger.debug(f"dijkstraFX - update distance carte[{e}] {carte[e].getDistance()}")
                carte[e].setParent(currentCell)
                # carte[e].resetColor()
                # carte[e].refreshLabel()

            if not carte[e].isVisited():
                stackPriority.append(e)
                carte[e].setVisited()
            # logger.debug(f"dijkstraFX - stackPriority: {stackPriority}")

        #cherche la cellule la plus petite distance avec la cellule courrante
        stackPriority = sorted(stackPriority,key=lambda x: carte[x].getDistance())

        if refresh % 10 == 0 :
            spritesfield.draw(screen)
            pygame.display.flip()

        refresh += 1
        if currentCell == cellFin:

            logger.debug(f"dijkstraFX - >>>>>>>>>>>>>trouvé<<<<<<<<<<<<<")
            logger.debug(f"dijkstraFX - cellDebut: {cellDebut} pathLengh : {carte[currentCell].getDistance() } caseVisited: {nbCaseVisited}")
            break
    currentCell = carte[currentCell].getParent()

    while currentCell != cellDebut:
        carte[currentCell].setColor((255,0,0))

        if refresh % 5 == 0 :
            spritesfield.draw(screen)
            pygame.display.flip()
        refresh += 1
        # spritesfield.draw(screen)
        # pygame.display.flip()
        # carte[currentCell].refreshLabel()
        currentCell = carte[currentCell].getParent()
    return carte[cellFin].getDistance()

def dijkstra(cellDebut, cellFin):
    initDijkstra(carte, cellDebut)
    # logger.debug(f"dijkstra - cellDebut distance = {carte[cellDebut].getDistance()}")
    stackPriority = [cellDebut]
    nbCaseVisited = 0
    findPath = False
    while stackPriority:

        # logger.debug(f"dijkstra - stackPriority: {stackPriority}")
        currentCell = stackPriority.pop(0)
        nbCaseVisited += 1
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255, 255, 255))
        else:
            carte[currentCell].setColor(couleur[0])

        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"dijkstra - caseAdjacentPossible: {caseAdjacentPossible}")
        for e in caseAdjacentPossible:
            if (carte[currentCell].getDistance() + carte[e].getPoids()) < carte[e].getDistance():
                carte[e].setDistance(carte[currentCell].getDistance() + carte[e].getPoids())
                # logger.debug(f"dijkstra - update distance carte[{e}] {carte[e].getDistance()}")
                carte[e].setParent(currentCell)

            if not carte[e].isVisited():
                stackPriority.append(e)
                carte[e].setVisited()
            # logger.debug(f"dijkstrae - stackPriority: {stackPriority}")

        #cherche la cellule la plus petite distance avec la cellule courrante
        stackPriority = sorted(stackPriority,key=lambda x: carte[x].getDistance())

        if currentCell == cellFin:
            findPath = True
            logger.debug(f"dijkstra - >>>>>>>>>>>>>trouvé<<<<<<<<<<<<<")
            logger.debug(f"dijkstra - cellDebut:{cellDebut} pathLength : {carte[currentCell].getDistance() } caseVisited: {nbCaseVisited}")
            break
    if findPath :
        return carte[currentCell].getDistance()
    else:
        return -1


def astarFX(cellDebut, cellFin, spritesfield, screen):
    initAstar(carte, cellDebut)
    logger.debug(f"astarFX - cellDebut distance = {carte[cellDebut].getDistance()} heuristique:{getManhattanLong(cellDebut, cellFin)}")
    stackPriority = [cellDebut]
    carte[cellDebut].setVisited()
    carte[cellDebut].setLabel(str(carte[cellDebut].getDistance()) + "|"+ str(getManhattanLong(cellDebut, cellFin))
                              + "="+ str(carte[cellDebut].getDistance()+getManhattanLong(cellDebut, cellFin)))
    refresh = 0
    nbCaseVisited = 0
    while stackPriority:
        # logger.debug(f"astarFX - stackPriority: {stackPriority}")
        currentCell = stackPriority.pop(0)
        nbCaseVisited += 1
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255, 255, 255))
            # carte[currentCell].updateLabel()
        else:
            carte[currentCell].setColor(couleur[0])
            # carte[currentCell].updateLabel()


        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"astarFX - caseAdjacentPossible: {caseAdjacentPossible}")
        for e in caseAdjacentPossible:

            if (carte[currentCell].getDistance() + carte[e].getPoids())  < carte[e].getDistance():
                carte[e].setDistance(carte[currentCell].getDistance() + carte[e].getPoids())
                carte[e].setParent(currentCell)

            if not carte[e].isVisited():
                stackPriority.append(e)
                carte[e].setVisited()

            carte[e].setLabel(str(carte[e].getDistance()) +"|"+ str(getManhattanLong(e,cellFin))+"="+
                              str(carte[e].getDistance()+getManhattanLong(e,cellFin)))

            # logger.debug(f"astarFX - e: {e} costH: {costHeuristique} costTotal: {carte[e].getDistance() + costHeuristique}")


        #cherche la cellule avec le moins de cout avec la cellule courrante
        # stackPriority = sorted(stackPriority, key=lambda x: carte[x].getDistance() + getManhattanLong(x, cellFin))
        stackPriority = sorted(stackPriority, key=lambda x: getManhattanLong(x, cellFin))
        # listCost = [(carte[a].getDistance() + getManhattanLong(a, cellFin)) for a in stackPriority]

        # logger.debug(f"astarFX - stackPriority: {stackPriority}")
        if refresh % 10 == 0 :
            spritesfield.draw(screen)
            pygame.display.flip()

        refresh += 1
        if currentCell == cellFin:
            logger.debug(f"astarFX -  >>>>>>>>>>>>>trouvé<<<<<<<<<<<<<")
            logger.debug(f"astarFX -  cellDebut:{cellDebut}  pathLength : {carte[currentCell].getDistance()} caseVisited: {nbCaseVisited}")
            break
    # currentCell = carte[currentCell].getParent()

    # draw shortPath
    while currentCell != cellDebut:
        carte[currentCell].setColor((255,0,0))

        if refresh % 5 == 0 :
            spritesfield.draw(screen)
            pygame.display.flip()
        refresh += 1
        currentCell = carte[currentCell].getParent()
    return carte[cellFin].getDistance()

def astar(cellDebut, cellFin):
    initAstar(carte, cellDebut)
    # logger.debug(f"astar - cellDebut distance = {carte[cellDebut].getDistance()} heuristique:{getManhattanLong(cellDebut, cellFin)}")
    stackPriority = [cellDebut]
    carte[cellDebut].setVisited()
    findPath = False
    # carte[cellDebut].setLabel(str(carte[cellDebut].getDistance()) + "|"+ str(getManhattanLong(cellDebut, cellFin))
    #                           + "="+ str(carte[cellDebut].getDistance()+getManhattanLong(cellDebut, cellFin)))

    nbCaseVisited = 0

    while stackPriority:
        # logger.debug(f"astar - stackPriority: {stackPriority}")
        currentCell = stackPriority.pop(0)
        nbCaseVisited += 1
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255, 255, 255))

        else:
            carte[currentCell].setColor(couleur[0])

        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"astar - caseAdjacentPossible: {caseAdjacentPossible}")
        for e in caseAdjacentPossible:
            if (carte[currentCell].getDistance() + carte[e].getPoids())  < carte[e].getDistance():
                carte[e].setDistance(carte[currentCell].getDistance() + carte[e].getPoids())
                carte[e].setParent(currentCell)

            if not carte[e].isVisited():
                stackPriority.append(e)
                carte[e].setVisited()

            carte[e].setLabel(str(carte[e].getDistance()) +"|"+ str(getManhattanLong(e,cellFin))+"="+
                              str(carte[e].getDistance()+getManhattanLong(e,cellFin)))

            # logger.debug(f"astar - e: {e} costH: {costHeuristique} costTotal: {carte[e].getDistance() + costHeuristique}")

        #cherche la cellule avec le moins de cout avec la cellule courrante
        # stackPriority = sorted(stackPriority, key=lambda x: carte[x].getDistance() + getManhattanLong(x, cellFin))
        stackPriority = sorted(stackPriority, key=lambda x: getManhattanLong(x, cellFin))
        # listCost = [(carte[a].getDistance() + getManhattanLong(a, cellFin)) for a in stackPriority]

        # logger.debug(f"astar - stackPriority: {stackPriority}")
        if currentCell == cellFin:
            findPath = True
            logger.debug(f"astar -  >>>>>>>>>>>>>trouvé<<<<<<<<<<<<<")
            logger.debug(f"astar - cellDebut: {cellDebut} pathLengh : {carte[currentCell].getDistance()} caseVisited: {nbCaseVisited}")
            break
    if findPath :
        return carte[currentCell].getDistance()
    else:
        return -1



#Depth-First Search
def parcoursGrapheProfondeur(cellDebut, cellFin, spritesfield, screen ):
    cellsQueue = []
    cellsQueue.append(cellDebut)
    carte[cellDebut].setVisited()
    pathLength = 0
    refresh = 0
    while cellsQueue:
        currentCell = cellsQueue.pop()
        pathLength += 1
        caseAdjacentPossible = getListCaseAdjacentToGo(carte, currentCell)
        # logger.debug(f"parcoursGrapheLargeur - currentCell: {currentCell} listcaseAdja: {caseAdjacentPossible}")
        if currentCell == cellDebut or currentCell == cellFin:
            carte[currentCell].setColor((255, 0, 0))
        else:
            carte[currentCell].setColor(couleur[0])
        # carte[currentCell].refreshLabel()
        if currentCell == cellFin:
            break
        for e in caseAdjacentPossible:
            logger.debug(f"parcoursGrapheLargeur - e : {e}")
            if not carte[e].isVisited():
                cellsQueue.append(e)
                carte[e].setVisited()
                # carte[e].refreshLabel()
        if refresh % 10 == 0:
            spritesfield.draw(screen)
            pygame.display.flip()
        refresh += 1
    return pathLength

# for use this methode need increase recursif loop in python
def explortGraphProfondeurRec(cellDebut, cellFin, spritesfield, screen):

    if cellDebut == cellFin:
        print("trouve")
    else:
        carte[cellDebut].setColor(couleur[0])
        carte[cellDebut].setVisited()
        spritesfield.draw(screen)
        pygame.display.flip()
        caseAdjacentPossible = getListCaseAdjacentToGo(carte, cellDebut)
        logger.debug(f"caseAdjacentPossible : {caseAdjacentPossible}")
        for e in caseAdjacentPossible:
            if not carte[e].isVisited():
                explortGraphProfondeurRec(e, cellFin, spritesfield, screen)




def main():
    pygame.init()
    # width, height = 1900,900
    width, height = 600,400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("climbing_sol1")
    screen.fill((0, 0, 0))
    # input = "test.txt"
    input = "input.txt"
    global carte
    carte = loadInput(input)
    # printMap(grid)

    spritesfield = displayMap(carte, screen)
    print(f"stack: {stack} cellEnd: {cellEnd} cellStart: {cellStart}")

    while 1:
        # pygame.time.Clock().tick(60)
        event_list = pygame.event.get()
        for event in event_list:  # On parcours la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                sys.exit()  # On quite le programme
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    astarFX(cellStart,cellEnd,spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()  # On quite le programme
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    parcoursGrapheLargeur(cellStart, cellEnd, spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    parcoursGrapheProfondeur(cellStart, cellEnd, spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    listA = listAPosition(carte)
                    highlightPosition(carte,listA)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    listA = listAPosition(carte)
                    listSolution = []
                    for a in listA:
                        resetMap(carte)
                        lengthPath = dijkstra(a, cellEnd)
                        if lengthPath > 0:
                            listSolution.append((a,lengthPath))
                    solution = min(listSolution, key=lambda x: x[1])
                    logger.debug(f"via dijkstra: solution {solution[0]} with pathlength: {solution[1]}")
                    resetMap(carte)
                    dijkstraFX(solution[0], cellEnd, spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    listA = listAPosition(carte)
                    listSolution = []
                    for a in listA:
                        resetMap(carte)
                        lengthPath = astar(a,cellEnd)
                        if lengthPath > 0:
                            listSolution.append((a,lengthPath))
                    solution = min(listSolution, key=lambda x: x[1])
                    logger.debug(f"via astar: solution {solution[0]} with pathlength: {solution[1]}")
                    resetMap(carte)
                    astarFX(solution[0], cellEnd, spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    resetMap(carte)
                    dijkstraFX(cellStart, cellEnd, spritesfield, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    resetMap(carte)
            # mouse Event
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for cell in spritesfield:
                    if cell.rect.collidepoint(event.pos):
                        print(f"cell: {cell.getAltitude()} lig,col: {cell.lig},{cell.col}")
                        a = getListCaseAdjacentToGo(carte, (cell.lig, cell.col))
                        print(f"cheminPossible: {a}")
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                for cell in spritesfield:
                    if cell.rect.collidepoint(event.pos):
                        cellSelected = (cell.lig, cell.col)
                        print(f"cell: {cell.getAltitude()} cellSelected: {cellSelected}")
                        cell.setColor(colorList[0])
                        cell.setVisited()
                        # cell.refreshLabel()
                        if cellSelected not in stack:
                            stack.append(cellSelected)
                        logger.debug(f"main - stack: {stack}")

        spritesfield.draw(screen)
        pygame.display.flip()



if __name__ == '__main__':

    main()