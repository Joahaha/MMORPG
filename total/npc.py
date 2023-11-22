from mysprite import mySprite
import random



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
        self.speed = 1
        self.is_in_contact = False
        

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
            if self.health <= 0:
                self.game.all_sprites.remove(self)
                self.game.npcs.remove(self)
                self.game.player.nb_voisin -= 1
            else :
                self.health -= self.game.player.atq
        

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