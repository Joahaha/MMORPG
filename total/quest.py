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
            if objective['name'] == 'Defeat all the the enemy':
                if self.game.player.nb_voisin == 1:
                    objective['completed'] = True



    def display_objective(self, objective):
        if objective['completed'] and not objective['shown']:
            objective['display_counter'] = 20  