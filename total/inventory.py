import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

class Inventory():
    def __init__(self, size, game, owner):
        self.size = size
        self.game = game
        self.owner = owner
        self.weapon_tab = [self.game.weapons[1].name]
        self.usable_item = []


    def display(self):
        inventory_surface = pygame.image.load(self.game.backgrounds[self.game.current_map])
        inventory_surface = pygame.transform.scale(inventory_surface,(1000,800))

        font = pygame.font.Font(None, 30)
        weapon_text = font.render(f"Weapons: {', '.join(self.weapon_tab)}", True, (0, 0, 0))
        item_text = font.render(f"Items: {', '.join(self.usable_item)}", True, (0, 0, 0))
        gold_text = font.render(f"Gold: {self.owner.gold}", True, (0, 0, 0))

        inventory_surface.blit(weapon_text, (10, 10))
        inventory_surface.blit(item_text, (10, 50))
        inventory_surface.blit(gold_text, (10, 90))

        self.game.screen.blit(inventory_surface, (0, 0))
        pygame.display.flip()

    def add_weapon(self, weapon):
        if len(self.weapon_tab) < self.size:
            self.weapon_tab.append(weapon)

    def remove_weapon(self, weapon):
        if weapon in self.weapon_tab:
            self.weapon_tab.remove(weapon)

    def add_item(self, item):
        if len(self.usable_item) < self.size:
            self.usable_item.append(item)

    def remove_item(self, item):
        if item in self.usable_item:
            self.usable_item.remove(item)
