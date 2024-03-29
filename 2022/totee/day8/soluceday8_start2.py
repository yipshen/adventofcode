import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#file = "test.txt"
file = "input.txt"

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

# support position is a couple (line,col)
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

grid = loadInput(file)

#print(f" {scenicScore(grid, (3, 2))}")
print(f"maxScenicScore(grid) : {maxScenicScore(grid)}")