import gamePolicy
import gameConstants

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = gamePolicy.Policy(environment.states.keys(), gameConstants.ACTIONS)
        self.reset()
        
    def reset(self):
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.last_action = None
        self.score = 0

    def best_action(self):
        availableActions = self.environment.availableActions(self.state)
        print(availableActions)
        return self.policy.best_action(self.state, availableActions)

    def do(self, action):
        self.previous_state = self.state
        self.state, cellContent = self.environment.apply(self.state, action)
        self.last_action = action
        self.update_policy(cellContent)

    def update_policy(self, cellContent):
        self.policy.update(self.previous_state, self.state, self.last_action, cellContent)