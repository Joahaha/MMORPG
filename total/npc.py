from mysprite import mySprite



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
        self.dialogue_id = 0
        self.action = [self.parler, self.kill,self.trade,self.sell]  
        self.action_names = ["parler", "kill", "trade", "sell"]
        self.quest=quest
        self.told_quest = False
        self.talk_sound = talk_sound

    def actions(self):
        self.action[self.current_id]()

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
            self.game.all_sprites.remove(self)
            self.game.npcs.remove(self)
            self.game.player.nb_voisin -= 1
    

    def trade(self):
        pass    
    
    def sell(self):
        pass

    def show_interaction(self):
        text = "Press e to "
        text += self.action_names[self.current_id]
        if self.quest is not None and self.told_quest:
            text += "\nPress q to show quest"
        self.possible_interaction= text

    def next_step(self):
        self.current_id += 1

    def dialogue_next(self):
        self.dialogue_id+=1