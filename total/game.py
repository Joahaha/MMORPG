import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite
from player import Player
from npc import NPC
from house import house
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

                ((290,60,'Bob :','Je suis gentil', 'images/npc_bad_1.png'),
                (280, 341,'Bobo :', 'Je suis pas gentil', 'images/npc_bad_2.png'),
                (660,60, 'Baba :', 'Je suis trop fort en sport', 'images/npc_bad_3.png'),
                (740,320, 'Fdp :', 'Ptn mais qui est bob','images/npc_bad_4.png'),
                (280,553,'dark_madao :', 'Ils veulent pas la fermer?'+"\n"+'Tu veux pas les manger pour moi?\n(press r to accept)','images/npc_madao_1.png'))]
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
        self.backgrounds = ['images/background_npc_town.png','images/quatre_chemin.png','images/carte_riviere.png','images/house_inside.png']
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
        self.background = pygame.transform.scale(self.background, (self.width, self.height))


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