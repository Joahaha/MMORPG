import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

class Inventory():
    def __init__(self,size,game):
        self.size = size
        self.game = game
        self.owner = self.game.player
        self.weapon_tab = []
        self.usable_item = []
        self.gold = self.owner.gold


    
