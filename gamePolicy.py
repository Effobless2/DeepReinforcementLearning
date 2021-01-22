import gameConstants
import copy
import random

DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR = 1e-2, 1

REWARDS = {
    gameConstants.WALL           : -10000,
    gameConstants.PLAYER         : -10,
    gameConstants.PLAYER_ON_GOAL : -10,
    gameConstants.BOX            : -2,
    gameConstants.BOX_ON_GOAL    : +10000,
    gameConstants.GOAL           : -10,
    gameConstants.FLOOR          : -10,
    "LOOSE"                      : -100
}

class Policy:
    def __init__(self, states, actions, learning_rate = DEFAULT_LEARNING_RATE, discount_factor = DEFAULT_DISCOUNT_FACTOR, table = None):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        if table == None:
            self.table = {}
            for s in states:
                self.table[s] = {}
                for a in actions:
                    self.table[s][a] = {}
                    self.table[s][a][True] = 0
                    self.table[s][a][False] = 0
        else:
            self.table = table

    def __repr__(self):
        result = ""
        for items in self.table.items():
            result += str(items[0]) + " : " + str(items[1]) + "\n"
        return result

    def best_action(self, state, availableActions, environnement):
        action = None
        reward = None
        blockMoved = False
        for currentAction in self.table[state].keys():
            if currentAction in availableActions.keys():
                # Calculer reward de l'action
                currentReward = self.table[state][currentAction][availableActions[currentAction]] #TODO
                if not action or currentReward > reward:
                    action = currentAction
                    reward = currentReward
                    blockMoved = availableActions[currentAction]
        return (action, blockMoved)

    def update(self, previous_state, state, last_action, environnement, reward, blockHasMoved):
        maxQ = max( max(i.values()) for i in self.table[state].values())
        self.table[previous_state][last_action][blockHasMoved] += reward + self.learning_rate * (self.discount_factor * maxQ - self.table[previous_state][last_action][blockHasMoved])
