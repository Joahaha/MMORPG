
from item import Item

class Usable_Item(Item):
    def __init__(self, name, description, value,rarity,game,usage,):
        super().__init__(name, description, value,rarity,game)
        self.usage = usage
