from mysprite import mySprite



class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path,max_dialogue,game,is_killable,quest):
        super().__init__(x,y,path)
        self.name = name
        self.game = game
        self.is_killable = is_killable
        self.max_dialogue = max_dialogue
        self.dialogue = dialogue
        self.current_id = 0
        self.dialogue_id = 0
        self.action = [self.parler, self.kill]  
        self.quest=quest

    def actions(self):
        self.action[self.current_id]()

    def parler(self):
        if self.dialogue_id == self.max_dialogue:
            self.dialogue_id = 0
        self.game.player.text += self.name
        if self.quest is not None:
            self.game.player.text += "\nQuest available: " + self.quest.name
        else :
            self.game.player.text += self.dialogue [self.dialogue_id]


    def kill(self):
        if self.quest is None:
            self.game.all_sprites.remove(self)
            self.game.npcs.remove(self)
            self.game.player.nb_voisin -= 1
        

    def next_step(self):
        self.current_id += 1
        if self.current_id >= len(self.action):
            self.current_id = 0

    def dialogue_next(self):
        self.dialogue_id+=1