import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


file = 'test.txt'
#file = "input.txt"

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
    (rowMax, colMax) = np.shape(matrice)
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


grid = loadInput(file)
#print(f"{grid}")
# print(f"tree (1,1) est visible : {isVisible(grid, (1,1))}")
# print(f"tree (1,3) est visible : {isVisible(grid, (1,3))}")
#
# assert isVisible(grid, (0, 1)) == True
# assert isVisible(grid, (4, 4)) == True
# assert isVisible(grid, (1, 1)) == True
# assert isVisible(grid, (1, 2)) == True
# assert isVisible(grid, (1, 3)) == False
# assert isVisible(grid, (2, 1)) == True
# assert isVisible(grid, (2, 2)) == False
# assert isVisible(grid, (2, 3)) == True
# assert isVisible(grid, (3, 1)) == False
# assert isVisible(grid, (3, 2)) == True
# assert isVisible(grid, (3, 3)) == False


# print(f"tree in border : {countTreesinBorder(grid)}")
print(f"soluce : {countTreeVisible(grid)}")