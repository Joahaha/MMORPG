from item import Item

class Weapon(Item):
    def __init__(self, name, description, value,rarity,game,damage,):
        super().__init__(name, description, value,rarity,game)
        self.damage = damage


    def attack(self):
        self.game.player.attack(self.damage)
