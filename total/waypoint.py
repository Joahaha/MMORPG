import pygame
from mysprite import mySprite

class Waypoint(mySprite):
    def __init__(self,x,y,path):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.avaiable = False