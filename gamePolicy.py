import gameConstants
import copy

DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR = 1, 0.8

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

    def __repr__(self):
        result = ""
        for items in self.table.items():
            result += str(items[0]) + " : " + str(items[1]) + "\n"
        return result


    def best_action(self, state, availableActions, environnement):
        action = None
        reward = None
        for currentAction in self.table[state]:
            if currentAction in availableActions:
                # Calculer reward de l'action
                currentReward = self.table[state][currentAction] #TODO
                if not action or currentReward > reward:
                    action = currentAction
                    reward = currentReward
        return action

    def preventReward(self, state, action, environnement):
        template = copy.deepcopy(environnement)
        new_state, blockHasMoved = template.apply(state, action)
        reward = self.defineReward(template)
        if blockHasMoved == 0:
            reward -= 100
        elif blockHasMoved == 1:
            reward += 100
        elif blockHasMoved == 2:
            reward += 10
        return reward - self.distanceToBox(environnement, new_state)


    def update(self, previous_state, state, last_action, environnement, blockHasMoved):
        maxQ = max(self.table[state].values())
        reward = self.defineReward(environnement)
        if blockHasMoved == 0:
            reward -= 100
        elif blockHasMoved == 1:
            reward += 100
        elif blockHasMoved == 2:
            reward += 10
        reward -= self.distanceToBox(environnement, state)
        self.table[previous_state][last_action] += reward + self.learning_rate * (self.discount_factor * maxQ - self.table[previous_state][last_action])
        print("Reward: ", reward)


    def defineReward(self, environnement):
        boxes = []
        goals = []
        if environnement.win():
            return 10000
        if environnement.lose():
            return -1000
        reward = 0
        for i in range(environnement.height()):
            for j in range(environnement.width(i)):
                content = environnement.getContent(i, j)
                if content == gameConstants.BOX:
                    boxes.append((i,j))
                    availableActions = environnement.availableActions((i,j), True)
                    if len(availableActions) == 2:
                        reward -= 10
                    else:
                        reward -= 1 #TODO
                elif content == gameConstants.BOX_ON_GOAL:
                    boxes.append((i,j))
                    goals.append((i,j))
                    reward += 100
                    availableActions = environnement.availableActions((i,j), True)
                    if len(availableActions) == 2:
                        reward -= 10
                    else:
                        reward -= 1 #TODO
                elif content == gameConstants.GOAL:
                    goals.append((i,j))
        distanceForGoals = dict()
        for i in range(len(boxes)):
            distanceForGoals[boxes[i]] = dict()
            for j in range(len(goals)):
                distanceForGoals[boxes[i]][goals[j]] = abs(boxes[i][0] - goals[j][0] + boxes[i][1] - goals[j][1])
        for (key, value) in distanceForGoals.items():
            reward -= sum(value.values())
        return reward

    def distanceToBox(self, environnement, state):
        boxes = []
        for i in range(environnement.height()):
            for j in range(environnement.width(i)):
                content = environnement.getContent(i, j)
                if content == gameConstants.BOX or gameConstants.BOX_ON_GOAL:
                    boxes.append((i,j))
        return min(abs(boxes[i][0] - state[0]) + abs(boxes[i][1] - state[1]) for i in range(len(boxes)))
