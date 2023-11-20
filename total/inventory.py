import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

class Inventory():
    def __init__(self, size, game, owner):
        self.size = size
        self.game = game
        self.owner = owner
        self.weapon_tab = []
        self.usable_item = []
        self.rarity_tab = [(0,0,0),(0, 255, 0),(255, 0, 0),(0, 0, 255)]
        self.current_weapon = None
        #self.current_armor = None


    def add_weapon(self, weapon):
        if len(self.weapon_tab) < self.size:
            self.weapon_tab.append(weapon)
            self.current_weapon = weapon

    def remove_weapon(self, weapon):
        if weapon in self.weapon_tab:
            self.weapon_tab.remove(weapon)

    def add_item(self, item):
        if len(self.usable_item) < self.size:
            self.usable_item.append(item)

    def remove_item(self, item):    
        if item in self.usable_item:
            self.usable_item.remove(item)

    def display(self):
        inventory_surface = pygame.image.load('images/dq_background.png')
        inventory_surface = pygame.transform.scale(inventory_surface,(1000,800))


        if self.current_weapon == None:
            weapon_slot = pygame.image.load('images/weapon_slot.png')
            weapon_slot = pygame.transform.scale(weapon_slot,(50,50))
            inventory_surface.blit(weapon_slot, (600, 80))
        else:
            inventory_surface.blit(pygame.transform.scale(self.current_weapon.image,(50,50)),(600,80))
            color = self.rarity_tab[self.current_weapon.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(600,80, 50,50), 2) 

        font = pygame.font.Font(None, 30)
        weapon_names = [weapon.name for weapon in self.weapon_tab]
        item_names = [item.name for item in self.usable_item]

        weapon_text = font.render(f"Weapons: {', '.join(weapon_names)}", True, (255,255,255 ))
        item_text = font.render(f"Items: {', '.join(item_names)}", True, (255,255,255 ))
        gold_text = font.render(f"Gold: {self.owner.gold}", True, (255,255,255 ))
        atq_stat = font.render(f"Atq: {self.owner.atq}", True, (255,255,255 ))
        def_stat = font.render(f"Def: {self.owner.defense}", True, (255,255,255 ))

        inventory_surface.blit(weapon_text, (10, 10))
        inventory_surface.blit(item_text, (10, 50))
        inventory_surface.blit(gold_text, (10, 90))
        inventory_surface.blit(atq_stat, (10, 130))
        inventory_surface.blit(def_stat, (10, 170))
        for i, weapon in enumerate(self.weapon_tab):
            weapon_image = weapon.image 
            weapon_image = pygame.transform.scale(weapon_image, (50, 50)) 
            inventory_surface.blit(weapon_image, (10, 200 + i * 60)) 
            color = self.rarity_tab[weapon.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(10, 200 + i * 60, 50, 50), 2) 

        self.game.screen.blit(inventory_surface, (0, 0))    
        pygame.display.flip()