import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup


pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT = 1000, 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

all_sprites = pygame.sprite.Group()


npcs = pygame.sprite.Group()


houses = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('background_npc_town.png')

pygame.display.set_caption("Adventure Game")

font = pygame.font.Font(None, 30)


class game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tab_npc1= [(280,150,'Alexandre :','Je suis raciste', 'npc.png'),
                (280, 341,'Coco :', 'Je suis pas raciste', 'npc.png'),
                (740,150, 'Olivier :', 'Je suis trop fort en info', 'npc_reverse.png'),
                (740,320, 'Martin :', 'Ptn mais qui est olivier','npc_reverse.png'),
                (280,553,'Madao :', 'Ils veulent pas la fermer?'+"\n"+'Tu veux pas les tuer pour moi?\n(press r to accept)','madao.png')]
        
        self.tab_house = [(140,87,'house2.png'),
                 (140, 281,'house3.png'),
                 (140, 490, 'house1.png')]
        
        self.tab_npc_map1 = []
        self.tab_house_map1= []
        self.init_npc()
        self.init_house()
    
    def init_npc(self):
        for i in range(5):
            self.tab_npc_map1.append(NPC(self.tab_npc1[i][0],self.tab_npc1[i][1],self.tab_npc1[i][2],self.tab_npc1[i][3],self.tab_npc1[i][4]))
            npcs.add(self.tab_npc_map1[i])
            all_sprites.add(self.tab_npc_map1[i])
    def init_house(self):
        for i in range(3):
            self.tab_house_map1.append(house(self.tab_house[i][0],self.tab_house[i][1],self.tab_house[i][2]))
            houses.add(self.tab_house_map1[i])
            all_sprites.add(self.tab_house_map1[i])
            print(self.tab_house_map1[i].rect.x,self.tab_house_map1[i].rect.y)
            print(self.tab_house[i][0],self.tab_house[i][1])



class mySprite(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect.x = x
        self.rect.y = y


class Player(mySprite):
    def __init__(self,speed=2):
        super().__init__(483,600,'steve.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.speed = speed
        self.basespeed = speed
        self.e_key_released = True
        self.text=''
        self.voisin=''
        self.alex = False
        self.gun = False
        self.nb_voisin = 5
        self.key = False


    def move(self):
        hit_npc = pygame.sprite.spritecollide(self,npcs,False)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            if self.speed<=self.basespeed:
                self.speed*=4
            else:
                self.speed/=4
        if pressed_keys[K_LEFT] and self.rect.x - self.speed > 0 :
            self.rect.x -= self.speed
            self.check_collision('x')
        if pressed_keys[K_RIGHT] and self.rect.x + self.speed < WIDTH-50 :
            self.rect.x += self.speed
            self.check_collision('x')
        if pressed_keys[K_UP]  and self.rect.y - self.speed > 0:  
            self.rect.y -= self.speed
            self.check_collision('y')
        if pressed_keys[K_DOWN] :
            self.rect.y += self.speed
            self.check_collision('y')
            print(self.rect.x,self.rect.y)
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
                    self.text = 'Bv mon gars mais la suite existe pas'  
                    self.key = True
            self.e_key_released = False
        if pressed_keys[K_r] and hit_npc and self.alex== True:
            for npc in hit_npc:
                if npc.name == 'Madao :':
                    self.text = 'Merci! Prends ce gun'
                    npc.dialogue = 'Vasyyyy'   
                    self.alex = False     
                    self.gun = True   
        if pressed_keys[K_r] and hit_npc and self.gun== True:
            for npc in hit_npc:
                if npc.name != 'Madao :':
                    self.text = 'BANG!'
                    all_sprites.remove(npc)
                    npcs.remove(npc)
                    self.nb_voisin -=1
                    print("test3")
        if not pressed_keys[K_e] and not hit_npc and not self.e_key_released:
            self.e_key_released = True
            self.text = '' 
            self.voisin = ''
            print("test4")

    def check_collision(self, direction):

        hits = pygame.sprite.spritecollide(self, houses, False)
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
        

player = Player()   
all_sprites.add(player)

class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path) :
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.name = name
        self.dialogue = dialogue

class house(mySprite):
    def __init__(self,x,y,path):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (160, 160))



game = game()



text = player.text

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.blit(background, (0,0))

    lines = f'{player.voisin} {player.text}'.split('\n')
    text_surfaces = [font.render(line, True, (155, 0, 0)) for line in lines]

    y = 700  
    for text_surface in text_surfaces:
        screen.blit(text_surface, (200, y))
        y += text_surface.get_height() 

    player.move()
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    pygame.display.flip()