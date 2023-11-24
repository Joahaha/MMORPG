import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

class ExitLoops(Exception):
    pass
class Inventory():
    def __init__(self, size, game, owner):
        self.size = size
        self.game = game
        self.owner = owner
        self.weapon_tab = [self.game.weapons[1],self.game.weapons[3],self.game.weapons[2]]
        self.usable_item = [self.game.usable_items[3]]
        self.rarity_tab = [(0,0,0),(0, 255, 0),(255, 0, 0),(0, 0, 255)]
        self.current_weapon = None
        #self.current_armor = None
        self.selected_item_index = 0
        self.is_visible = False


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
    
    def handle_input(self, key):
        if key == K_TAB:
            self.is_visible = not self.is_visible
        elif key == K_DOWN and self.selected_item_index is not None:
            self.selected_item_index = (self.selected_item_index + 1) % len(self.weapon_tab + self.usable_item)
        elif key == K_UP and self.selected_item_index is not None:
            self.selected_item_index = (self.selected_item_index - 1) % len(self.weapon_tab + self.usable_item)
            
    def handle_upgrade(self, key):
        if self.owner.gold >= 100:
            if key == K_h:
                self.owner.base_health+=5
                self.owner.health +=5
                self.owner.gold -=100
            if key == K_j:
                self.owner.base_range+=5
                self.owner.gold -= 100
            
        
    def set_as_current_weapon(self, id):
        self.current_weapon = self.weapon_tab[id]
        self.weapon_tab[id] = self.current_weapon
    
    

    def help_display(self,inventory_surface):
        if self.owner.health >= self.owner.base_health:
            self.owner.health = self.owner.base_health
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

        weapon_text = font.render(f"Weapons: {', '.join(weapon_names)}", True, (135,255,255 ))
        item_text = font.render(f"Items: {', '.join(item_names)}", True, (135,255,255 ))
        gold_text = font.render(f"Gold: {self.owner.gold}", True, (135,255,255 ))
        atq_stat = font.render(f"Atq: {self.owner.atq}+{self.weapon_tab[self.selected_item_index].damage}", True, (135,255,255 ))
        def_stat = font.render(f"Def: {self.owner.defense}", True, (135,255,255 ))
        range = font.render(f"Range : '{self.owner.attack_range}+{self.weapon_tab[self.selected_item_index].range}range'", True, (135,255,255 ))
        hp = font.render(str(self.owner.health), True, (255, 0, 0))
        mana = font.render(str(self.owner.mana), True, (0, 0, 255))
        if self.selected_item_index < len(self.weapon_tab):
            description = font.render(f"Description : '{self.weapon_tab[self.selected_item_index].description}'", True, (135,255,255 ))
    
        else:
            description = font.render(f"Description :'{self.usable_item[self.selected_item_index - len(self.weapon_tab)].description}'", True,(135,255,255 ))
          
        inventory_surface.blit(weapon_text, (10, 10))

        inventory_surface.blit(item_text, (10, 50))
        inventory_surface.blit(gold_text, (10, 90))
        inventory_surface.blit(atq_stat, (10, 130))
        inventory_surface.blit(def_stat, (10, 170))
        inventory_surface.blit(description, (10, 210))
        inventory_surface.blit(range, (10, 250))
        inventory_surface.blit(mana, (800, 750))
        inventory_surface.blit(hp, (800, 700))
        for i, weapon in enumerate(self.weapon_tab):
            weapon_image = weapon.image 
            weapon_image = pygame.transform.scale(weapon_image, (50, 50)) 
            inventory_surface.blit(weapon_image, (10, 250 + i * 60)) 
            color = self.rarity_tab[weapon.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(10, 250 + i * 60, 50, 50), 2) 
        arrow = pygame.image.load('images/arrow1.png')
        arrow = pygame.transform.scale(arrow, (50, 50))
        if len(self.usable_item)==0 or self.selected_item_index < len(self.weapon_tab)  :
            inventory_surface.blit(arrow, (70, 250 + self.selected_item_index * 60))
        else:
            inventory_surface.blit(arrow, (240, 250 + (self.selected_item_index - len(self.weapon_tab)) * 60))
        for i, item in enumerate(self.usable_item):
            item_image = item.image 
            item_image = pygame.transform.scale(item_image, (50, 50)) 
            inventory_surface.blit(item_image, (180, 250 + i * 60)) 
            color = self.rarity_tab[item.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(180, 250 + i * 60, 50, 50), 2)
        self.game.screen.blit(inventory_surface, (0, 0))    
        pygame.display.flip()

    def display(self):
        inventory_surface = pygame.image.load('images/dq_background.png')
        inventory_surface = pygame.transform.scale(inventory_surface,(1000,800))
        self.help_display(inventory_surface) 
        running = True
        while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                            self.handle_input(event.key)
                            inventory_surface.blit(pygame.transform.scale(pygame.image.load('images/dq_background.png'),(1000,800)), (0,0))
                            self.help_display(inventory_surface)
                        
                        if event.key == pygame.K_RETURN:
                            if self.selected_item_index < len(self.weapon_tab):
                                if self.current_weapon is not None and self.current_weapon.name == self.weapon_tab[self.selected_item_index].name:
                                    self.current_weapon = None
                                    self.owner.atq = self.owner.base_atq
                                else:
                                    self.set_as_current_weapon(self.selected_item_index)
                                    self.owner.atq = self.owner.base_atq + self.current_weapon.damage if self.current_weapon is not None else self.owner.base_atq
                                    self.owner.attack_range = self.owner.base_range + self.current_weapon.range if self.current_weapon is not None else self.owner.base_range
                                inventory_surface.blit(pygame.transform.scale(pygame.image.load('images/dq_background.png'),(1000,800)), (0,0))
                                self.help_display(inventory_surface)
                        
                            else:
                                self.usable_item[self.selected_item_index - len(self.weapon_tab)].use()
                                self.remove_item(self.usable_item[self.selected_item_index - len(self.weapon_tab)])
                                if len(self.usable_item) == 0:
                                    self.selected_item_index = 0

                                inventory_surface.blit(pygame.transform.scale(pygame.image.load('images/dq_background.png'),(1000,800)), (0,0))
                                self.help_display(inventory_surface)
                        if event.key == pygame.K_j or event.key == pygame.K_h:
                            self.handle_upgrade(event.key)
                            inventory_surface.blit(pygame.transform.scale(pygame.image.load('images/dq_background.png'),(1000,800)), (0,0))
                            self.help_display(inventory_surface)

                        if event.key == pygame.K_ESCAPE:
                            self.is_visible = False
                            running = False