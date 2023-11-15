from mysprite import mySprite



class NPC(mySprite):
    def __init__(self,x,y,name,dialogue,path) :
        super().__init__(x,y,path)
        self.name = name
        self.dialogue = dialogue