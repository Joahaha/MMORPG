import pygame
from pygame.locals import *
from mysprite import mySprite

class Item(pygame.sprite.Sprite):

    def __init__(self, name, description, value,rarity,path,game):
        super().__init__()
        self.name = name
        self.description = description
        self.value = value
        self.rarity = rarity
        self.game = game
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        

    