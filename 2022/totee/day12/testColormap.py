import string
import sys

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

colorField = dict(zip(list(range(0, 28)), colorList))
mapLetterToLevel = dict(zip(string.ascii_lowercase,list(range(1,27))))
mapLetterToLevel['S'] = 0
mapLetterToLevel['E'] = 27

mapLevelToLetter = dict(zip(list(range(1, 27)), string.ascii_lowercase))
mapLevelToLetter[0] = 'S'
mapLevelToLetter[27] = 'E'

# print(f"{colorField}")
# print(f"{mapLetterLevel}")

def loadInput(input: str) -> np.array:
    with open(input, 'r') as f:
        firstLine = f.readline().strip()
        gridField = np.array([[mapLetterToLevel[x] for x in firstLine.strip()]])
        for line in f:
            a = [mapLetterToLevel[x] for x in line.strip()]
            gridField = np.vstack([gridField, a])

    return gridField


def displayMap(matrice, window):
    carte = pygame.sprite.Group()
    rowMax, colMax = np.shape(matrice)
    # rowMax, colMax = 2, 8
    rowMin, colMin = 0, 0
    space = 2
    marge = 2
    height = window.get_height()
    width = window.get_width()
    sizeCaseY = (height - ((2 * marge) + (space * rowMax))) // rowMax
    sizeCaseX = (width - ((2 * marge) + (space * colMax))) // colMax
    # sizeCase = 300
    center_x = (abs(height - (rowMax * sizeCaseY + rowMax * space)) // 2 )
    center_y = (abs(width - (colMax * sizeCaseX + colMax * space)) // 2 )

    myfont = pygame.font.SysFont("", 15)
    logger.debug(f"init Display Matrice size {rowMax, colMax} sizeCaseY: {sizeCaseY} sizeCaseX: {sizeCaseX}")
    # logger.debug(f"init Display Matrice size {rowMax,colMax} sizeCase: {sizeCase} center: {center_x, center_y}")
    for i in range(rowMin, rowMax):
        caseCoordY = ((sizeCaseY+space) * i) + center_x
        for j in range(colMin, colMax):
            caseCoordX = ((sizeCaseX+space) * j) + center_y
            fieldLevel = matrice[i, j]
            logger.debug(f"fieldHeight: {fieldLevel}")
            color = colorField[fieldLevel]

            logger.debug(f"matrice[{i},{j}]: {matrice[i, j]}")
            field = pygame.sprite.Sprite()
            field.image = pygame.Surface([sizeCaseX, sizeCaseY])
            field.image.fill(color)
            field.rect = field.image.get_rect()
            field.rect.x = caseCoordX
            field.rect.y = caseCoordY
            logger.debug(f"caseCoordY: {caseCoordY} caseCoordX: {caseCoordX}")
            logger.debug(f"{field.image.get_rect()} x: {field.rect.x} y: {field.rect.y}")
            # label = myfont.render(mapLevelToLetter[fieldLevel], 1, (0, 0, 0))
            label = myfont.render(str(fieldLevel), 1, (0, 0, 0))
            field.image.blit(label, (field.rect.width / 2, field.rect.height / 2))

            carte.add(field)
            logger.debug(f"carto: {carte}")
    return carte



pygame.init()
width, height = 1800,900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("test colormap")
# background = pygame.Surface(screen.get_size())
screen.fill((0, 0, 0))
# screen.blit(background, (0, 0))
# a = list("Sabqponm".strip())
# b = list("abcryxxl".strip())
# c = list("accszExk".strip())
# d = list("acctuvwj".strip())
# e = list("abdefghi".strip())
# # print(f"toto {a} {b}")
# grid = np.array([a, b, c, d, e])
#input = "test.txt"
input = "input.txt"
grid = loadInput(input)
print(f"carte: \n{grid}")
all_field = displayMap(grid, screen)
all_field.draw(screen)


while 1:
    pygame.time.Clock().tick(60)
    event_list = pygame.event.get()
    for event in event_list:  # On parcours la liste de tous les événements reçus
        if event.type == QUIT:  # Si un de ces événements est de type QUIT
            sys.exit()  # On quite le programme

    pygame.display.flip()