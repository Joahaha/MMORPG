import sys
sys.path.insert(0, '/autofs/unitytravail/travail/jemy/Perso/MMORPG/total/src/decor')
sys.path.insert(0, '/autofs/unitytravail/travail/jemy/Perso/MMORPG/total/src/player')
sys.path.insert(0, '/autofs/unitytravail/travail/jemy/Perso/MMORPG/total/src/npc')
sys.path.insert(0, '/autofs/unitytravail/travail/jemy/Perso/MMORPG/total/src/items')



import pygame
from pygame.locals import *
from pygame.sprite import AbstractGroup
from src.player.player import Player
from npc import NPC
from src.decor.house import House
from wall_verti import Wall_verti
from wall_hori import Wall_hori
from waypoint import Waypoint
from src.player.quest import Quest
from weapon import Weapon
from usable_item import Usable_Item
from src.decor.fake_house import Fake_house
from monster import Monster
import random
from monster_mele import Monster_melee
from unique_item import Unique_Item
from src.decor.chest import Chest
from boss import Boss

pygame.init()
pygame.display.set_caption("Joah adventure")

class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_music = ['sounds/pokemon_ost_1.mp3','sounds/pokemon_ost_1.mp3','sounds/pokemon_ost_1.mp3']
        self.npc_sounds = ['sounds/npc_talk_1.mp3','sounds/npc_talk_2.mp3','sounds/npc_talk_3.mp3']
        self.weapons = [
            Weapon("Sword", "Elle coupe bien", 100, 1,'images/weapons/sword.png', self,20,10),
            Weapon("Axe", "You can couper du bois easier", 150, 2,'images/weapons/axe.png', self,25,5),
            Weapon("Spear", "Elle est belle", 200, 3,'images/weapons/spear.png', self,10,30),
            Weapon("Bow", "Grosse range mais peu de dégats", 250, 2,'images/weapons/bow.png', self,-5,60),
        ]
        self.usable_items = [
        Usable_Item("Potion de gold", "Elle give 10 gold", 50, 1, 'images/usable_item/potion_gold.png', self, lambda : setattr(self.player, 'gold', self.player.gold + 10)),
        Usable_Item("Potion de gold", "Elle give 20 gold", 50, 1, 'images/usable_item/potion_gold.png', self, lambda : setattr(self.player, 'gold', self.player.gold + 20)),
        Usable_Item("Potion de HP", "Elle soigne 10 HP", 50, 1, 'images/usable_item/potion_hp.png', self, lambda : setattr(self.player, 'health', self.player.health + 10)),
        Usable_Item("Potion de HP", "Elle soigne 50 HP", 50, 1, 'images/usable_item/potion_hp.png', self, lambda : setattr(self.player, 'health', self.player.health + 50)),
        Usable_Item("Potion de mana", "Elle soigne mana", 50, 1, 'images/usable_item/potion_mana.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
        Usable_Item("Potion de mana", "Elle soigne mana", 50, 1, 'images/usable_item/potion_mana.png', self, lambda : setattr(self.player, 'gold', self.player.gold - 10)),
        Usable_Item("Potion d'arme aléatoire", "Elle donne une arme aléatoire", 50, 1, 'images/usable_item/potion_weapon.png', self, lambda : self.player.weapon_tab.append(random.choice(self.weapons))),
        Usable_Item("Potion d'arme aléatoire", "Elle donne une arme aléatoire", 50, 1, 'images/usable_item/potion_weapon.png', self, lambda : self.player.weapon_tab.append(random.choice(self.weapons))),
                ]
        self.unique_items = [
            Unique_Item("Golden key", "Elle ouvre le portail", 0, 1, 'images/unique_item/golden_key.png', self),
            Unique_Item("Monster heart", "Coeur d'un monstre qui apparait une fois par millénaire", 0, 1, 'images/unique_item/monster_heart.png', self),
            Unique_Item("Ultimate key", "Permet d'accéder à la fin du jeu", 0, 1, 'images/unique_item/ultimate_key.png', self),
        ]


        self.quest= Quest(  
                            name ='Kill everybody',
                            description='Madao en a marre. Il veut que tu tues tout le monde',
                            objectives = [{
                                'name': 'Defeat all the the enemy',
                                'completed': False,
                                'shown': False,
                                'display_counter': 150,
                            }],
                            reward= [50,self.weapons[1],self.usable_items[1],None],
                            condition = False,
                            post_text = '\nMerci tu peux prendre le téléporteur pour changer de map',
                            holder = NPC,
                            game_changer = True,
                            id = 0,
                            game = self
                            )
        self.quest2= Quest(  
            name ='Retrieve the golden key',
            description='Retrouve la clé dorée pour ouvrir le portail',
            objectives = [
                {
                    'name': 'Find the password',
                    'completed': False,
                    'shown': False,
                    'display_counter': 150,
                },
                {
                    'name': 'Open the chest',
                    'completed': False,
                    'shown': False,
                    'display_counter': 150,
                }
            ],
            reward= [50,None,None,None],
            condition = False,
            post_text = '\nBonne chance avec le boss final',
            holder = NPC,
            game_changer = True,
            id = 1,
            game = self
        )
        self.quest3= Quest(  
                            name ='La quête de la forêt',
                            description='Une armée de monstre est apparu dans la forêt. Va les tuer',
                            objectives = [{
                                'name': 'Kill all the monster',
                                'completed': False,
                                'shown': False,
                                'display_counter': 150,
                            }],
                            reward= [50,None,None,self.unique_items[1]],
                            condition = False,
                            post_text = '\nMerci de m\'avoir débarassé de ces monstres',
                            holder = NPC,
                            game_changer = True,
                            id = 2,
                            game = self
                            )
        self.quest4= Quest(  
                                name ='Fin du jeu',
                                description='Recupère le coeur du monstre et la clé en or pour finir le jeu',
                                objectives = [{
                                    'name': 'Bring the key and the heart',
                                    'completed': False,
                                    'shown': False,
                                    'display_counter': 150,
                                }
                                ,{
                                    'name': 'Beat the boss',
                                    'completed': False,
                                    'shown': False,
                                    'display_counter': 150,
                                }],
                                reward= [50,None,None,self.unique_items[1]],
                                condition = False,
                                post_text = '\nMerci de m\'avoir débarassé de ces monstres',
                                holder = NPC,
                                game_changer = True,
                                id = 3,
                                game = self
                                )
        self.chest_tab = [
            (),
            (), (500, 200,
                'images/backgrounds/chest.png',
                [50, None, None, self.unique_items[0]],
                lambda player: player.password_found if any(quest is not None and quest.id == 1 for quest in player.on_going_quest) else None,
                self
            )
        ]

        self.tab_npc= [((300,240,'Alexandre',['\nJe suis raciste','\nJe suis vraiment raciste','\nJe suis le plus raciste'], 'images/npc/npc_good_2.png',3,self,True,None,self.npc_sounds[1]),
                (300, 370,'Coco', ['\nTu peux appuyer sur tab pour voir ton inventaire'], 'images/npc/npc_good_1.png',1,self,True,None,self.npc_sounds[1]),
                (740,150, 'Olivier', ['\nJe suis trop fort en info'], 'images/npc/npc_good_3.png',1,self,True,None,self.npc_sounds[1]),
                (740,450, 'Martin', ['\nPtn mais qui est olivier'],'images/npc/npc_good_4.png',1,self,True,None,self.npc_sounds[1]),
                (400,600,'Madao', ['\nIls veulent pas la fermer?'+"\n"],'images/npc/npc_madao_2.png',1,self,False,self.quest,self.npc_sounds[2])),

                ((50,300,'Bob',['\nPrends ce portail pour aller vers la maison hantée'], 'images/npc/npc_bad_1.png',1,self,True,self.quest2,self.npc_sounds[1]),
                (410, 70,'Bobo',[ '\nIl te faut les deux clés pour prendre ce portail'], 'images/npc/npc_bad_2.png',1,self,True,self.quest4,self.npc_sounds[1]),
                (860,300,'dark_madao :', ['\nPortail en direction de la forêt du monstre'],'images/npc/npc_good_1.png',1,self,True,self.quest3,self.npc_sounds[1])),

                ((290,60,'Bob',['\nJe me retiens de tuer tout le monde ici'], 'images/npc/npc_bad_1.png',1,self,True,None,self.npc_sounds[1]),
                (280, 341,'Bobo',[ '\nHmm le mot de passe est 667'], 'images/npc/npc_bad_2.png',1,self,True,None,self.npc_sounds[1]),
                (660,60, 'Baba :', ['\nLe mot de passe est....','\nje sais pas'], 'images/npc/npc_bad_3.png',2,self,True,None,self.npc_sounds[1]),
                (740,320, 'Fdp :', ['\nJe jure Bob il fait peur'],'images/npc/npc_bad_4.png',1,self,True,None,self.npc_sounds[1]),
                (280,553,'dark_madao :', ['\nJe cherche mon clone'],'images/npc/npc_madao_1.png',1,self,True,None,self.npc_sounds[1])),
                (()),(())
                ]
        self.tab_house = [((140,87,'images/backgrounds/house1.png'),
                 (700, 281,'images/backgrounds/house1.png'),
                 (140, 490, 'images/backgrounds/house1.png')),
                 (()),(()),(())]
        self.tab_monster = [(()),(()),(()),((30,400,'images/monster/monster_test.png',30,10,1000,1,self,2),(134,230,'images/monster/monster_test.png',30,10,1000,1,self,2)),
                            ((600,500,'images/npc/npc_madao_1.png',30,10,1000,1,self,None),(700,400,'images/npc/npc_madao_2.png',30,10,1000,1,self,None)),(())]
        self.tab_monster_melee = [(()),(()),(()),((400,150,'images/monster/monster_test.png',30,10,1000,1,self,1),(200,400,'images/monster/monster_test.png',30,10,1000,1,self,1)),(())]

                       
        self.walls_verti = [(()),
                            ((30, 10,'images/backgrounds/wall.png',150,220,self)),
                            ((320, 30,'images/backgrounds/wall.png',10,220,self),(320, 30,'images/backgrounds/wall.png',10,220,self)),
                            (0,0,'images/border.png'),
                            ((395,269,'images/backgrounds/wall.png',75,70,self),(528,266,'images/backgrounds/wall.png',75,80,self),
                            (243,273,'images/backgrounds/wall.png',90,75,self),(389,116,'images/backgrounds/wall.png',80,93,self),
                            (528,114,'images/backgrounds/wall.png',88,90,self), (663,277,'images/backgrounds/wall.png',128,73,self),
                            (674,226,'images/backgrounds/wall.png',75,36,self),(278,236,'images/backgrounds/wall.png',60,40,self),
                            (635,160,'images/backgrounds/wall.png',38,50,self), (317,170,'images/backgrounds/wall.png',36,45,self))]
        
        self.walls_hori = [(()),
                           ((300, 200,'images/backgrounds/wall.png',50,50,self)),
                           ((215,255,'images/backgrounds/wall.png',650,10,self),(215,255,'images/backgrounds/wall.png',650,10,self)),
                           (0,0,'images/backgrounds/border.png'),
                           ((238,432,'images/backgrounds/wall.png',100,88,self),(395,429,'images/backgrounds/wall.png',65,80,self),
                            (387,569,'images/backgrounds/wall.png',82,134,self),(258,527,'images/backgrounds/wall.png',81,57,self),
                            (348,572,'images/backgrounds/wall.png',32,77,self), (528,430,'images/backgrounds/wall.png',67,81,self),
                            (661,429,'images/backgrounds/wall.png',115,93,self),(527,570,'images/backgrounds/wall.png',85,133,self),
                            (620,573,'images/backgrounds/wall.png',89,52,self), (660,526,'images/backgrounds/wall.png',69,39,self))]
        
        self.current_map = 0
        
        self.tab_npc_map = [[] for _ in range(len(self.tab_npc))]
        self.tab_house_map = [[] for _ in range(len(self.tab_house))]
        self.tab_fake_house_map =[[] for _ in range(len(self.tab_house))] 
        self.tab_monster_map = [[] for _ in range(len(self.tab_monster))]
        self.tab_monster_melee_map = [[] for _ in range(len(self.tab_monster_melee))]
        self.chest_map = [[] for _ in range(len(self.chest_tab))]
        self.wall_per_map_hori = [[] for _ in range(len(self.walls_hori))]
        self.wall_per_map_verti = [[] for _ in range(len(self.walls_verti))]
        self.backgrounds = ['images/backgrounds/background_npc_town.png','images/backgrounds/crossroad.png','images/backgrounds/house_inside.png','images/backgrounds/map_monster.png','images/backgrounds/boss_room2.png']
        self.background = ''

        self.waypoints_tab = [(Waypoint(600,700,'images/backgrounds/waypoint.png',1,self),
                               ),
                              (Waypoint(450,50,'images/backgrounds/waypoint.png',4,self),
                              Waypoint(900,370,'images/backgrounds/waypoint.png',3,self),
                              Waypoint(30,370,'images/backgrounds/waypoint.png',2,self),
                              ),

                              (Waypoint(600,700,'images/backgrounds/waypoint.png',1,self),
                               ),
                               (Waypoint(600,700,'images/backgrounds/waypoint.png',1,self),
                               ),]

        self.fps = 60
        self.clock = pygame.time.Clock()
        self.current_frame = 0
        self.frame_counter = 0
        self.muted = False
        self.fireball =pygame.image.load('images/fireball.png') 
        self.all_sprites = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.fake_houses = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()
        self.waypoints =pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.nb_voisins = [5,3,5,0,0]
        self.nb_maisons = [3,0,0,0,0]
        self.nb_walls = [0,0,2,0,10]
        self.nb_waypoints = [1,3,1,1,0]
        self.nb_monsters = [0,0,0,2,0]
        self.nb_boss = [0,0,0,0,1]
        self.nb_chest = [0,0,1,0,0]
        self.completed_objectives = []
        self.init_player()
        self.init_house()
        self.init_npc()
        self.init_walls()
        self.init_waypoint()
        self.init_monster()
        self.init_background()
        self.init_game()
        
        

    def init_chest(self):
        for quest in self.player.completed_quest:
            if quest is not None and quest.id == 1:
                return
        for i in range(self.nb_chest[self.current_map]):
            self.chest_map[self.current_map].append((Chest(self.chest_tab[self.current_map][0],
                                                               self.chest_tab[self.current_map][1],
                                                               self.chest_tab[self.current_map][2],
                                                               self.chest_tab[self.current_map][3],
                                                               self.chest_tab[self.current_map][4],
                                                               self.chest_tab[self.current_map][5])
                                                               ))        
            
            self.chests.add(self.chest_map[self.current_map][i])
            self.all_sprites.add(self.chest_map[self.current_map][i])

    def init_chests_per_map(self):
        for chest_nb in self.chests:
                self.screen.blit(chest_nb.image, chest_nb.rect)
    def clear_chests(self):
        for chest in self.chests:
            chest.kill()
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
        if self.current_map == 0:
                self.quest.holder = self.tab_npc_map[0][4] 
        if self.current_map == 1:
                self.quest2.holder = self.tab_npc_map[1][0]
                self.quest3.holder = self.tab_npc_map[1][2]
                self.quest4.holder = self.tab_npc_map[1][1]
        if self.current_map == 2:
            self.tab_npc_map[2][1].password_found = True

    def init_npc_per_map(self):
        for npc_nb in self.npcs:
                self.screen.blit(npc_nb.image, npc_nb.rect)

    def clear_npc(self):
        for npc in self.tab_npc_map[self.current_map] if self.tab_npc_map[self.current_map] else []:
            npc.health = 0
            npc.quest = None
            npc.kill() 
        self.tab_npc_map[self.current_map] = []

    def clear_house(self):
        for house in self.tab_house_map[self.current_map] if self.tab_house_map[self.current_map] else []:
            house.kill()
        self.tab_house_map[self.current_map] = []

    def clear_fake_house(self):
        for house in self.tab_fake_house_map[self.current_map] if self.tab_fake_house_map[self.current_map] else []:
            house.kill()
        self.tab_fake_house_map[self.current_map] = []
    def clear_walls(self):
        for i in range(self.nb_walls[self.current_map]):
            self.wall_per_map_hori[self.current_map][i].kill()
            self.wall_per_map_verti[self.current_map][i].kill()
        if self.nb_walls[self.current_map] is not []:
            self.wall_per_map_hori[self.current_map] = []
            self.wall_per_map_verti[self.current_map] = []
    def clear_monster(self):
        for monster in self.tab_monster_map[self.current_map] if self.tab_monster_map[self.current_map] else []:
            monster.kill()
        self.tab_monster_map[self.current_map] = []
        for monster in self.tab_monster_melee_map[self.current_map] if self.tab_monster_melee_map[self.current_map] else []:
            monster.kill()
        self.tab_monster_melee_map[self.current_map] = []
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
            self.wall_per_map_verti[self.current_map].append(Wall_verti(self.walls_verti[self.current_map][i][0],
                                                    self.walls_verti[self.current_map][i][1],
                                                    self.walls_verti[self.current_map][i][2],
                                                    self.walls_verti[self.current_map][i][3],
                                                    self.walls_verti[self.current_map][i][4],
                                                    self.walls_verti[self.current_map][i][5]))
            
            self.wall_per_map_hori[self.current_map].append (Wall_hori(self.walls_hori[self.current_map][i][0],
                                                    self.walls_hori[self.current_map][i][1],
                                                    self.walls_hori[self.current_map][i][2],
                                                    self.walls_hori[self.current_map][i][3],
                                                    self.walls_hori[self.current_map][i][4],
                                                    self.walls_hori[self.current_map][i][5]))
            
            self.all_walls.add(self.wall_per_map_verti[self.current_map][i])
            self.all_walls.add(self.wall_per_map_hori[self.current_map][i])
            self.all_sprites.add(self.wall_per_map_hori[self.current_map][i])
            self.all_sprites.add(self.wall_per_map_verti[self.current_map][i])

    def init_walls_per_map(self):
        for walls in self.all_walls:
            self.screen.blit(walls.image, walls.rect)

    def init_background(self) :
        self.background= pygame.image.load(self.backgrounds[self.current_map])
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.dq_background = pygame.transform.scale(pygame.image.load('images/inventory/dq_background.png'), (self.width,self.height))

        
    def init_waypoint(self):
        for i in range(self.nb_waypoints[self.current_map]):
            waypoint = self.waypoints_tab[self.current_map][i]
            self.waypoints.add(waypoint)

    def init_waypoint_per_map(self):
        for waypoints in self.waypoints:
            self.screen.blit(waypoints.image, waypoints.rect)
        
    def clear_waypoint(self):
        for waypoint in self.waypoints:
            waypoint.kill()

    def init_fireball(self):
        for fireball in self.fireballs:
            fireball.update()
            fireball.draw(self.screen)
    def init_player(self):
        self.player = Player(self)
        self.all_sprites.add(self.player)

    def npc_update(self):
        npc = random.choice(self.tab_npc_map[self.current_map])
        npc.update()

    def show_player(self):
            if not self.player.inventory_open:
                self.frame_counter = (self.frame_counter + 1) % (self.fps//8)
                self.screen.blit(self.player.frames[self.player.current_direction][self.current_frame], (self.player.rect.x, self.player.rect.y))

                if self.frame_counter == 0:
                    self.current_frame = (self.current_frame + 1) % 9
                    
    def init_monster(self):
        for i in range(self.nb_monsters[self.current_map]):
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

        for i in range(self.nb_monsters[self.current_map]):

            self.tab_monster_melee_map[self.current_map].append(Monster_melee(self.tab_monster_melee[self.current_map][i][0],
                                                                  self.tab_monster_melee[self.current_map][i][1],
                                                                  self.tab_monster_melee[self.current_map][i][2],
                                                                  self.tab_monster_melee[self.current_map][i][3],
                                                                  self.tab_monster_melee[self.current_map][i][4],
                                                                  self.tab_monster_melee[self.current_map][i][5],
                                                                  self.tab_monster_melee[self.current_map][i][6],
                                                                  self.tab_monster_melee[self.current_map][i][7],
                                                                  self.tab_monster_melee[self.current_map][i][8]))
            self.all_sprites.add(self.tab_monster_melee_map[self.current_map][i])
            self.monsters.add(self.tab_monster_melee_map[self.current_map][i])
        for i in range(self.nb_boss[self.current_map]):
            self.tab_monster_map[self.current_map].append(Boss(self.tab_monster[self.current_map][i][0],
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

    def check_fireball_collision(self):
        for fireball in self.fireballs:
            if pygame.sprite.collide_rect(self.player, fireball):
                self.player.health -= fireball.damage 
                if self.player.health <= 0:
                    self.game_over()
                self.fireballs.remove(fireball)
                fireball.kill()
    def show_weapon(self):
        if self.player.inventory.current_weapon is not None:
            self.screen.blit(pygame.transform.scale(self.player.inventory.current_weapon.image,(50,50)),(900,700))
    
    def show_hp(self):
        hp = self.font.render(str(self.player.health), True, (255, 0, 0))
        self.screen.blit(hp, (800, 700))
        for npc in self.npcs:
            npc.show_health()
    def show_mana(self):
        mana = self.font.render(str(self.player.mana), True, (0, 0, 255))
        self.screen.blit(mana, (800, 750))
    def game_over(self):
        self.screen.fill((0,0,0))
        game_over = self.font.render("Game over", True, (255, 0, 0))
        self.screen.blit(game_over, (400, 400))
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()
        quit()
    def won_game(self):
        self.screen.fill((0,0,0))
        game_over = self.font.render("gg mgl", True, (255, 0, 0))
        self.screen.blit(game_over, (400, 400))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        quit()
    
    def show_circle_range(self):
        if self.player.showing_range:
            pygame.draw.circle(self.screen, (255, 0, 0), self.player.rect.center, self.player.attack_range, 1)
    
    def check_quest(self):
        for quest in self.player.on_going_quest:
            if quest is not None:
                quest.update_objectives()
                quest.is_completed()
                for objective in quest.objectives:
                    if objective['completed'] and not objective['shown']:
                        self.completed_objectives.append(objective)  

    def displaye_objective(self):
        for objective in self.completed_objectives:
            objective['shown'] = True 
            objective_done = self.font.render(f"{objective['name']} (Completed)", True, (135,255,255))
            self.screen.blit(objective_done, (600,10))
            objective['display_counter'] -= 1
        
            if objective['display_counter'] <= 0:  
                self.completed_objectives.remove(objective)
    def clear_all(self):
        self.clear_fake_house()
        self.clear_chests()
        self.clear_house()
        self.clear_npc()
        self.clear_npc()
        self.clear_waypoint()
        self.clear_walls()
        self.clear_monster()
    
    def init_all(self):
        self.init_background()
        self.init_monster()
        self.init_fireball()
        self.init_walls()
        self.init_house()
        self.init_waypoint()
        self.init_npc()
        self.init_chest()

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
            self.check_fireball_collision()
            self.init_fake_house_per_map()
            self.init_walls_per_map()
            self.screen.blit(self.background, (0,0))
            
            self.show_circle_range()
            self.init_house_per_map()
            self.init_npc_per_map()
            self.init_waypoint_per_map()
            self.init_chests_per_map()

            self.player.show_text()
            self.init_fireball()
            self.player.move()
            
            self.show_player()
            self.player.is_end_end()
            self.show_weapon()
            self.show_hp()
            self.show_mana()
            self.check_quest()
            self.displaye_objective()
            #self.npc_update()
            

            for monster in self.monsters:
                monster.update()

            pygame.display.flip()