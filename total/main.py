import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup


pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT = 1000, 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('background_npc_town.png')

pygame.display.set_caption("Adventure Game")

font = pygame.font.Font(None, 30)

class Player(pygame.sprite.Sprite):
    def __init__(self, x=483, y=0, speed=2):
        super().__init__()
        self.image = pygame.image.load('steve.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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
        if pressed_keys[K_RIGHT] and self.rect.x + self.speed < WIDTH - self.rect.width:
            self.rect.x += self.speed
        if pressed_keys[K_UP] :
            if self.rect.y -self.speed <0 and self.key and self.rect.x>400 and self.rect.x<550 :
                self.rect.y += self.speed
            if self.rect.y - self.speed > 0:
                self.rect.y -= self.speed
        if pressed_keys[K_DOWN] and self.rect.y + self.speed < HEIGHT - self.rect.height:
            self.rect.y += self.speed
        hits = pygame.sprite.spritecollide(self, houses, False)
        for hit in hits:
            if self.rect.colliderect(hit.rect):
                if self.rect.right > hit.rect.left and self.rect.left < hit.rect.left:
                    self.rect.right = hit.rect.left
                if self.rect.left < hit.rect.right and self.rect.right > hit.rect.right:
                    self.rect.left = hit.rect.right
                if self.rect.bottom > hit.rect.top and self.rect.top < hit.rect.top:
                    self.rect.bottom = hit.rect.top
                if self.rect.top < hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                    self.rect.top = hit.rect.bottom
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

    

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y,name,dialogue,pathes) :
        super().__init__()
        self.image = pygame.image.load(pathes).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.dialogue = dialogue
class NPC_reverse(pygame.sprite.Sprite):
    def __init__(self, x, y,name,dialogue) :
        super().__init__()
        self.image = pygame.image.load('npc_reverse.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.dialogue = dialogue

class house(pygame.sprite.Sprite):
    def __init__(self,x,y,pathes):
        super().__init__()
        self.image = pygame.image.load(pathes).convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



player = Player()
npc1 = NPC(280,150,'Alexandre :','Je suis raciste', 'npc.png')
npc2 = NPC(280, 341,'Coco :', 'Je suis pas raciste', 'npc.png')
npc3 = NPC_reverse(740,150, 'Olivier :', 'Je suis trop fort en info')
npc4 = NPC_reverse(740,320, 'Martin :', 'Ptn mais qui est olivier')
npc5 = NPC(280,553,'Madao :', 'Ils veulent pas la fermer?'+"\n"+'Tu veux pas les tuer pour moi?\n(press r to accept)','madao.png')
house1 = house(140,87,'house2.png')
house2 = house(140, 281,'house3.png')
house3 = house(140, 490, 'house1.png')


all_sprites = pygame.sprite.Group()
all_sprites.add(house1)
all_sprites.add(house2)
all_sprites.add(house3)
all_sprites.add(player)
all_sprites.add(npc1)
all_sprites.add(npc2)
all_sprites.add(npc3)
all_sprites.add(npc4)
all_sprites.add(npc5)

npcs = pygame.sprite.Group()
npcs.add(npc1)
npcs.add(npc2)
npcs.add(npc3)
npcs.add(npc4)
npcs.add(npc5)

houses = pygame.sprite.Group()
houses.add(house1)
houses.add(house2)
houses.add(house3)

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