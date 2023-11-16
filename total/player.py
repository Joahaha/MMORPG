import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite

class Player(mySprite):
    def __init__(self,game,speed=10):
        super().__init__(483,600,'images/steve.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 483
        self.rect.y = 600
        self.speed = speed
        self.game = game
        self.basespeed = speed
        self.e_key_released = True
        self.text=''
        self.voisin=''
        self.alex = False
        self.gun = False
        self.nb_voisin = self.game.nb_voisins[self.game.current_map]
        self.key = False
        self.temp_x = 0
        self.temp_y = 0


    def move(self):
        hit_npc = pygame.sprite.spritecollide(self,self.game.npcs,False)
        hit_waypoint = pygame.sprite.spritecollide(self.self.game.waypoints,False)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_p]:
            self.update()
        if pressed_keys[K_LEFT] and self.rect.x - self.speed > 0 :
            self.rect.x -= self.speed
            self.check_collision('x')
            self.check_collision2('x')
        if pressed_keys[K_RIGHT] and self.rect.x + self.speed < self.game.width-50 :
            self.rect.x += self.speed
            self.check_collision('x')
            self.check_collision2('x')
        if pressed_keys[K_UP]  and self.rect.y - self.speed > 0:  
            self.rect.y -= self.speed
            self.check_collision('y')
            self.check_collision2('y')
        if pressed_keys[K_DOWN] and self.rect.y +self.speed < self.game.height-50 :
            self.rect.y += self.speed
            self.check_collision('y')
            self.check_collision2('y')
        if pressed_keys[K_e] and hit_npc and self.e_key_released:
            for npc in hit_npc:
                self.interaction(npc)
            self.e_key_released = False
        if pressed_keys[K_e] and hit_waypoint: 
            self.update()
        

        if not hit_npc and not self.e_key_released:
            self.e_key_released = True


    def check_collision(self, direction):

        hits = pygame.sprite.spritecollide(self, self.game.houses, False)
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

    def check_collision2(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.all_walls, False)
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

    def interaction(self,npc):
        npc.actions()
        npc.dialogue_next()
        
    def next_step(self,npc):
        npc.next_step()

    def is_herobrine(self):
        if self.gun == True:
            self.temp_x = self.rect.x
            self.temp_y = self.rect.y
            self.image = pygame.image.load('images/herobrine.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.x = self.temp_x
            self.rect.y = self.temp_y
            
    def update(self):
        self.game.clear_npc()
        self.game.clear_house()
        self.game.current_map+=1
        self.game.init_background()
        self.game.init_walls()
        self.game.init_house()
        self.game.init_npc()
        self.default()
    
    def default(self):
        self.e_key_released = True
        self.text=''
        self.voisin=''
        self.alex = False
        self.gun = False
        self.nb_voisin = 5
        self.key = False
