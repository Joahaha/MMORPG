import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup

pygame.init()

pygame.display.set_caption("Joah adventure")

font = pygame.font.Font(None, 30)


class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tab_npc= [((280,150,'Alexandre :','Je suis raciste', 'images/npc.png'),
                (280, 341,'Coco :', 'Je suis pas raciste', 'images/npc.png'),
                (740,150, 'Olivier :', 'Je suis trop fort en info', 'images/npc_reverse.png'),
                (740,320, 'Martin :', 'Ptn mais qui est olivier','images/npc_reverse.png'),
                (280,553,'Madao :', 'Ils veulent pas la fermer?'+"\n"+'Tu veux pas les tuer pour moi?\n(press r to accept)','images/madao.png')),
                ((290,60,'Bob :','Je suis gentil', 'images/npc.png'),
                (280, 341,'Bobo :', 'Je suis pas gentil', 'images/npc.png'),
                (660,60, 'Baba :', 'Je suis trop fort en sport', 'images/npc_reverse.png'),
                (740,320, 'Fdp :', 'Ptn mais qui est bob','images/npc_reverse.png'),
                (280,553,'dark_madao :', 'Ils veulent pas la fermer?'+"\n"+'Tu veux pas les manger pour moi?\n(press r to accept)','images/madao.png'))]
        self.tab_house = [((140,87,'images/house2.png'),
                 (140, 281,'images/house3.png'),
                 (140, 490, 'images/house1.png')),
                 (())]
        self.current_map = 0
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.tab_npc_map1 = []
        self.tab_house_map1= []
        self.backgrounds = ['images/background_npc_town.png','images/quatre_chemin.png','images/winter.png']
        self.background = ''
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.nb_voisins = [5,5]
        self.nb_maisons = [3,0]
        self.init_player()
        self.init_house()
        self.init_npc()
        self.init_background()
        self.init_game()


    def init_npc(self):
        for i in range(self.nb_voisins[self.current_map]):
            self.tab_npc_map1.append(NPC(self.tab_npc[self.current_map][i][0],self.tab_npc[self.current_map][i][1],self.tab_npc[self.current_map][i][2],self.tab_npc[self.current_map][i][3],self.tab_npc[self.current_map][i][4]))
            self.npcs.add(self.tab_npc_map1[i])
            self.all_sprites.add(self.tab_npc_map1[i])

    def clear_npc(self):
        for i in range(self.nb_voisins[self.current_map]):
            self.tab_npc_map1[i].kill() 
        self.tab_npc_map1 = [] 

    def clear_house(self):
        for i in range(self.nb_maisons[self.current_map]):
            self.tab_house_map1[i].kill() 
        self.tab_house_map1 = []

    def init_house(self):
        for i in range(self.nb_maisons[self.current_map]):
            self.tab_house_map1.append(house(self.tab_house[self.current_map][i][0],self.tab_house[self.current_map][i][1],self.tab_house[self.current_map][i][2]))
            self.houses.add(self.tab_house_map1[i])
            self.all_sprites.add(self.tab_house_map1[i])

        

    def init_background(self) :
        self.background= pygame.image.load(self.backgrounds[self.current_map])


    def init_player(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)

    def init_game(self):
        running = True

        while running:
            dt = self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.screen.blit(self.background, (0,0))
            lines = f'{self.player.voisin} {self.player.text}'.split('\n')
            text_surfaces = [font.render(line, True, (155, 0, 0)) for line in lines]

            y = 700  
            for text_surface in text_surfaces:
                self.screen.blit(text_surface, (200, y))
                y += text_surface.get_height() 

            self.player.move()
            for houses_nb in self.houses:
                self.screen.blit(houses_nb.image, houses_nb.rect)
            for npc_nb in self.npcs:
                self.screen.blit(npc_nb.image, npc_nb.rect)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()

class mySprite(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Player(mySprite):
    def __init__(self,game,speed=10):
        super().__init__(483,600,'images/steve.png')
        self.rect = self.image.get_rect()
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

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.x - self.speed > 0 :
            self.rect.x -= self.speed
            self.check_collision('x')
        if pressed_keys[K_RIGHT] and self.rect.x + self.speed < self.game.width-50 :
            self.rect.x += self.speed
            self.check_collision('x')
        if pressed_keys[K_UP]  and self.rect.y - self.speed > 0:  
            self.rect.y -= self.speed
            self.check_collision('y')
        if pressed_keys[K_DOWN] and self.rect.y +self.speed < self.game.height-50 :
            self.rect.y += self.speed
            self.check_collision('y')
        if pressed_keys[K_e] and hit_npc and self.e_key_released:
            for npc in hit_npc:
                self.voisin = npc.name
                self.text = npc.dialogue
                if self.text !='Vasyyyy' and self.voisin == 'Madao :':
                    self.alex = True
                if self.voisin != 'Madao :' and self.gun == True:
                    self.text += '\n(appuie sur r pour tirer)'
                    npc.dialogue = 'Ouille' 
                if self.voisin == 'Madao :' and self.nb_voisin ==1:
                    if self.key == False:
                        self.text = 'Bv mgl reviens me parler si tu veux changer de map'  
                        self.key = True
                    else:
                           
                        self.update()
            self.e_key_released = False
        if pressed_keys[K_r] and hit_npc and self.alex== True:
            for npc in hit_npc:
                if npc.name == 'Madao :':
                    self.text = 'Merci! Prends ce gun'
                    npc.dialogue = 'Vasyyyy'   
                    self.alex = False     
                    self.gun = True   
                    self.is_herobrine()
        if pressed_keys[K_r] and hit_npc and self.gun== True:
            for npc in hit_npc:
                if npc.name != 'Madao :':
                    self.text = 'BANG!'
                    self.game.all_sprites.remove(npc)
                    self.game.npcs.remove(npc)
                    self.nb_voisin -=1

        if not pressed_keys[K_e] and not hit_npc:
            self.e_key_released = True
            self.text = '' 
            self.voisin = ''

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


class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path) :
        super().__init__(x,y,path)
        self.name = name
        self.dialogue = dialogue

class house(mySprite):
    def __init__(self,x,y,path):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



game = Game()

