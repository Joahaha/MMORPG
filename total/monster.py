import pygame
import random
from mysprite import mySprite
from fireball import Fireball
class Monster(mySprite):
    def __init__(self, x, y, path, attack, defense, health, speed, game, nb,detection_range=400, attack_range=400):
        super().__init__(x, y, path)
        self.attack_power = attack
        self.defense = defense
        self.health = health
        self.speed = speed
        self.game = game
        self.detection_range = detection_range
        self.attack_range = attack_range
        self.sprites = self.load_sprite_sheet('images/monster/monster_sprite_sheets_1.png', (32, 32),nb)
        self.current_sprite = 0
        self.font = pygame.font.Font(None, 25)  
        self.frame_counter = 0
        self.attack_cooldown = 0

    def move(self):
        if self.attack_cooldown > 0:
            return
        player_distance = ((self.game.player.rect.x - self.rect.x)**2 + (self.game.player.rect.y - self.rect.y)**2)**0.5

        if player_distance < self.detection_range:
            if self.rect.x < self.game.player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > self.game.player.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < self.game.player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > self.game.player.rect.y:
                self.rect.y -= self.speed


    def load_sprite_sheet(self, sprite_sheet_path, sprite_size,nb):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sprite_list = []
        for y in range(0, sprite_sheet.get_height(), sprite_size[1]):
            for x in range(96*nb, sprite_sheet.get_width(), sprite_size[0]):
                if len(sprite_list) < 3:
                    sprite = pygame.Surface(sprite_size, pygame.SRCALPHA)
                    sprite.blit(sprite_sheet, (0, 0), (x, y, sprite_size[0], sprite_size[1]))
                    sprite_list.append(sprite)
        return sprite_list

    
    def attack_player(self, player):
        if self.attack_cooldown == 0:
            if self.health < 500:
                 fireball = Fireball(self.rect.topleft, player.rect.center, self.game,10,40)
            else:
                fireball = Fireball(self.rect.topleft, player.rect.center, self.game,10,20)
            self.game.fireballs.add(fireball)
            self.attack_cooldown = 60


    def kill(self):
            if self.health <= 0:
                self.game.all_sprites.remove(self)
                self.game.monsters.remove(self)
                self.game.tab_monster_map[self.game.current_map].remove(self)
                self.game.player.health += 10
                self.game.player.gold += 10
    def check_attack(self, player):
        player_distance = ((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)**0.5
        if player_distance < self.attack_range  and self.attack_cooldown == 0:
            self.attack_player(player)
            self.attack_cooldown = 60

    def show_health(self):
        health_text = self.font.render(str(self.health), True, (255, 0, 0)) 
        self.game.screen.blit(health_text, (self.rect.x, self.rect.y - 20))  

    def show_monster(self):
        self.image = self.sprites[self.current_sprite]
        self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.game.screen.blit(self.image, self.rect)

    def dash(self, player):
        if self.attack_cooldown > 0:
            return
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.rect.x += self.speed+3 * dx / distance
            self.rect.y += self.speed +3* dy / distance

    def update(self):
        self.move()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        self.check_attack(self.game.player)
        self.show_health()
        if self.frame_counter % 10 == 0:
            self.image = self.sprites[self.current_sprite]
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)

        self.frame_counter += 1  
        if self.health < 500: 
            self.sprites = self.load_sprite_sheet('images/monster/monster_sprite_sheets_1.png', (32, 32),3)
            self.dash(self.game.player)
        self.show_monster()
        self.kill()