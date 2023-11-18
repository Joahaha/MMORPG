import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Wall_verti(mySprite):
    def __init__(self, x, y, path,loot,condition):
        super().__init__(x,y,path)
        self.condition = condition
        self.loot = loot

    def open(self,player):
        if self.condition(player):
            self.give(self,player)


    def give(self,player):
        player.stuff.append(self.loot)


