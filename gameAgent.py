import gamePolicy
import gameConstants

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = gamePolicy.Policy(environment.states.keys(), gameConstants.ACTIONS)
        self.reset()
        
    def reset(self):
        self.actionNumber = 0
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.last_action = None
        self.score = 0

    def best_action(self):
        availableActions = self.environment.availableActions(self.state)
        return self.policy.best_action(self.state, availableActions, self.environment)

    def do(self, action):
        self.actionNumber += 1
        print("Tour: {0}", self.actionNumber)
        self.previous_state = self.state
        self.state, blockHasMoved = self.environment.apply(self.state, action)
        self.last_action = action
        self.update_policy(blockHasMoved)

    def update_policy(self, blockHasMoved):
        self.policy.update(self.previous_state, self.state, self.last_action, self.environment, blockHasMoved)