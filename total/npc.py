from mysprite import mySprite



class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path,max_dialogue,game,is_killable):
        super().__init__(x,y,path)
        self.name = name
        self.game = game
        self.is_killable = is_killable
        self.max_dialogue = max_dialogue
        self.dialogue = dialogue
        self.current_id = 0
        self.dialogue_id = 0
        self.action = [self.parler, self.kill]  

    def actions(self):
        self.action[self.current_id]()

    def parler(self):
        if self.dialogue_id == self.max_dialogue:
            self.dialogue_id = 0
        self.game.player.text = self.dialogue [self.dialogue_id]

    def kill(self):
        self.game.all_sprites.remove(self)
        self.game.npcs.remove(self)
        self.game.player.nb_voisin -= 1

    def next_step(self):
        self.current_id += 1
        if self.current_id >= len(self.action):
            self.current_id = 0

    def dialogue_next(self):
        self.dialogue_id+=1