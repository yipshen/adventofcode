import logging

import numpy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)


ZooM=9
def initMatrice(nbRow, nbCol):
    resultat = np.full((nbRow, nbCol), fill_value=".", dtype=list)
    return resultat

def initMatricewithSpoint(nbRow, nbCol, SPosition):
    resultat = np.full((nbRow, nbCol), fill_value=list("."), dtype=list)
    resultat[SPosition]=['s']
    return resultat

def initMatriceCustom(nbRow, nbCol, Hpos, Tpos):
    resultat = np.full((nbRow, nbCol), fill_value=".", dtype=list)
    resultat[Hpos] = 'H'
    resultat[Tpos] = 'T'
    return resultat


def loadInput(fileInput):
    listMoves = []
    rowMax, colMax = 0,0
    rowMin, colMin = 0,0
    rowCurrent,colCurrent = 0,0
    with open(fileInput, "r") as f:
        for line in f:
            direction = line.split()[0]
            step = int(line.split()[1])

            if direction == 'R':
                colCurrent += step
                if colCurrent > colMax:
                    colMax = colCurrent

            elif direction == 'L':
                colCurrent -= step
                if colCurrent < colMin:
                    colMin = colCurrent

            elif direction == 'U':
                rowCurrent += step
                if rowCurrent > rowMax:
                    rowMax = rowCurrent

            elif direction == 'D':
                rowCurrent -= step
                if rowCurrent < rowMin:
                    rowMin = rowCurrent


            listMoves.append(line.split())
        logger.debug(f"listMoves: {listMoves} \n rowMax: {rowMax} colMax: {colMax} rowMin: {rowMin} colMin: {colMin}")

    return (rowMax, colMax, rowMin, colMin ,listMoves)

def isCover(HPos,TPos):
    #return (HPos[0] == TPos[0]) and (HPos[1] == TPos[1])
    return HPos == TPos

def zoomMatrice(matrice, zoomPos, zoomSize):
    rowMax, colMax = np.shape(matrice)
    rowZoom, colZoom = zoomPos
    if (rowZoom - zoomSize) < 0 :
        row_lwr = 0
    else:
        row_lwr = rowZoom - zoomSize

    if (colZoom - zoomSize) < 0 :
        col_lwr = 0
    else:
        col_lwr = colZoom - zoomSize

    if (rowZoom + zoomSize) > rowMax :
        row_upp = rowMax
    else:
        row_upp = rowZoom + zoomSize

    if (colZoom + zoomSize) > colMax :
        col_upp = colMax
    else:
        col_upp = colZoom + zoomSize
    return matrice[row_lwr:row_upp, col_lwr:col_upp]

def zoomPosition(matrice: np.array, coordsPoint: (int,int), zoomSize: int) -> (int, int, int, int):
    rowMax, colMax = np.shape(matrice)
    rowZoom, colZoom = coordsPoint

    if (rowZoom - zoomSize) < 0:
        row_lwr = 0
    else:
        row_lwr = rowZoom - zoomSize

    if (colZoom - zoomSize) < 0:
        col_lwr = 0
    else:
        col_lwr = colZoom - zoomSize

    if (rowZoom + zoomSize) > rowMax:
        row_upp = rowMax
    else:
        row_upp = rowZoom + zoomSize

    if (colZoom + zoomSize) > colMax:
        col_upp = colMax
    else:
        col_upp = colZoom + zoomSize
    logger.debug(f"zoomPosition: ({row_lwr},{col_lwr}),({row_upp},{col_upp})")
    return (row_lwr, col_lwr, row_upp, col_upp)


def moveTail(head, tail):
    Hrow, Hcol = head["coordX"], head["coordY"]
    Trow, Tcol = tail["coordX"], tail["coordY"]

    if Hrow == Trow:
        if Tcol > Hcol and (Tcol - Hcol) > 1:
            Tcol -= 1
        else:
            if abs(Tcol - Hcol) > 1:
                Tcol += 1

    elif Hcol == Tcol:
        if Trow > Hrow and (Trow - Hrow) > 1:
            Trow -= 1
        else:
            if abs(Trow - Hrow) > 1:
                Trow += 1

    elif Hrow < Trow and Hcol > Tcol and ((Hcol - Tcol) > 1 or (Trow - Hrow) > 1):
        # H en haut a droite
        Trow -= 1
        Tcol += 1
    elif Hrow > Trow and Hcol > Tcol and ((Hcol - Tcol) > 1 or (Hrow - Trow) > 1):
        # H en bas a droite
        Trow += 1
        Tcol += 1
    elif Hrow < Trow and Hcol < Tcol and ((Tcol - Hcol) > 1 or (Trow - Hrow) > 1):
        # H en haut gauche
        Trow -= 1
        Tcol -= 1
    elif Hrow > Trow and Hcol < Tcol and ((Tcol - Hcol) > 1 or (Hrow - Trow) > 1):
        # H en bas gauche
        Trow += 1
        Tcol -= 1
    return (Trow, Tcol)

def moveHeader(head, direction):
    newhead = head
    if direction == 'R':
        newhead = (newhead["coordX"], newhead["coordY"]+1)
    elif direction == 'L':
        newhead = (newhead["coordX"], newhead["coordY"]-1)
    elif direction == 'U':
        newhead = (newhead["coordX"]-1, newhead["coordY"])
    elif direction == 'D':
        newhead = (newhead["coordX"]+1, newhead["coordY"])

    return newhead

def updateMatrice(matrice, headCur, tailCur, headNw, tailNw):

    headCurPos = (headCur["coordX"], headCur["coordY"])
    tailCurPos = (tailCur["coordX"], tailCur["coordY"])
    headNewPos = (headNw["coordX"], headNw["coordY"])
    tailNewPos = (tailNw["coordX"], tailNw["coordY"])

    logger.debug(f"updateMatrice : headCurPos: {headCur['value']}{headCurPos} headNewPos: {headNw['value']}{headNewPos}  tailCurPos: {tailCur['value']}{tailCurPos} tailNewPos: {tailNw['value']}{tailNewPos}")

    if isinstance(matrice[headCurPos], str):
        matrice[headCurPos] = '.'
    else:
        matrice[headCurPos].remove(headCur["value"])

    if isinstance(matrice[headNewPos], str):
        matrice[headNewPos] = headNw["value"]
    else:
        matrice[headNewPos].append(headNw["value"])

    if tailCurPos != tailNewPos:
        if isinstance(matrice[tailCurPos],str):
            matrice[tailCurPos] = "."
        else:
            matrice[tailCurPos].remove(tailCur["value"])

        if isinstance(matrice[tailNewPos], str):
            matrice[tailNewPos] = tailNw["value"]
        else:
            matrice[tailNewPos].append(tailNw["value"])


def updateMatriceHeader(matrice, headCur, headNw):
    headCurPos = (headCur["coordX"], headCur["coordY"])
    headNewPos = (headNw["coordX"], headNw["coordY"])

    logger.debug(f"updateMatriceHeader :headCurPos: {headCur['value']}{headCurPos} headNewPos: {headNw['value']}{headNewPos}")

    if isinstance(matrice[headCurPos], str):
        matrice[headCurPos] = '.'
    else:
        matrice[headCurPos].remove(headCur["value"])

    if isinstance(matrice[headNewPos], str):
        matrice[headNewPos] = headNw["value"]
    else:
        matrice[headNewPos].append(headNw["value"])

def updateMatriceTail(matrice, tailCur, tailNw):
    tailCurPos = (tailCur["coordX"], tailCur["coordY"])
    tailNewPos = (tailNw["coordX"], tailNw["coordY"])
    logger.debug(f"updateMatriceTail : tailCurPos: {tailCur['value']}{tailCurPos} tailNewPos: {tailNw['value']}{tailNewPos}")
    if tailCurPos != tailNewPos:
        if isinstance(matrice[tailCurPos],str):
            matrice[tailCurPos] = "."
        else:
            matrice[tailCurPos].remove(tailCur["value"])

        if isinstance(matrice[tailNewPos], str):
            matrice[tailNewPos] = tailNw["value"]
        else:
            matrice[tailNewPos].append(tailNw["value"])
def debugMatrice(matrice: np.array, zone: (int, int, int, int) )-> None:
    rowMin, colMin, rowMax, colMax = zone
    rowNewMatrice = rowMax - rowMin
    colNewMatrice = colMax - colMin
    matriceShape = matrice[rowMin:rowMax,colMin:colMax]
    logger.debug(f"debugMatrice: rowNewMatrice: {rowNewMatrice} colNewMatrice: {colNewMatrice} zone: {zone}")
    m = np.full((rowNewMatrice,colNewMatrice), '.', dtype=str)
    for i in range(0,rowNewMatrice):
        for j in range(0,colNewMatrice):
            if isinstance(matriceShape[i, j], list):
                if 'H' in matriceShape[i, j]:
                    m[i, j] = 'H'
                elif '1' in matriceShape[i, j]:
                    m[i, j] = '1'
                elif '2' in matriceShape[i, j]:
                    m[i, j] = '2'
                elif '3' in matriceShape[i, j]:
                    m[i, j] = '3'
                elif '4' in matriceShape[i, j]:
                    m[i, j] = '4'
                elif '5' in matriceShape[i, j]:
                    m[i, j] = '5'
                elif '6' in matriceShape[i, j]:
                    m[i, j] = '6'
                elif '7' in matriceShape[i, j]:
                    m[i, j] = '7'
                elif '8' in matriceShape[i, j]:
                    m[i, j] = '8'
                elif '9' in matriceShape[i, j]:
                    m[i, j] = '9'
                elif 'S' in matriceShape[i, j]:
                    m[i, j] = 'S'
            else:
                m[i, j] = matriceShape[i, j]
    return m

def moveHeaderNTail(matrice:numpy.array, head:dict, tail:dict, start:dict, move: str) -> (dict, dict, list, list):
    direction = move[0]
    step = int(move[1])

    listHmoves, listTmoves = [], []

    for iter in range(step):
        headCurrent = dict(head)
        tailCurrent = dict(tail)
        head["coordX"],head["coordY"] = moveHeader(head, direction)
        tail["coordX"], tail["coordY"] = moveTail(head, tail)
        headNew = head
        tailNew = tail
        updateMatrice(matrice, headCurrent, tailCurrent, headNew, tailNew)
        logger.debug(f"moveHaderNTail \n{debugMatrice(matrice,zoomPosition(matrice,(head['coordX'],head['coordY']),ZooM))}")
        #logger.debug(f"\n{matrice}")
        listHmoves.append((head["coordX"],head["coordY"]))
        listTmoves.append((tail["coordX"],tail["coordY"]))

    return listHmoves, listTmoves


def moveHeaderNTail2(matrice:numpy.array, head:dict, listoftail:list, start:dict, move: str) -> (list, list):
    direction = move[0]
    step = int(move[1])

    listHmoves, listTmoves = [], []

    for iter in range(step):
        headCurrent = dict(head)
        head["coordX"],head["coordY"] = moveHeader(head, direction)
        headNew = head
        updateMatriceHeader(matrice, headCurrent, headNew)
        listHmoves.append((head["coordX"], head["coordY"]))
        # tail["coordX"], tail["coordY"] = moveTail(head, tail)
        for i in range(0,len(listoftail)):
            tailCurrent = dict(listoftail[i])
            if i == 0:
                listoftail[i]["coordX"], listoftail[i]["coordY"] = moveTail(head, listoftail[i])
            else:
                listoftail[i]["coordX"], listoftail[i]["coordY"] = moveTail(listoftail[i-1], listoftail[i])

            tailNew = listoftail[i]
            updateMatriceTail(matrice, tailCurrent, tailNew)
            if i == 8:
                listTmoves.append((listoftail[i]["coordX"],listoftail[i]["coordY"]))
                #logger.debug(f"moveHeaderNTail2 \n{debugMatrice(matrice, zoomPosition(matrice, (head['coordX'], head['coordY']), ZooM))}")

    return listHmoves, listTmoves


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
                elif '1' in matriceShape[i,j]:
                    m[i, j] = '1'
                elif '2' in matriceShape[i,j]:
                    m[i, j] = '2'
                elif '3' in matriceShape[i,j]:
                    m[i, j] = '3'
                elif '4' in matriceShape[i,j]:
                    m[i, j] = '4'
                elif '5' in matriceShape[i,j]:
                    m[i, j] = '5'
                elif '6' in matriceShape[i,j]:
                    m[i, j] = '6'
                elif '7' in matriceShape[i,j]:
                    m[i, j] = '7'
                elif '8' in matriceShape[i,j]:
                    m[i, j] = '8'
                elif '9' in matriceShape[i,j]:
                    m[i, j] = '9'
                elif 'S' in matriceShape[i,j]:
                    m[i, j] = 'S'
            else:
                m[i, j] = matriceShape[i, j]
    print(f"{m}")


def main():
    #file = 'test2.txt'
    #file = 'test.txt'
    file = 'input.txt'

    (rowMax, colMax, rowMin, colMin, listMoves) = loadInput(file)

    m = initMatrice(rowMax+abs(rowMin)+4, colMax + abs(colMin)+4)
    #m = initMatricewithSpoint(rowMax+abs(rowMin)+4, colMax + abs(colMin)+4, (rowMax, abs(colMin)))
    #Hinit = (rowMax, abs(colMin))
    header = {"value": 'H', "coordX": rowMax, "coordY": abs(colMin)}
    start = {"value": 'S', "coordX": rowMax, "coordY": abs(colMin)}
    listOfTails = []
    #tail = {"value": 'T', "coordX": rowMax, "coordY": abs(colMin)}
    for i in range(1,10):
        listOfTails.append({"value":str(i), "coordX": rowMax, "coordY": abs(colMin)})

    m[rowMax, abs(colMin)] = []
    m[rowMax, abs(colMin)].insert(0, start["value"])
    #m[rowMax, abs(colMin)].insert(0, tail["value"])
    for i in range(0,9):
        m[rowMax, abs(colMin)].append(listOfTails[i]["value"])
    m[rowMax, abs(colMin)].insert(0,header["value"])

    #print(m)
    #zrowMin, zcolMin, zrowMax, zcolMax = zoomPosition(m,Hinit,ZooM)
    #zoomFieldPointH = zoomPosition(m,(header["coordX"],header["coordY"]),ZooM)
    #printMatrice(m,zoomFieldPointH)
    #print(f"{m} \n type(m[4,0]) :{type(m[4,0])}" )

    Tvisited = [(rowMax, abs(colMin))]
    Hvisited = []
    for cpt,move in enumerate(listMoves):
        logger.debug(f"move : {move}")
        HMoves, Tmoves = moveHeaderNTail2(m, header, listOfTails, start, move)
        logger.debug(f"{debugMatrice(m, zoomPosition(m, (header['coordX'], header['coordY']), ZooM))}")
        Hvisited += HMoves
        Tvisited += Tmoves

       # logger.debug(f"======== Hvisited : {Hvisited} \n len(Hvisited): {len(Hvisited)} moveNumber: {cpt}")
       # logger.debug(f"======== Tvisited : {Tvisited} \n len(Tvisited): {len(Tvisited)} moveNumber: {cpt}")

    setTvisited = set(Tvisited)
    print(f"setTvisited : {setTvisited} \n len(setTvisited): {len(setTvisited)}")

    return 0


if __name__ == '__main__':
    main()