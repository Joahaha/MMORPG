class Quest:
    def __init__(self, name, description, objectives, reward):
        self.name = name
        self.description = description
        self.objectives = objectives 
        self.reward = reward
        self.status = 'Not started'

    def start(self):
        self.status = 'In progress'

    def complete_objective(self, objective):
        if objective in self.objectives:
            self.objectives.remove(objective)
            if not self.objectives:
                self.complete()

    def complete(self):
        self.status = 'Completed'

    def is_completed(self):
        return self.status == 'Completed'