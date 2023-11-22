from mysprite import mySprite
import random
import pygame



class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path,max_dialogue,game,is_killable,quest,talk_sound):
        super().__init__(x,y,path)
        self.name = name
        self.game = game
        self.is_killable = is_killable
        self.max_dialogue = max_dialogue
        self.dialogue = dialogue
        self.possible_interaction =''
        self.current_id = 0
        self.movement_id = 0
        self.dialogue_id = 0
        self.action = [self.parler, self.kill,self.trade,self.sell]  
        self.action_names = ["parler", "kill", "trade", "sell"]
        self.movement = [self.move,self.freeze,self.fuir]
        self.quest=quest
        self.told_quest = False
        self.talk_sound = talk_sound
        self.health = 100
        self.detection_range = 200
        self.speed = 5
        self.is_in_contact = False
        self.font = pygame.font.Font(None, 25)  
        self.frame_counter = 0
        self.target_x = x
        self.target_y = y
        
        

    def actions(self):
        self.action[self.current_id]()

    def bouger(self):
        if self.health !=100:
            self.movement_id = 2
        self.movement[self.movement_id]()

    def parler(self):
        if self.dialogue_id == self.max_dialogue:
            self.dialogue_id = 0
        self.game.player.text += self.name
        if self.quest is not None:
            self.game.player.quest = True
            self.told_quest = True
        self.game.player.text += self.dialogue [self.dialogue_id]


    def kill(self):
        if self.quest is None:
            self.health -= self.game.player.atq
            if self.health <= 0:
                self.game.all_sprites.remove(self)
                self.game.npcs.remove(self)
                self.game.player.nb_voisin -= 1
           
    def __delete__(self):
        print("hi")

    def trade(self):
        pass    
    
    def sell(self):
        pass

    def move(self):
        new_x = self.rect.x + random.randint(-self.speed*3, self.speed*3)
        new_y = self.rect.y + random.randint(-self.speed*3, self.speed*3)

        if 0 <= new_x <= self.game.width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.game.height - self.rect.height:
            self.rect.y = new_y


    def freeze(self):
        pass

    def fuir(self):
        player_distance = ((self.game.player.rect.x - self.rect.x)**2 + (self.game.player.rect.y - self.rect.y)**2)**0.5
        if player_distance < self.detection_range:
            new_x = self.rect.x
            new_y = self.rect.y

            if self.rect.x < self.game.player.rect.x:
                new_x -= self.speed
            elif self.rect.x > self.game.player.rect.x:
                new_x += self.speed

            if self.rect.y < self.game.player.rect.y:
                new_y -= self.speed
            elif self.rect.y > self.game.player.rect.y:
                new_y += self.speed

            if 0 <= new_x <= self.game.width - self.rect.width:
                self.rect.x = new_x
            if 0 <= new_y <= self.game.height - self.rect.height:
                self.rect.y = new_y
        else:
            self.move()
        
    def show_interaction(self):
        text = "Press e to "
        text += self.action_names[self.current_id]
        if self.quest is not None and self.told_quest:
            text += "\nPress w to show quest"
        self.possible_interaction= text

    def next_step(self):
        self.current_id += 1

    def dialogue_next(self):
        self.dialogue_id+=1

    def show_health(self):
        if self.is_killable:
            health_text = self.font.render(str(self.health), True, (0, 255, 0)) 
            self.game.screen.blit(health_text, (self.rect.x +10, self.rect.y +50))  

    def set_random_target(self):
        self.target_x = random.randint(0, self.game.width)
        self.target_y = random.randint(0, self.game.height)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= 20:
            for npc in self.game.npcs:
                npc.frame_counter =0
            if self.target_x is None and self.target_y is None:
                self.set_random_target()
            self.frame_counter = 0

        if self.target_x is not None and self.target_y is not None:

            if abs(self.rect.x - self.target_x) <= self.speed:
                self.rect.x = self.target_x
            if self.rect.x < self.target_x:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

            if abs(self.rect.y - self.target_y) <= self.speed:
                self.rect.y = self.target_y
            elif self.rect.y < self.target_y:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
        if self.target_x == self.rect.x:
            self.target_x = None
        if self.target_y == self.rect.y:
            self.target_y= None