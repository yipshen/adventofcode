import pygame

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Tree(pygame.sprite.Sprite):
    def __init__(self, color, width, height, coordX, coordY, posX, posY, size):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.__size = size
        self.__coordX = coordX
        self.__coordY = coordY
        if self.__size == 9:
            self.__color = (255,0,0)
        else:
            self.__color = color
        self.clicked = False
        self.highlighted = False

    def setSize(self, size):
        self.__size = size

    def getSize(self):
        return self.__size

    def getColor(self):
        return self.__color

    def getCoordX(self):
        return self.__coordX

    def getCoordY(self):
        return self.__coordY

    def reset(self):
        self.image.fill(self.__color)
        self.clicked = False
        self.highlighted =False

    def setHighlighted(self, b):
        self.highlighted = b

    def isHighligthed(self):
        return self.highlighted
    def isSelected(self):
        return self.clicked

    def setSelected(self, value):
        self.clicked = value
    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    logger.debug(f" update() event : {event} treeSize: {self.getSize()} color: {self.getColor()}")
                    self.clicked = not self.clicked
                    self.highlighted = not self.highlighted
            if self.isHighligthed() or self.clicked:
                logger.debug(f"Tree Highlighted : {self.getCoordX(), self.getCoordY()}")
                self.image.fill((0, 0, 255))
            else:
                self.image.fill(self.__color)