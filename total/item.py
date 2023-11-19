import pygame
from pygame.locals import *

class Item:
    def __init__(self, name, description, value,rarity,game):
        self.name = name
        self.description = description
        self.value = value
        self.rarity = rarity
        self.game = game

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Value: {self.value}")

    