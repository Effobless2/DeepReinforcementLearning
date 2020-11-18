import gameConstants

DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR = 1, 0.1

REWARDS = {
    gameConstants.WALL           : -100000,
    gameConstants.PLAYER         : -5,
    gameConstants.PLAYER_ON_GOAL : -5,
    gameConstants.BOX            : -5,
    gameConstants.BOX_ON_GOAL    : -10,
    gameConstants.GOAL           : -5,
    gameConstants.FLOOR          : -5    
}

class Policy:
    def __init__(self, states, actions, learning_rate = DEFAULT_LEARNING_RATE, discount_factor = DEFAULT_DISCOUNT_FACTOR):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.table = {}
        for s in states:
            self.table[s] = {}
            for a in actions:
                self.table[s][a] = 0

    def best_action(self, state, availableActions):
        action = None
        for a in self.table[state]:
            if a in availableActions and (not action or self.table[state][a] > self.table[state][action]):
                action = a
        return action

    def update(self, previous_state, state, last_action, cellContent):
        maxQ = max(self.table[state].values())
        reward = self.defineReward(cellContent)
        self.table[previous_state][last_action] += self.learning_rate * \
            (reward + self.discount_factor * maxQ - self.table[previous_state][last_action])

    def defineReward(self, cellContent):
        return REWARDS[cellContent]
