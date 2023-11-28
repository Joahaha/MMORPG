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
        self.unique_item = []
        self.rarity_tab = [(0,0,0),(0, 255, 0),(255, 0, 0),(0, 0, 255)]
        self.current_weapon = None
        #self.current_armor = None
        self.selected_item_index = 0
        self.is_visible = False
        self.weapon_slot = pygame.transform.scale(pygame.image.load('images/inventory/weapon_slot.png'), (50,50))
        self.arrow = pygame.transform.scale(pygame.image.load('images/inventory/arrow1.png'), (50, 50))
        self.font = pygame.font.Font(None, 30)



    def add_weapon(self, weapon):
        if weapon is not None:
            if len(self.weapon_tab) < self.size:
                self.weapon_tab.append(weapon)

    def remove_weapon(self, weapon):
        if weapon in self.weapon_tab:
            self.weapon_tab.remove(weapon)

    def add_item(self, item):
        if item is not None:
            if len(self.usable_item) < self.size:
                self.usable_item.append(item)
    def add_unique(self, unique):
        if unique is not None:
            if len(self.unique_item) < self.size:
                self.unique_item.append(unique)

    def remove_item(self, item):    
        if item in self.usable_item:
            self.usable_item.remove(item)
    
    def handle_input(self, key):
        if key == K_TAB:
            self.is_visible = not self.is_visible
        elif key == K_DOWN and self.selected_item_index is not None:
            self.selected_item_index = (self.selected_item_index + 1) % len(self.weapon_tab + self.usable_item + self.unique_item)
        elif key == K_UP and self.selected_item_index is not None:
            self.selected_item_index = (self.selected_item_index - 1) % len(self.weapon_tab + self.usable_item + self.unique_item)
    
            
    def handle_upgrade(self, key):
        if self.owner.gold >= 100:
            if key == K_h:
                self.owner.base_health+=5
                self.owner.health +=5
                self.owner.gold -=100
            if key == K_j:
                self.owner.base_range+=5
                self.owner.gold -= 100
            
    def display_current_quest(self,inventory_surface):
        for i, quest in enumerate(self.owner.on_going_quest):
            if quest is not None: 
                quest_active = self.font.render(f"Quest: {quest.name}", True, (135,255,255 ))
                inventory_surface.blit(quest_active, (600,300 + i * 30))

    def set_as_current_weapon(self, id):
        self.current_weapon = self.weapon_tab[id]
        self.weapon_tab[id] = self.current_weapon
    
    def check_health(self):
        if self.owner.health >= self.owner.base_health:
            self.owner.health = self.owner.base_health
    
    def display_current_weapon(self,inventory_surface):
        if self.current_weapon == None:
            inventory_surface.blit(self.weapon_slot, (600, 80))
        else:
            inventory_surface.blit(pygame.transform.scale(self.current_weapon.image,(50,50)),(600,80))
            color = self.rarity_tab[self.current_weapon.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(600,80, 50,50), 2) 

    def display_weapons(self,inventory_surface):
        weapon_names = [weapon.name for weapon in self.weapon_tab]
        item_names = [item.name for item in self.usable_item]
        unique_names = [unique.name for unique in self.unique_item]

        weapon_text = self.font.render(f"Weapons: {', '.join(weapon_names)}", True, (135,255,255 ))
        item_text = self.font.render(f"Items: {', '.join(item_names)}", True, (135,255,255 ))
        unique_text = self.font.render(f"Unique {', '.join(unique_names)}", True, (135,255,255))
        gold_text = self.font.render(f"Gold: {self.owner.gold}", True, (135,255,255 ))
        if self.selected_item_index < len(self.weapon_tab):
            if self.current_weapon is not None and self.current_weapon.name == self.weapon_tab[self.selected_item_index].name:
                atq_stat = self.font.render(f"Atq: {self.owner.atq}", True, (135,255,255 ))
            else:
                atq_stat = self.font.render(f"Atq: {self.owner.atq}+{self.weapon_tab[self.selected_item_index].damage}", True, (135,255,255 ))
        else: 
             atq_stat = self.font.render(f"Atq: {self.owner.atq}", True, (135,255,255 ))
        def_stat = self.font.render(f"Def: {self.owner.defense}", True, (135,255,255 ))
        if self.selected_item_index < len(self.weapon_tab):
            if self.current_weapon is not None and self.current_weapon.name == self.weapon_tab[self.selected_item_index].name:
                range = self.font.render(f"Range : {self.owner.attack_range}", True, (135,255,255 ))
            else:
                range = self.font.render(f"Range : {self.owner.attack_range}+{self.weapon_tab[self.selected_item_index].range}range", True, (135,255,255 ))
        else: 
             range = self.font.render(f"Range : {self.owner.attack_range}", True, (135,255,255 ))
        hp = self.font.render(str(self.owner.health), True, (255, 0, 0))
        mana = self.font.render(str(self.owner.mana), True, (0, 0, 255))
        if self.selected_item_index < len(self.weapon_tab):
            description = self.font.render(f"Description : '{self.weapon_tab[self.selected_item_index].description}'", True, (135,255,255 ))
        elif self.selected_item_index < len(self.weapon_tab) + len(self.usable_item):
            description = self.font.render(f"Description :'{self.usable_item[self.selected_item_index - len(self.weapon_tab)].description}'", True,(135,255,255 ))
        elif self.selected_item_index < len(self.weapon_tab) + len(self.usable_item) + len(self.unique_item):
            description = self.font.render(f"Description :'{self.unique_item[self.selected_item_index - len(self.weapon_tab)-len(self.usable_item)].description}'", True,(135,255,255 ))
        else:
            description = self.font.render("No item selected", True, (135,255,255))
          
        inventory_surface.blit(weapon_text, (10, 10))
        inventory_surface.blit(item_text, (10, 50))
        inventory_surface.blit(unique_text, (10, 90))
        inventory_surface.blit(gold_text, (10, 130))
        inventory_surface.blit(atq_stat, (10, 170))
        inventory_surface.blit(def_stat, (120, 170))
        inventory_surface.blit(description, (10, 210))
        inventory_surface.blit(range, (10, 250))
        inventory_surface.blit(mana, (800, 750))
        inventory_surface.blit(hp, (800, 700))

        for i, weapon in enumerate(self.weapon_tab):
            weapon_image = weapon.image 
            weapon_image = pygame.transform.scale(weapon_image, (50, 50)) 
            inventory_surface.blit(weapon_image, (10, 290 + i * 60)) 
            color = self.rarity_tab[weapon.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(10, 290 + i * 60, 50, 50), 2) 
        if len(self.usable_item)==0 or self.selected_item_index < len(self.weapon_tab)  :
            inventory_surface.blit(self.arrow, (70, 290 + self.selected_item_index * 60))
        elif self.selected_item_index < len(self.weapon_tab) + len(self.usable_item):
            inventory_surface.blit(self.arrow, (240, 290 + (self.selected_item_index - len(self.weapon_tab)) * 60))
        else:
            inventory_surface.blit(self.arrow, (410, 290 + (self.selected_item_index - len(self.weapon_tab) - len(self.usable_item)) * 60))
        for i, item in enumerate(self.usable_item):
            item_image = item.image 
            item_image = pygame.transform.scale(item_image, (50, 50)) 
            inventory_surface.blit(item_image, (180, 290 + i * 60)) 
            color = self.rarity_tab[item.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(180, 290 + i * 60, 50, 50), 2)
        for i, unique in enumerate(self.unique_item):
            unique_image = unique.image 
            unique_image = pygame.transform.scale(unique_image, (50, 50)) 
            inventory_surface.blit(unique_image, (350, 290 + i * 60)) 
            color = self.rarity_tab[item.rarity]
            pygame.draw.rect(inventory_surface, color, pygame.Rect(350, 290 + i * 60, 50, 50), 2)
        self.game.screen.blit(inventory_surface, (0, 0))    
        pygame.display.flip()

    def help_display(self,inventory_surface):
        self.check_health()
        self.display_current_quest(inventory_surface)
        self.display_current_weapon(inventory_surface)
        self.display_weapons(inventory_surface)


    def display(self):
        inventory_surface = pygame.transform.scale(self.game.dq_background,(1000,800))
        self.help_display(inventory_surface) 
        running = True
        while running:
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                            self.handle_input(event.key)
                            inventory_surface.blit(self.game.dq_background, (0,0))
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
                                inventory_surface.blit(self.game.dq_background, (0,0))
                                self.help_display(inventory_surface)
                        
                            elif self.selected_item_index < len(self.weapon_tab)+ len(self.usable_item):
                                self.usable_item[self.selected_item_index - len(self.weapon_tab)].use()
                                self.remove_item(self.usable_item[self.selected_item_index - len(self.weapon_tab)])
                                if len(self.usable_item) == 0:
                                    self.selected_item_index = 0
                                inventory_surface.blit(self.game.dq_background, (0,0))
                                self.help_display(inventory_surface)
                            else:
                                inventory_surface.blit(self.game.dq_background, (0,0))
                                self.help_display(inventory_surface)
                        if event.key == pygame.K_j or event.key == pygame.K_h:
                            self.handle_upgrade(event.key)
                            inventory_surface.blit(self.game.dq_background, (0,0))
                            self.help_display(inventory_surface)

                        if event.key == pygame.K_ESCAPE:
                            self.is_visible = False
                            running = False