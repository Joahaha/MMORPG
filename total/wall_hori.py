import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Wall_hori(mySprite):
    def __init__(self, x, y, path):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (650, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
