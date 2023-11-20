from item import Item

class Weapon(Item):
    def __init__(self, name, description, value,rarity,path,game,damage,):
        super().__init__(name, description, value,rarity,path,game)
        self.damage = damage


