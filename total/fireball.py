import pygame


class Fireball(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos,game, speed,taille,):
        super().__init__() 
        self.rect = pygame.Rect(start_pos, (20, 20))    
        self.image = pygame.image.load('images/fireball.png') 
        self.image = pygame.transform.scale(self.image, (taille, taille)) 
        self.damage = 10
        self.game = game
        self.speed = speed
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.velocity = (speed * dx / distance, speed * dy / distance)
        else:
            self.velocity = (0, 0)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x < 0 or self.rect.y < 0 or self.rect.x > self.game.width or self.rect.y > self.game.height:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
