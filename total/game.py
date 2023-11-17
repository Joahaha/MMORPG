import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from mysprite import mySprite
from player import Player
from npc import NPC
from house import House
from wall_verti import Wall_verti
from wall_hori import Wall_hori
from waypoint import Waypoint
from quest import Quest

pygame.init()
pygame.display.set_caption("Joah adventure")
font = pygame.font.Font(None, 30)

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.quest= Quest(
                            name ='Kill everybody',
                            description='Madao en a marre. Il veut que tu tues tout le monde',
                            objectives=['Tuer tout le monde', 'Reparler à Madao après'],
                            reward='50 gold coins',
                            condition = True,
                            post_text = '\nMerci tu peux prendre le téléporteur pour changer de map',
                            holder = NPC,
                            game_changer = True)
        
        self.tab_npc= [((300,200,'Alexandre',['\nJe suis raciste','\nJe suis vraiment raciste'], 'images/npc_good_2.png',2,self,True,None),
                (300, 341,'Coco', ['\nJe suis pas raciste'], 'images/npc_good_1.png',1,self,True,None),
                (740,150, 'Olivier', ['\nJe suis trop fort en info'], 'images/npc_good_3.png',1,self,True,None),
                (740,420, 'Martin', ['\nPtn mais qui est olivier'],'images/npc_good_4.png',1,self,True,None),
                (300,553,'Madao', ['\nIls veulent pas la fermer?'+"\n"+'Tu veux pas les tuer pour moi?\n'],'images/npc_madao_2.png',1,self,False,self.quest)),

                ((290,60,'Bob',['Je suis gentil'], 'images/npc_bad_1.png',1,self,True,None),
                (280, 341,'Bobo',[ 'Je suis pas gentil'], 'images/npc_bad_2.png',1,self,True,None),
                (660,60, 'Baba :', ['Je suis trop fort en sport'], 'images/npc_bad_3.png',1,self,True,None),
                (740,320, 'Fdp :', ['Ptn mais qui est bob'],'images/npc_bad_4.png',1,self,True,None),
                (280,553,'dark_madao :', ['Yo la team tu veux quoi frr'],'images/npc_madao_1.png',1,self,True,None)),
                (())
                ]
        self.tab_house = [((140,87,'images/house1.png'),
                 (700, 281,'images/house1.png'),
                 (140, 490, 'images/house1.png')),
                 (()),(())]
       
        self.current_map = 0
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.tab_npc_map = [[] for _ in range(len(self.tab_npc))]
        self.tab_house_map = [[] for _ in range(len(self.tab_house))]
        self.backgrounds = ['images/background_npc_town.png','images/house_inside.png','images/carte_riviere.png','images/quatre_chemin.png']
        self.background = ''
        self.walls_verti = [(0,0,''),(320, 30,'images/wall.png'),(0,0,'images/border.png')]
        self.walls_hori = [(0,0,''),(215,255,'images/wall.png'),(0,0,'images/border.png')]
        self.wall_per_map_hori = []
        self.wall_per_map_verti = []


        self.fps = 60
        self.clock = pygame.time.Clock()
        self.current_frame = 0
        self.frame_counter = 0

        self.all_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()
        self.waypoints =pygame.sprite.Group()
        self.nb_voisins = [5,5,0]
        self.nb_maisons = [3,0,0]
        self.nb_walls = [0,2,0]
        self.init_player()
        self.quest.condition = lambda: self.player.nb_voisin == 1
        self.init_house()
        self.init_npc()
        self.quest.holder = self.tab_npc_map[0][4] 
        self.init_walls()
        self.init_waypoint()
        self.init_background()
        self.init_game()


    def init_npc(self):
        for i in range(self.nb_voisins[self.current_map]):
            self.tab_npc_map[self.current_map].append(NPC(self.tab_npc[self.current_map][i][0],
                                         self.tab_npc[self.current_map][i][1],
                                         self.tab_npc[self.current_map][i][2],
                                         self.tab_npc[self.current_map][i][3],
                                         self.tab_npc[self.current_map][i][4],
                                         self.tab_npc[self.current_map][i][5],
                                         self.tab_npc[self.current_map][i][6],
                                         self.tab_npc[self.current_map][i][7],
                                         self.tab_npc[self.current_map][i][8]
                                         ))
            self.npcs.add(self.tab_npc_map[self.current_map][i])
            self.all_sprites.add(self.tab_npc_map[self.current_map][i])

    def clear_npc(self):
        for npc in self.tab_npc_map[self.current_map]:
            npc.kill() 
        self.tab_npc_map[self.current_map] = [] 

    def clear_house(self):
        for i in range(self.nb_maisons[self.current_map]):
            self.tab_house_map[self.current_map][i].kill() 
        self.tab_house_map[self.current_map] = []

    def init_house(self):
        for i in range(self.nb_maisons[self.current_map]):
            self.tab_house_map[self.current_map].append((House(self.tab_house[self.current_map][i][0],
                                                               self.tab_house[self.current_map][i][1],
                                                               self.tab_house[self.current_map][i][2])))
            self.houses.add(self.tab_house_map[self.current_map][i])
            self.all_sprites.add(self.tab_house_map[self.current_map][i])

    def init_walls(self):
        for i in range(self.nb_walls[self.current_map]):
            self.wall_per_map_verti.append(Wall_verti(self.walls_verti[self.current_map][0],self.walls_verti[self.current_map][1],self.walls_verti[self.current_map][2]))
            self.wall_per_map_hori.append (Wall_hori(self.walls_hori[self.current_map][0],self.walls_hori[self.current_map][1],self.walls_hori[self.current_map][2]))
            
            self.all_walls.add(self.wall_per_map_verti[i])
            self.all_walls.add(self.wall_per_map_hori[i])
            self.all_sprites.add(self.wall_per_map_hori[i])
            self.all_sprites.add(self.wall_per_map_verti[i])

    def init_background(self) :
        self.background= pygame.image.load(self.backgrounds[self.current_map])
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def init_waypoint(self):
        self.waypoints.add(Waypoint(400,700,'images/waypoint.png'))


    def init_player(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)

    def init_game(self):
        running = True

        while running:
            self.frame_counter = (self.frame_counter + 1) % (self.fps//5)
            
            dt = self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            for walls in self.all_walls:
                self.screen.blit(walls.image, walls.rect)
            self.screen.blit(self.background, (0,0))
            
            lines = f'{self.player.voisin} {self.player.text}'.split('\n')
            text_surfaces = [font.render(line, True, (155, 0, 0)) for line in lines]

            y = 700  
            for houses_nb in self.houses:
                self.screen.blit(houses_nb.image, houses_nb.rect)
            for npc_nb in self.npcs:
                self.screen.blit(npc_nb.image, npc_nb.rect)
            for waypoints in self.waypoints:
                self.screen.blit(waypoints.image, waypoints.rect)
            for text_surface in text_surfaces:
                self.screen.blit(text_surface, (200, y))
                y += text_surface.get_height() 

            self.player.move()
            self.screen.blit(self.player.frames[self.player.current_direction][self.current_frame], (self.player.rect.x, self.player.rect.y))

            if self.frame_counter == 0:
                self.current_frame = (self.current_frame + 1) % 9
            self.player.is_end_end()
            
            pygame.display.flip()