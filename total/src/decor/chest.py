import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Chest(mySprite):
    def __init__(self, x, y, path,loot,condition,game):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.condition = condition
        self.loot = loot
        self.possible_interaction='Press e to open'
        self.game = game

    def open(self,player):
        if self.condition(player):
            self.give()
            self.kill()

        else:
            self.possible_interaction = 'Press e to open(need password)'

    def kill(self):
            self.game.all_sprites.remove(self)
            self.game.chests.remove(self)
    def give_weapon(self):
        if self.loot[1] is not None:
            print(self.loot[1])
            self.game.player.inventory.add_weapon(self.loot[1])

    def give_usable_item(self):
        if self.loot[2] is not None:
            self.game.player.inventory.add_item(self.loot[2])

    def give_gold(self):
        if self.loot[0] is not None:
            print(self.loot[0])
            self.game.player.inventory.owner.gold+=self.loot[0]
    def give_unique(self):
        if self.loot[3] is not None:
            self.game.player.inventory.unique_item.append(self.loot[3])

    def give(self):
        self.give_gold()
        self.give_usable_item()
        self.give_weapon()
        self.give_unique()

    def show_interaction(self):
        pass
