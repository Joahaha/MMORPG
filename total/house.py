import pygame
from mysprite import mySprite

class House(mySprite):
    def __init__(self,x,y,path):    
        super().__init__(x,y,path)
        
        original_width, original_height = self.image.get_size()
        aspect_ratio = original_width / original_height

        new_width = 160
        new_height = int(new_width / aspect_ratio)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y