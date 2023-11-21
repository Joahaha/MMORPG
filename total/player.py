import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite
from inventory import Inventory

class Player(mySprite):
    def __init__(self,game,speed=4):
        super().__init__(483,600,'images/mc_sprite_sheet.png')
        self.frame_width = 64
        self.frame_height = 53
        self.current_direction ='standing'
        self.gap_height = 13
        self.frames = {
            'up': [self.image.subsurface(pygame.Rect(i * self.frame_width, 0 * (self.frame_height + self.gap_height)+self.gap_height-8, self.frame_width, self.frame_height)) for i in range(9)],
            'left': [self.image.subsurface(pygame.Rect(i * self.frame_width, 1 * (self.frame_height + self.gap_height), self.frame_width, self.frame_height+10)) for i in range(9)],
            'down': [self.image.subsurface(pygame.Rect(i * self.frame_width, 2 * (self.frame_height + self.gap_height), self.frame_width, self.frame_height)) for i in range(9)],
            'right': [self.image.subsurface(pygame.Rect(i * self.frame_width, 3 * (self.frame_height + self.gap_height), self.frame_width, self.frame_height)) for i in range(9)],
            'standing':[self.image.subsurface(pygame.Rect( self.frame_width, 2 * (self.frame_height + self.gap_height), self.frame_width, self.frame_height)) for i in range(9)],
        }
        self.rect = self.frames[self.current_direction][0].get_rect()
        self.rect.width = 50
        self.rect.height = 50
        self.rect.x = 483
        self.rect.y = 600
        self.speed = speed
        self.game = game
        self.basespeed = speed
        self.e_key_released = True
        self.go_next = True
        self.text=''
        self.voisin=''
        self.quest = False
        self.on_going_quest = [None] * 10
        self.gun = False
        self.nb_voisin = self.game.nb_voisins[self.game.current_map]
        self.key = False
        self.temp_x = 0
        self.temp_y = 0
        self.gold = 0
        self.inventory_open = False
        self.inventory = Inventory(10, game,self)
        self.base_atq = 10
        self.base_defense = 10 
        self.health = 100
        self.mana = 100

    def handle_movement(self, pressed_keys):
        if not self.inventory_open  :
            if pressed_keys[K_q] and self.rect.x - self.speed > 0 :
                self.rect.x -= self.speed
                self.current_direction = 'left'
                self.check_collision('x', self.game.fake_houses)
                self.check_collision('x', self.game.all_walls)
            if pressed_keys[K_d] and self.rect.x + self.speed < self.game.width-50 :
                self.rect.x += self.speed
                self.current_direction = 'right'
                self.check_collision('x', self.game.fake_houses)
                self.check_collision('x', self.game.all_walls)
            if pressed_keys[K_z]  and self.rect.y - self.speed > 0:  
                self.rect.y -= self.speed
                self.current_direction = 'up'
                self.check_collision('y', self.game.fake_houses)
                self.check_collision('y', self.game.all_walls)
            if pressed_keys[K_s] and self.rect.y +self.speed < self.game.height-50 :
                self.rect.y += self.speed
                self.current_direction = 'down'
                self.check_collision('y', self.game.fake_houses)
                self.check_collision('y', self.game.all_walls)
    def handle_npc_interaction(self, pressed_keys, hit_npc):
        if pressed_keys[K_e] and hit_npc and self.e_key_released:
            for npc in hit_npc:
                self.interaction(npc)
            self.e_key_released = False

    def handle_quest_interaction(self, pressed_keys, hit_npc):
        if pressed_keys[K_w] and self.quest == True  :
            for npc in hit_npc:
                if npc.quest is not None :
                    self.show_quest(npc)
        if pressed_keys[K_h]:
            for npc in hit_npc:
                if npc.quest is not None and npc.told_quest == True and npc.quest.status == 'Not started':
                    self.quest_screen(npc)
    def handle_waypoint_interaction(self, pressed_keys, hit_waypoint):
        if pressed_keys[K_e] and hit_waypoint and self.e_key_released and self.go_next: 
            for waypoint in hit_waypoint:
                if waypoint.avaiable:
                    self.e_key_released = False
                    waypoint.actions()


    def handle_inventory(self,pressed_keys):
        if pressed_keys[K_TAB]:
                self.inventory_open = True
                self.atq = self.base_atq + self.inventory.current_weapon.damage if self.inventory.current_weapon is not None else self.base_atq
                self.defense = 0
                #self.defense = self.base_defense + self.inventory.current_armor.armor if self.inventory.current_weapon is not None else self.base_defense
                self.inventory.display()   
        else :
            self.inventory_open = False 
    def move(self):
        hit_npc = pygame.sprite.spritecollide(self,self.game.npcs,False)
        hit_waypoint = pygame.sprite.spritecollide(self, self.game.waypoints,False)

        pressed_keys = pygame.key.get_pressed()
        if hit_npc:
            for npc in hit_npc:
                self.show_interaction(npc)
        if pressed_keys[K_p]:
            self.update()
        if hit_waypoint:
            for waypoint in hit_waypoint:
                if waypoint.avaiable:
                    self.show_interaction(waypoint)

        self.handle_movement(pressed_keys)
        self.handle_npc_interaction(pressed_keys, hit_npc)
        self.handle_quest_interaction(pressed_keys, hit_npc)
        self.handle_waypoint_interaction(pressed_keys, hit_waypoint)
        self.handle_inventory(pressed_keys)

        if not hit_npc and not self.e_key_released:
            self.reset_text()
            self.e_key_released = True

        if not any(pressed_keys):
            self.current_direction = 'standing'
        

    def check_collision(self, direction, sprite_group):
        hits = pygame.sprite.spritecollide(self, sprite_group, False)
        for hit in hits:
            if direction == 'x':
                if self.rect.right > hit.rect.left and self.rect.left < hit.rect.left:
                    self.rect.right = hit.rect.left
                if self.rect.left < hit.rect.right and self.rect.right > hit.rect.right:
                    self.rect.left = hit.rect.right
            else:
                if self.rect.bottom > hit.rect.top and self.rect.top < hit.rect.top:
                    self.rect.bottom = hit.rect.top
                if self.rect.top < hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                    self.rect.top = hit.rect.bottom

    def show_interaction(self,npc):
        npc.show_interaction()
        self.show_npc_text(npc)

    def show_npc_text(self,npc):
        font = pygame.font.Font(None, 20)
        
        x = npc.rect.x -10
        lines = f'{npc.possible_interaction}'.split('\n')
        y= npc.rect.y -(20*len(lines))
        text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
        for text_surface in text_surfaces:
            self.game.screen.blit(text_surface, (x, y))
            y += text_surface.get_height() 


    def next_step(self,npc):
        npc.next_step()

    def reset_text(self):
        self.text = ''

    def is_herobrine(self):
        if self.gun == True:
            self.temp_x = self.rect.x
            self.temp_y = self.rect.y
            self.image = pygame.image.load('images/herobrine.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.x = self.temp_x
            self.rect.y = self.temp_y

    def start_quest(self):
        self.quest = True
        for npc in self.game.npcs:
            if npc.killable:
                self.next_step(npc)

    def interaction(self, npc):
        npc.actions()
        npc.talk_sound.play()
        npc.dialogue_next()

    def end_of_quest(self,quest):
        for i in range (quest.holder.max_dialogue):
            quest.holder.dialogue[i] = quest.post_text
        quest.holder.quest = None
        if quest.game_changer:
            for waypoint in self.game.waypoints:
                waypoint.avaiable = True
                self.gold += self.on_going_quest[quest.id].reward[0]
                self.inventory.add_weapon(self.on_going_quest[quest.id].reward[1])
                self.inventory.add_item(self.on_going_quest[quest.id].reward[2])
        self.on_going_quest.remove(quest)

    def is_end_end(self):
        for quest in self.on_going_quest:
            if quest is not None and quest.condition():
                self.end_of_quest(quest)

    def show_quest(self,npc):
        self.text = self.voisin 
        self.text += "\nQuête : " + npc.quest.name
        self.text += "\n" + npc.quest.description
        self.text += "\n-Press space to exit"
        if npc.quest.status == 'Not started':
            self.text += "\n-Press y to accept"
        lines = f'{self.voisin} {self.text}'.split('\n')
        background_image = pygame.image.load(self.game.backgrounds[self.game.current_map])
        background_image = pygame.transform.scale(background_image,(1000,800))
        self.game.screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 36)
        npc.told_quest = True
        text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]

        for i, text_surface in enumerate(text_surfaces):
            self.game.screen.blit(text_surface, (100, 200 + i*40)) 
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE:
                        running = False
                    elif event.key == pygame.K_y and npc.quest.status == 'Not started':
                        npc.quest.start()  
                        self.on_going_quest[npc.quest.id] = npc.quest
                            
                        for each_npc in self.game.npcs:
                            if each_npc.quest == None:
                                self.next_step(each_npc)
                        running = False
        self.text = ''


    def show_text(self):
            font = pygame.font.Font(None, 24)
            y= 700
            lines = f'{self.voisin} {self.text}'.split('\n')
            text_surfaces = [font.render(line, True, (240, 240, 240)) for line in lines]
            for text_surface in text_surfaces:
                self.game.screen.blit(text_surface, (200, y))
                y += text_surface.get_height() 

    def attack_monster(self, monster):
        monster.health -= self.attack_power
        if monster.health <= 0:
            print("You have defeated the monster!")
        else:
            print("You have attacked the monster! Its health is now {}".format(monster.health))
    def update(self):
        self.game.clear_npc()
        self.game.clear_house()
        self.game.current_map+=1
        self.game.init_background()
        self.game.init_walls()
        self.game.init_house()
        self.game.init_npc()
        self.default()
    
    def update_before(self):
        self.game.clear_npc()
        self.game.clear_house()
        self.game.current_map-=1
        self.game.init_background()
        self.game.init_walls()
        self.game.init_house()
        self.game.init_npc()
        self.default()

    def default(self):
        self.go_next = False
        self.text=''
        self.voisin=''
        self.alex = False
        self.gun = False
        self.nb_voisin = 5
        self.key = False
        self.quest = False