import gamePolicy

UP, DOWN, LEFT, RIGHT = 'U', 'D', 'L', 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = gamePolicy.Policy(environment.states.keys(), ACTIONS)
        self.reset()
        
    def reset(self):
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.last_action = None
        self.score = 0