
from item import Item

class UsableItem(Item):
    def __init__(self, name, description, value,usage):
        super().__init__(name, description, value)
        self.usage = usage
