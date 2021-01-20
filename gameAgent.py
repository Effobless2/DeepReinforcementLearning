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

    def do(self):
        action = self.best_action()
        if action != None :
            self.previous_state = self.state
            self.state, blockHasMoved, state_content = self.environment.apply(self.state, action)
            reward = gamePolicy.REWARDS[state_content]
            self.last_action = action
            self.update_policy(reward)
            self.actionNumber += 1
            self.score += reward
            print("Tour: ", self.actionNumber)
            print("Score: " + str(self.score))
        if self.environment.lose():
            return False
        elif self.environment.win():
            print("won")
            return False
        return True

    def update_policy(self, reward):
        self.policy.update(self.previous_state, self.state, self.last_action, self.environment, reward)