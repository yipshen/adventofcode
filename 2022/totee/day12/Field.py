import pygame
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Field(pygame.sprite.Sprite):

    def __init__(self, color, altitude):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()
        self.image = pygame.Surface([2, 2])
        self.__currentColor = color
        self.__originColor = color
        self.image.fill(self.__currentColor)
        self.rect = self.image.get_rect()
        self.__altitude = altitude
        myfont = pygame.font.SysFont("", 15)
        self.__visited = False
        self.__distance = 10000
        self.__poids = 1
        self.__parent = "+"
        self.label = myfont.render("" + str(self.__altitude) + "|" + str(self.__distance) , 1, (0, 0, 0))


    def getParent(self):
        return self.__parent
    def setParent(self,p):
        self.__parent = p
    def resetFieldVisited(self):
        self.__visited = False
    def setVisited(self):
        self.__visited = True

    def isVisited(self):
        return self.__visited

    def getAltitude(self) -> int:
        return self.__altitude

    def setColor(self, color) -> None:
        self.__currentColor = color
        self.image.fill(self.__currentColor)

    def getCurrentColor(self):
        return self.__currentColor

    def getOriginColor(self):
        return self.__originColor

    def resetColor(self):
        self.__currentColor = self.__originColor
        self.image.fill(self.__currentColor)

    def refreshLabel(self):
        myfont = pygame.font.SysFont("", 15)
        self.label = myfont.render("" + str(self.__altitude) + "|" + str(self.__distance) , 1, (0, 0, 0))
        self.image.blit(self.label, (self.rect.width / 2, self.rect.height / 2))

    def updateLabel(self):
        self.image.blit(self.label, (self.rect.width / 2, self.rect.height / 2))

    def setLabel(self,message: str):
        myfont = pygame.font.SysFont("", 15)
        self.label = myfont.render(message , 1, (0, 0, 0))
        self.image.blit(self.label, (self.rect.width / 2, self.rect.height / 2))

    def getLig(self):
        return self.__lig

    def getCol(self):
        return self.__col

    def setLig(self,ligne):
        self.__lig = ligne

    def setCol(self,col):
        self.__col = col

    def setDistance(self,d):
        self.__distance = d

    def getDistance(self):
        return self.__distance

    def getPoids(self):
        return self.__poids
