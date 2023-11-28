import pygame
from mysprite import mySprite

class Waypoint(mySprite):
    def __init__(self,x,y,path,destination,game):
        super().__init__(x,y,path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.avaiable = False
        self.action_names = ["go next map", "chose destination"]
        self.action = [self.move, self.teleport]
        self.current_id = 0
        self.destination = destination


    def actions(self):
        self.action[self.current_id]()
    def move(self):
        self.game.player.update(self.destination)

    def teleport(self):
        self.game.player.update_before()

    
    def show_interaction(self):
        if self.destination == 4:
            completed_quest_ids = [quest.id for quest in self.game.player.completed_quest if quest is not None]
            if 2 in completed_quest_ids and 3 in completed_quest_ids:
                self.avaiable = True
                text = "Press e to fight the boss "
                self.possible_interaction= text
            else:
                text = "You need to complete the quests first"
                self.possible_interaction= text
                self.avaiable = False
        else:
            text = "Press e to "
            text += self.action_names[self.current_id]
            self.possible_interaction= text

    def kill(self):
        self.game.all_sprites.remove(self)
        self.game.waypoints.remove(self)