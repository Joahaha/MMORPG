class Quest:
    def __init__(self, name, description, objectives, reward,condition,post_text,holder,game_changer,id,game):
        self.name = name
        self.description = description
        self.objectives = objectives 
        self.reward = reward
        self.condition = condition
        self.status = 'Not started'
        self.post_text = post_text
        self.holder = holder
        self.game_changer = game_changer
        self.id = id
        self.game = game
        self.frame_counter = 0

    def start(self):
        self.status = 'In progress'


    def complete(self):
        self.status = 'Completed'

    def is_completed(self):
        for objective in self.objectives:
            if not objective['completed']:
                return False  
        self.status = 'Completed'
    
    def update_objectives(self):
        for objective in self.objectives:
            if objective['name'] == 'Defeat all the the enemy' and objective['completed'] == False:
                if self.game.player.nb_voisin == 1:
                    objective['completed'] = True
            if objective['name'] == 'Find the password' and objective['completed'] == False:
                if self.holder.game.player.password_found:
                    objective['completed'] = True
            if objective['name'] == 'Open the chest' and objective['completed'] == False:
                for item in self.game.player.inventory.unique_item:
                    if item.name == 'Golden key':
                        objective['completed'] = True
            if objective['name'] == 'Kill all the monster' and objective['completed'] == False:
                if self.game.current_map == 3 and self.game.nb_monsters[self.game.current_map] == 0:
                    objective['completed'] = True
            if objective['name'] == 'Bring the key and the heart' and objective['completed'] == False:
                if self.game.player.inventory.unique_item[0].name == 'Golden key' and self.game.player.inventory.unique_item[1].name == 'Monster heart':
                    objective['completed'] = True
                if self.game.player.inventory.unique_item[0].name == 'Monster heart' and self.game.player.inventory.unique_item[1].name == 'Golden key':
                    objective['completed'] = True
            if objective['name'] == 'Beat the boss' and objective['completed'] == False:
                print("yes")
                if self.game.player.finished_game:
                    print("yes2")
                    self.game.won_game()
                    objective['completed'] = True

    def add_reward(self,player):
        player.inventory.add_item(self.reward[2])
        player.gold += self.reward[0]
        player.inventory.add_weapon(self.reward[1])
        player.inventory.add_unique(self.reward[3])


    def display_objective(self, objective):
        if objective['completed'] and not objective['shown']:
            objective['display_counter'] = 20  