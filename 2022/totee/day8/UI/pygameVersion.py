import numpy as np
import pygame
from Tree import Tree
import sys
from pygame.locals import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def loadInput(fileInput):
    with open(fileInput, "r") as f:
        firstLine = f.readline().strip()
        gridtree = np.array([[int(x) for x in firstLine]])
        for line in f:
            a = [int(x) for x in line.strip()]
            gridtree = np.vstack([gridtree, a])

    return gridtree


# A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
# Only consider trees in the same row or column;
# that is, only look up, down, left, or right from any given tree.
def isVisible(matrice, treePositions):
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    rowTree,colTree = treePositions
    # if tree is in border is visible
    if treePositions[0] == 0 or \
       treePositions[1] == 0 or \
       treePositions[0] == rowMax-1 or \
       treePositions[1] == colMax-1:
        return True

    treeSize = matrice[rowTree, colTree]

    checkLeft = checkRight = checkUp = checkDown = True

    # check left
    for e in range(colTree, colMin, -1):
        treeNeighborSize = matrice[rowTree, e-1]
        logger.debug(f"checkLetf - treeSize: {treeSize} treeNeighbordSize: {treeNeighborSize}")
        checkLeft = (treeSize > treeNeighborSize) and checkLeft
        # optimize not need browse all element of line or column
        if (treeSize <= treeNeighborSize) :
            break
    # print(f"checkLeft: {checkLeft}")
    logger.debug(f"checkLeft: {checkLeft}")

    # check right
    for e in range(colTree, colMax-1):
        treeNeighborSize = matrice[rowTree, e+1]
        logger.debug(f"checkRight  - treeSize: {treeSize} treeNeighbordSize: {treeNeighborSize}")
        checkRight = (treeSize > treeNeighborSize) and checkRight
        # optimize not need browse all element of line or column
        if (treeSize <= treeNeighborSize) :
            break
    #print(f"checkRight: {checkRight}")
    logger.debug(f"checkRight: {checkRight}")

    # check up
    for e in range(rowTree, rowMin, -1):
        treeNeighborSize = matrice[e-1, colTree]
        logger.debug(f"checkUp - treeSize: {treeSize} treeNeighbordSize: {treeNeighborSize}")
        checkUp = (treeSize > treeNeighborSize) and checkUp
        # optimize not need browse all element of line or column
        if (treeSize <= treeNeighborSize) :
            break
    #print(f"checkUp: {checkUp}")
    logger.debug(f"checkUp: {checkUp}")

    # check down
    for e in range(rowTree, rowMax-1):
        treeNeighborSize = matrice[e+1, colTree]
        #print(f"checkDown - treeSize: {treeSize} treeNeighbordSize: {treeNeighborSize}")
        logger.debug(f"checkDown - treeSize: {treeSize} treeNeighbordSize: {treeNeighborSize}")
        checkDown = (treeSize > treeNeighborSize) and checkDown
        # optimize not need browse all element of line or column
        if (treeSize <= treeNeighborSize) :
            break
    #print(f"checkDown: {checkDown}")
    logger.debug(f"checkDown: {checkDown}")
    logger.info(f"tree {(rowTree, colTree)} [{matrice[rowTree, colTree]}] \n\
    checkLeft: {checkLeft}\n\
    checkRight: {checkRight}\n\
    checkUp: {checkUp}\n\
    checkDown: {checkDown}" )
    return checkUp or checkDown or checkLeft or checkRight

# treePosition is a couple (line,col)
def scenicScore(matrice, treePosition):
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    rowTree,colTree = treePosition
    treeSize = matrice[rowTree, colTree]
    measureUp = measureLeft = measureRight = measureDown = 0

    # measuring Up
    if rowTree == rowMin:
        measureUp = 0
        logger.debug(f"tree {treePosition} [{treeSize}] - measureUp: {measureUp}")
    else:
        for e in range(rowTree, rowMin, -1):
            treeNeighborSize = matrice[e-1, colTree]
            if treeNeighborSize >= treeSize:
                measureUp += 1
                break
            else:
                measureUp += 1
        logger.debug(f"tree {treePosition} [{treeSize}] - measureUp: {measureUp}")

    # measuring down
    if rowTree == rowMax-1:
        measureDown = 0
        logger.debug(f"tree {treePosition} [{treeSize}] - measureDown: {measureDown}")
    else:
        for e in range(rowTree, rowMax-1):
            treeNeighborSize = matrice[e + 1, colTree]
            if treeNeighborSize >= treeSize:
                measureDown += 1
                break
            else:
                measureDown += 1
        logger.debug(f"tree {treePosition} [{treeSize}] - measureDown: {measureDown}")

    # measuring left
    if colTree == colMin:
        measureLeft = 0
        logger.debug(f"tree {treePosition} [{treeSize}] - measureLeft: {measureLeft}")
    else:
        for e in range(colTree, colMin, -1):
            treeNeighborSize = matrice[rowTree, e - 1]
            if treeNeighborSize >= treeSize:
                measureLeft += 1
                break
            else:
                measureLeft += 1
        logger.debug(f"tree {treePosition} [{treeSize}] - measureLeft: {measureLeft}")

    # measuring right
    if colTree == colMax - 1:
        measureRight = 0
        logger.debug(f"tree {treePosition} [{treeSize}] - measureRight: {measureRight}")
    else:
        for e in range(colTree, colMax -1):
            treeNeighborSize = matrice[rowTree, e + 1]
            if treeNeighborSize >= treeSize:
                measureRight += 1
                break
            else:
                measureRight += 1
        logger.debug(f"tree {treePosition} [{treeSize}] - measureRight: {measureRight}")


    return measureUp * measureDown * measureLeft * measureRight

def countTreesinBorder(matrice):
    rowMax, colMax = np.shape(matrice)
    return 2 * (rowMax+colMax) - 4

def subMatriceWithoutBorder(matrice):
    rowMin, colMin = 0, 0
    rowMax, colMax = np.shape(matrice)
    return matrice[rowMin+1:rowMax-1, colMin+1:colMax-1]


def countTreeVisible(matrice):
    result = 0
    rowSubMatriceMin, colSubMatriceMin = 1, 1
    rowMatriceMax, colMatriceMax = np.shape(matrice)
    rowSubMatriceMax, colSubMatriceMax = rowMatriceMax-1, colMatriceMax-1
    for i in range(rowSubMatriceMin,rowSubMatriceMax):
        for j in range(colSubMatriceMin, colSubMatriceMax):
            if isVisible(matrice, (i,j)) :
                result += 1
            # logger.debug(f"tree: {(i,j)} vaut : {matrice[i][j]} visible ? {isVisible(matrice, (i,j))}")
                #logger.info(f"tree: {(i, j)} vaut : {matrice[i][j]} visible ? {isVisible(matrice, (i, j))}")
    logger.info(f"tree interior visible: {result}")
    logger.info(f"tree border visible: {countTreesinBorder(matrice)}")
    return countTreesinBorder(matrice) + result

def maxScenicScore(matrice):
    scenicScoreList = []
    rowMatriceMax, colMatriceMax = np.shape(matrice)
    rowMatriceMin, colMatriceMin = 0,0
    for i in range(rowMatriceMin, rowMatriceMax):
        for j in range(colMatriceMin, colMatriceMax):
            scenicEvaluate = scenicScore(grid, (i, j))
            scenicScoreList.append(scenicEvaluate)
            logger.debug(f"tree: {(i, j)} vaut : {matrice[i][j]} - scenicscore: {scenicEvaluate}")
    return max(scenicScoreList)

def getTreeWithMaxScenicScore(matrice):
    dictOfTreeWithSceniceScore= {}
    rowMatriceMax, colMatriceMax = np.shape(matrice)
    rowMatriceMin, colMatriceMin = 0,0
    for i in range(rowMatriceMin, rowMatriceMax):
        for j in range(colMatriceMin, colMatriceMax):
            scenicEvaluate = scenicScore(matrice, (i, j))
            dictOfTreeWithSceniceScore[(i,j)] = scenicEvaluate
            logger.debug(f"tree: {(i, j)} vaut : {matrice[i][j]} - scenicscore: {scenicEvaluate}")
    logger.debug(f"dictOfTreeWithSceniceScore: {dictOfTreeWithSceniceScore}")
    return max(dictOfTreeWithSceniceScore, key=dictOfTreeWithSceniceScore.get)

def scenicUIOfTree(matrice,treePosition):
    listOfTrees = []
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    rowTree,colTree = treePosition
    treeSize = matrice[rowTree, colTree]

    # measuring Up
    if rowTree == rowMin:
        listOfTrees.append((rowTree,colTree))
    else:
        for e in range(rowTree, rowMin, -1):
            treeNeighborSize = matrice[e-1, colTree]
            if treeNeighborSize >= treeSize:
                listOfTrees.append((e-1, colTree))
                break
            else:
                listOfTrees.append((e-1, colTree))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")

    # measuring down
    if rowTree == rowMax-1:
        listOfTrees.append((rowTree, colTree))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")
    else:
        for e in range(rowTree, rowMax-1):
            treeNeighborSize = matrice[e + 1, colTree]
            if treeNeighborSize >= treeSize:
                listOfTrees.append((e+1, colTree))
                break
            else:
                listOfTrees.append((e+1, colTree))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")

    # measuring left
    if colTree == colMin:
        listOfTrees.append((rowTree,colTree))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")
    else:
        for e in range(colTree, colMin, -1):
            treeNeighborSize = matrice[rowTree, e - 1]
            if treeNeighborSize >= treeSize:
                listOfTrees.append((rowTree, e-1))
                break
            else:
                listOfTrees.append((rowTree, e-1))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")

    # measuring right
    if colTree == colMax - 1:
        listOfTrees.append((rowTree, colTree))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")
    else:
        for e in range(colTree, colMax -1):
            treeNeighborSize = matrice[rowTree, e + 1]
            if treeNeighborSize >= treeSize:
                listOfTrees.append((rowTree, e+1))
                break
            else:
                listOfTrees.append((rowTree, e+1))
        logger.debug(f"tree {treePosition} [{treeSize}] - listOfTrees: {listOfTrees}")
    return listOfTrees


def displayMatrice(matrice, window):
    forest = pygame.sprite.Group()
    rowMax, colMax = np.shape(matrice)
    rowMin, colMin = 0, 0
    space = 2
    marge = 5
    height = window.get_height()
    width = window.get_width()
    sizeCase = (height - ((2 * marge) + (space * rowMax))) // rowMax
    center_x = (abs(width - (rowMax * sizeCase + rowMax * space)) // 2 )
    center_y = (abs(height - (colMax * sizeCase + colMax * space)) // 2 )

    myfont = pygame.font.SysFont("", 15)

    logger.debug(f"init Display Matrice size {rowMax,colMax} sizeCase: {sizeCase} center: {center_x, center_y}")
    for i in range(rowMin, rowMax):
        caseCoordX = ((sizeCase+space) * i) + center_x
        for j in range(colMin, colMax):
            caseCoordY = ((sizeCase+space) * j) + center_y
            treeSize = matrice[i,j]
            color = (50, 28*treeSize, 0)
            #tree = pygame.draw.rect(window, color, Rect(caseCoordY, caseCoordX, sizeCase, sizeCase))
            tree = Tree(color,sizeCase,sizeCase,i,j,caseCoordX,caseCoordY,treeSize)
            logger.debug(f"tree.rect.size {tree.rect.size} tree.rect.center: {tree.rect.centery}")

            #label = myfont.render(str(treeSize), 1, (255, 255, 255))

            logger.debug(f"X,Y = ({tree.rect.x}, {tree.rect.y}) treeSize = {tree.getSize()} color = {tree.getColor()} i,j: {tree.getCoordX()},{tree.getCoordY()}")
            #tree.image.blit(label, (tree.rect.width/2, tree.rect.height/2))

            forest.add(tree)
            logger.debug(f"forest: {forest}")

    return forest

def getTreeSelected(listOfSprites):
    for e in listOfSprites:
        if e.isSelected():
            logger.debug(f"sprite get size: {e.getCoordX(), e.getCoordY()}")
            return (e.getCoordX(), e.getCoordY())

def selectTree(listOfSprites, treePosition):
    x,y = treePosition
    for e in listOfSprites:
        if e.getCoordX() == x and e.getCoordY() == y:
            e.setSelected(True)

def highlightScenicTree(spriteList, scenicList):
    logger.debug(f"scenicList : {scenicList}")
    for e in spriteList:
       # logger.debug(f"test : {e.}")
        if ((e.getCoordX(),e.getCoordY()) in scenicList):
            e.setHighlighted(True)


def reset(spriteList):
    for e in spriteList:
        e.reset()



######### main ########
def main():
    #file = "test.txt"
    file = "input.txt"
    grid = loadInput(file)
    print(grid)
    a = getTreeWithMaxScenicScore(grid)

    pygame.init()
    width, height = 1020,1020
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Forest")
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    all_trees = displayMatrice(grid, screen)
    all_trees.draw(screen)

    #boucle event
    while 1:
        pygame.time.Clock().tick(60)
        event_list = pygame.event.get()
        for event in event_list:  # On parcours la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                sys.exit()  # On quite le programme
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    maxTreeScenicScorePos = getTreeWithMaxScenicScore(grid)
                    selectTree(all_trees, maxTreeScenicScorePos)
                if event.key == pygame.K_r:
                    reset(all_trees)
        treeSelected = getTreeSelected(all_trees.sprites())
        if treeSelected:
            logger.info(f"treeSelected {treeSelected} ScenicList: {scenicUIOfTree(grid, treeSelected)}")
            highlightScenicTree(all_trees.sprites(), scenicUIOfTree(grid, treeSelected))
        else:
            reset(all_trees.sprites())

        all_trees.update(event_list)
        all_trees.draw(screen)
        pygame.display.flip()

#print(f" {scenicScore(grid, (3, 2))}")
#print(f"maxScenicScore(grid) : {maxScenicScore(grid)}")

if __name__ == '__main__':
    main()
    pg.quit()