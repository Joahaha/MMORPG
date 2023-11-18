
from item import Item
from game import Game

class Weapon(Item):
    def __init__(self, name, description, value,damage,game):
        super().__init__(name, description, value)
        self.damage = damage
        self.game = game

    def attack(self):
        self.game.player.attack(self.damage)
