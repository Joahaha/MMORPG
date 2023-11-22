import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from player import Player
from npc import NPC
from house import House
from wall_verti import Wall_verti
from wall_hori import Wall_hori
from waypoint import Waypoint
from quest import Quest
from weapon import Weapon
from usable_item import Usable_Item
from fake_house import Fake_house
from monster import Monster

pygame.init()
pygame.display.set_caption("Joah adventure")
font = pygame.font.Font(None, 30)

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_music = ['sounds/pokemon_ost_1.mp3','sounds/pokemon_ost_1.mp3','sounds/pokemon_ost_1.mp3']
        self.npc_sounds = ['sounds/npc_talk_1.mp3','sounds/npc_talk_2.mp3','sounds/npc_talk_3.mp3']
        self.weapons = [
            Weapon("Sword", "Elle coupe bien", 100, 1,'images/weapons/sword.png', self,10),
            Weapon("Axe", "Et pas le deo", 150, 2,'images/weapons/axe.png', self,15),
            Weapon("Spear", "il joue pantheon xd", 200, 3,'images/weapons/spear.png', self,20),
            Weapon("Bow", "Nv jungler de la kc?", 250, 2,'images/weapons/bow.png', self,25),
        ]
        self.usable_items = [
        Usable_Item("Potion de gold", "Elle give 10 gold", 50, 1, 'images/usable_item/potion_gold.png', self, lambda : setattr(self.player, 'gold', self.player.gold + 10)),
        Usable_Item("Potion de gold", "Elle give 20 gold", 50, 1, 'images/usable_item/potion_gold.png', self, lambda : setattr(self.player, 'gold', self.player.gold + 20)),
        Usable_Item("Potion de HP", "Elle soigne 10 HP", 50, 1, 'images/usable_item/potion_hp.png', self, lambda : setattr(self.player, 'health', self.player.health + 10)),
        Usable_Item("Potion de HP", "Elle soigne 50 HP", 50, 1, 'images/usable_item/potion_hp.png', self, lambda : setattr(self.player, 'health', self.player.health + 50)),
        Usable_Item("Potion de mana", "Elle soigne mana", 50, 1, 'images/usable_item/potion_mana.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
        Usable_Item("Potion de mana", "Elle soigne mana", 50, 1, 'images/usable_item/potion_mana.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
        Usable_Item("Potion d'arme aléatoire", "Elle soigne mana", 50, 1, 'images/usable_item/potion_weapon.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
        Usable_Item("Potion d'arme aléatoire", "Elle soigne mana", 50, 1, 'images/usable_item/potion_weapon.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
                ]
        self.quest= Quest(  
                            name ='Kill everybody',
                            description='Madao en a marre. Il veut que tu tues tout le monde',
                            objectives=['Tuer tout le monde', 'Reparler à Madao après'],
                            reward= [50,self.weapons[1],self.usable_items[1]],
                            condition = False,
                            post_text = '\nMerci tu peux prendre le téléporteur pour changer de map',
                            holder = NPC,
                            game_changer = True,
                            id = 0)
        
        self.tab_npc= [((300,240,'Alexandre',['\nJe suis raciste','\nJe suis vraiment raciste','\nJe suis le plus raciste'], 'images/npc_good_2.png',3,self,True,None,self.npc_sounds[1]),
                (300, 370,'Coco', ['\nJe suis pas raciste'], 'images/npc_good_1.png',1,self,True,None,self.npc_sounds[1]),
                (740,150, 'Olivier', ['\nJe suis trop fort en info'], 'images/npc_good_3.png',1,self,True,None,self.npc_sounds[1]),
                (740,450, 'Martin', ['\nPtn mais qui est olivier'],'images/npc_good_4.png',1,self,True,None,self.npc_sounds[1]),
                (400,600,'Madao', ['\nIls veulent pas la fermer?'+"\n"],'images/npc_madao_2.png',1,self,False,self.quest,self.npc_sounds[2])),

                ((290,60,'Bob',['\nJe suis gentil'], 'images/npc_bad_1.png',1,self,True,None,self.npc_sounds[1]),
                (280, 341,'Bobo',[ '\nJe suis pas gentil'], 'images/npc_bad_2.png',1,self,True,None,self.npc_sounds[1]),
                (660,60, 'Baba :', ['\nJe suis trop fort en sport'], 'images/npc_bad_3.png',1,self,True,None,self.npc_sounds[1]),
                (740,320, 'Fdp :', ['\nPtn mais qui est bob'],'images/npc_bad_4.png',1,self,True,None,self.npc_sounds[1]),
                (280,553,'dark_madao :', ['\nYo la team tu veux quoi frr'],'images/npc_madao_1.png',1,self,True,None,self.npc_sounds[1])),
                (())
                ]
        self.tab_house = [((140,87,'images/house1.png'),
                 (700, 281,'images/house1.png'),
                 (140, 490, 'images/house1.png')),
                 (()),(())]
        self.tab_monster = [((400,400,'images/monster/monster_test.png',10,10,100,1,self,2),)]
        self.current_map = 0
        
        self.tab_npc_map = [[] for _ in range(len(self.tab_npc))]
        self.tab_house_map = [[] for _ in range(len(self.tab_house))]
        self.tab_fake_house_map =[[] for _ in range(len(self.tab_house))] 
        self.tab_monster_map = [[] for _ in range(len(self.tab_monster))]
        self.backgrounds = ['images/background_npc_town.png','images/house_inside.png','images/carte_riviere.png','images/quatre_chemin.png']
        self.background = ''
        self.walls_verti = [(()),
                            ((320, 30,'images/wall.png',10,220),(320, 30,'images/wall.png',10,220)),
                            (0,0,'images/border.png')]
        self.walls_hori = [(()),
                           ((215,255,'images/wall.png',650,10),(215,255,'images/wall.png',650,10)),
                           (0,0,'images/border.png')]
        self.wall_per_map_hori = []
        self.wall_per_map_verti = []


        self.fps = 60
        self.clock = pygame.time.Clock()
        self.current_frame = 0
        self.frame_counter = 0
        self.muted = False
        self.all_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.fake_houses = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()
        self.waypoints =pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
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
        self.init_monster()
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
                                         self.tab_npc[self.current_map][i][8],
                                         pygame.mixer.Sound(self.tab_npc[self.current_map][i][9])
                                         ))
            self.npcs.add(self.tab_npc_map[self.current_map][i])
            self.all_sprites.add(self.tab_npc_map[self.current_map][i])
    def init_npc_per_map(self):
        for npc_nb in self.npcs:
                self.screen.blit(npc_nb.image, npc_nb.rect)
                npc_nb.bouger()

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
            self.tab_fake_house_map[self.current_map].append((Fake_house(self.tab_house[self.current_map][i][0]+10,
                                                               self.tab_house[self.current_map][i][1],
                                                               self.tab_house[self.current_map][i][2])))        
            
            self.houses.add(self.tab_house_map[self.current_map][i])
            self.fake_houses.add(self.tab_fake_house_map[self.current_map][i])
            self.all_sprites.add(self.tab_house_map[self.current_map][i])
    def init_house_per_map(self):
        for houses_nb in self.houses:
                self.screen.blit(houses_nb.image, houses_nb.rect)
    def init_fake_house_per_map(self):
        for houses_nb in self.fake_houses:
                self.screen.blit(houses_nb.image, houses_nb.rect)
    def init_walls(self):
        for i in range(self.nb_walls[self.current_map]):
            self.wall_per_map_verti.append(Wall_verti(self.walls_verti[self.current_map][i][0],
                                                      self.walls_verti[self.current_map][i][1],
                                                      self.walls_verti[self.current_map][i][2],
                                                      self.walls_verti[self.current_map][i][3],
                                                      self.walls_verti[self.current_map][i][4]))
            
            self.wall_per_map_hori.append (Wall_hori(self.walls_hori[self.current_map][i][0],
                                                     self.walls_hori[self.current_map][i][1],
                                                     self.walls_hori[self.current_map][i][2],
                                                     self.walls_hori[self.current_map][i][3],
                                                     self.walls_hori[self.current_map][i][4]))
            
            self.all_walls.add(self.wall_per_map_verti[i])
            self.all_walls.add(self.wall_per_map_hori[i])
            self.all_sprites.add(self.wall_per_map_hori[i])
            self.all_sprites.add(self.wall_per_map_verti[i])

    def init_walls_per_map(self):
        for walls in self.all_walls:
            self.screen.blit(walls.image, walls.rect)

    def init_background(self) :
        self.background= pygame.image.load(self.backgrounds[self.current_map])
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def init_waypoint(self):
        self.waypoints.add(Waypoint(400,700,'images/waypoint.png',self))

    def init_waypoint_per_map(self):
        for waypoints in self.waypoints:
            self.screen.blit(waypoints.image, waypoints.rect)

    def init_player(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)



    def show_player(self):
            if not self.player.inventory_open:
                self.frame_counter = (self.frame_counter + 1) % (self.fps//8)
                self.screen.blit(self.player.frames[self.player.current_direction][self.current_frame], (self.player.rect.x, self.player.rect.y))

                if self.frame_counter == 0:
                    self.current_frame = (self.current_frame + 1) % 9
    def init_monster(self):
        for i in range(len(self.tab_monster[self.current_map])):
            self.tab_monster_map[self.current_map].append(Monster(self.tab_monster[self.current_map][i][0],
                                                                  self.tab_monster[self.current_map][i][1],
                                                                  self.tab_monster[self.current_map][i][2],
                                                                  self.tab_monster[self.current_map][i][3],
                                                                  self.tab_monster[self.current_map][i][4],
                                                                  self.tab_monster[self.current_map][i][5],
                                                                  self.tab_monster[self.current_map][i][6],
                                                                  self.tab_monster[self.current_map][i][7],
                                                                  self.tab_monster[self.current_map][i][8]))
            self.all_sprites.add(self.tab_monster_map[self.current_map][i])
            self.monsters.add(self.tab_monster_map[self.current_map][i])

    def init_monster_per_map(self):
        for monster in self.monsters:
            self.screen.blit(monster.image, monster.rect)
    def init_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music[self.current_map])
        pygame.mixer.music.play(-1) 

    def mute_sound(self):
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else 1)
    
    def check_mute(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mute_sound()
    def show_weapon(self):
        if self.player.inventory.current_weapon is not None:
            self.screen.blit(pygame.transform.scale(self.player.inventory.current_weapon.image,(50,50)),(900,700))
    
    def show_hp(self):
        hp = font.render(str(self.player.health), True, (255, 0, 0))
        self.screen.blit(hp, (800, 700))

    def show_mana(self):
        mana = font.render(str(self.player.mana), True, (0, 0, 255))
        self.screen.blit(mana, (800, 750))
    def game_over(self):
        self.screen.fill((0,0,0))
        game_over = font.render("Game over", True, (255, 0, 0))
        self.screen.blit(game_over, (400, 400))
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()
        quit()
    

    def init_game(self):
        running = True
        self.init_music()
        self.init_monster_per_map() 

        while running:
            dt = self.clock.tick(self.fps)
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    running = False

            self.check_mute(events)
            self.init_fake_house_per_map()
            self.init_walls_per_map()
            self.screen.blit(self.background, (0,0))

            self.init_house_per_map()
            self.init_npc_per_map()
            self.init_waypoint_per_map()

            self.player.show_text()
            self.player.move()
            self.show_player()
            self.player.is_end_end()
            self.show_weapon()
            self.show_hp()
            self.show_mana()
            

            for monster in self.monsters:
                monster.update()

            pygame.display.flip()