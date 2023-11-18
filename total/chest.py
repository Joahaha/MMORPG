import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Chest(mySprite):
    def __init__(self, x, y, path,loot,condition):
        super().__init__(x,y,path)
        self.condition = condition
        self.loot = loot
        self.possible_interaction=''

    def open(self,player):
        if self.condition(player):
            self.give(self,player)

    def show_interaction(self):
        text = "Press e to open"
        text += self.action_names[self.current_id]
        self.possible_interaction= text

    def give_weapon(self):
        self.game.inventory.weapon_tab.append(self.loot[0])

    def give_usable_item(self):
        self.game.inventory.usable_item_tab.append(self.loot[1])

    def give_gold(self):
        self.game.inventory.gold+=self.loot[2]



