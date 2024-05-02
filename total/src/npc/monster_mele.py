from monster import Monster

class Monster_melee(Monster):
    def __init__(self, x, y, path, attack, defense, health, speed, game, nb, detection_range=200, attack_range=10):
        super().__init__(x, y, path, attack, defense, health, speed, game, nb, detection_range, attack_range)

    def attack_player(self, player):
        if self.attack_cooldown == 0:
            player.health -= self.attack_power - player.defense
            if player.health <= 0:
                self.game.game_over()
            self.attack_cooldown = 60

    def kill(self):
        if self.health <= 0:
            self.game.all_sprites.remove(self)
            self.game.monsters.remove(self)
            self.game.tab_monster_melee_map[self.game.current_map].remove(self)
            self.game.player.health += 10
            self.game.player.gold += 10