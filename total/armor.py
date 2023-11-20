from item import Item

class Armor(Item):
    def __init__(self, name, description, value,rarity,path,game,defense,):
        super().__init__(name, description, value,rarity,path,game)
        self.defense = defense

