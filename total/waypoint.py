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
        text = "Press e to "
        text += self.action_names[self.current_id]
        self.possible_interaction= text

    def kill(self):
        print("kill")
        self.game.all_sprites.remove(self)
        self.game.waypoints.remove(self)