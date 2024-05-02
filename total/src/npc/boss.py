from monster import Monster
from monster_mele import Monster_melee
import pygame
from fireball import Fireball

class Boss(Monster):
    def __init__(self,x, y, path, attack, defense, health, speed, game,nb):
        super().__init__(x, y, path, attack, defense, health, speed, game,nb)
        self.health = 10000 
        self.speed = 5 
        self.attack_range = 200 
        self.attack_power = 50  
        self.sprites = pygame.image.load(path)
        self.summon_cooldown = 0

    def attack_player(self, player):
        if self.attack_cooldown == 0:
            fireball = Fireball(self.rect.topleft, player.rect.center, self.game, 20, 30)  
            self.game.fireballs.add(fireball)
            self.attack_cooldown = 30

    def kill(self):
        if self.health <= 0:
            self.game.player.finished_game = True
            self.game.all_sprites.remove(self)
            self.game.monsters.remove(self)
            self.game.nb_monsters[self.game.current_map] -= 1
            self.game.tab_monster_map[self.game.current_map].remove(self)
            self.game.player.health += 50  
            self.game.player.gold += 50  
    def summon_minions(self):
        if self.summon_cooldown == 0 and self.game.nb_monsters[self.game.current_map] < 3:
            for _ in range(3):  
                minion = Monster_melee(self.rect.centerx, self.rect.centery, 'images/monster/monster_sprite_sheets_1.png', 10, 10, 300, 2, self.game, 3)  
                self.game.monsters.add(minion)
                self.game.all_sprites.add(minion)
                self.game.tab_monster_melee_map[self.game.current_map].append(minion)
                self.game.nb_monsters[self.game.current_map] += 1
            self.summon_cooldown = 60 
    def show_monster(self):
        self.image = self.sprites
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        super().update() 
        self.summon_minions() 
        self.summon_cooldown-=1