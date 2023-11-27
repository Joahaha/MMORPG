import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Wall_verti(mySprite):
    def __init__(self, x, y, path,size_x,size_y,game):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def kill(self):
        self.game.all_sprites.remove(self)
        self.game.all_walls.remove(self)