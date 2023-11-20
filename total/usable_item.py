
from item import Item

class Usable_Item(Item):
    def __init__(self, name, description, value,rarity,path,game,usage,):
        super().__init__(name, description, value,rarity,path,game)
        self.usage = usage

    def use(self):
        print("je")
        self.usage()