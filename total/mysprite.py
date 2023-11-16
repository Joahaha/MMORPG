import pygame

class mySprite(pygame.sprite.Sprite):
    def __init__(self,x,y,path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y