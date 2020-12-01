import gameConstants
import copy

DEFAULT_LEARNING_RATE, DEFAULT_DISCOUNT_FACTOR = 1, 0.4

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

    def best_action(self, state, availableActions, environnement):
        action = None
        reward = None
        for currentAction in self.table[state]:
            if currentAction in availableActions:
                # Calculer reward de l'action
                currentReward = self.preventReward(state, currentAction, environnement) + self.table[state][currentAction] #TODO
                if not action or currentReward > reward:
                    action = currentAction
                    reward = currentReward
        return action

    def preventReward(self, state, action, environnement):
        template = copy.deepcopy(environnement)
        new_state, blockHasMoved = template.apply(state, action)
        reward = self.defineReward(template)
        if blockHasMoved == 1:
            reward+= 100
        elif blockHasMoved == 2:
            reward -= 50
        return reward
     #   newPos = environnement.stateAfterMove(state, action)
     #   newPosContent = environnement.getContent(newPos[0], newPos[1])
     #   if newPosContent == gameConstants.BOX or newPosContent == gameConstants.BOX_ON_GOAL:
     #       nextPos = environnement.stateAfterMove(newPos, action)
     #       nextPosContent = environnement.getContent(nextPos[0], nextPos[1])
     #       if nextPosContent == gameConstants.GOAL:
     #           return 1000000000
     #       if nextPosContent == gameConstants.FLOOR:
     #           print("caca")
     #           return -5
     #       if nextPosContent == gameConstants.WALL:
     #           return -100
     #       if nextPosContent == gameConstants.BOX or nextPosContent == gameConstants.BOX_ON_GOAL: 
     #           availableActions = environnement.availableActions(nextPos, True)
     #           if action == gameConstants.UP and gameConstants.DOWN not in availableActions:
     #               availableActions.append(gameConstants.DOWN)
     #           elif action == gameConstants.DOWN and gameConstants.UP not in availableActions:
     #               availableActions.append(gameConstants.UP)
     #           elif action == gameConstants.LEFT and gameConstants.RIGHT not in availableActions:
     #               availableActions.append(gameConstants.RIGHT)
     #           elif action == gameConstants.RIGHT and gameConstants.LEFT not in availableActions:
     #               availableActions.append(gameConstants.LEFT)
     #           if len(availableActions) < 3:
     #               if gameConstants.UP in availableActions :
     #                   if gameConstants.DOWN in availableActions :
     #                       return -10 #TODO
     #               if gameConstants.LEFT in availableActions:
     #                   if gameConstants.RIGHT in availableActions:
     #                       return -10 #TODO
     #               return -100 #TODO
     #           return -100
     #   return -50


    def update(self, previous_state, state, last_action, environnement, blockHasMoved):
        maxQ = max(self.table[state].values())
        reward = self.defineReward(environnement)
        if blockHasMoved == 1:
            reward+= 100
        elif blockHasMoved == 2:
            reward -= 50
        self.table[previous_state][last_action] += reward + self.learning_rate * (self.discount_factor * maxQ - self.table[previous_state][last_action])
        print("Reward: ", reward)


    def defineReward(self, environnement):
        if environnement.win():
            return 10000000
        if environnement.lose():
            return -10000000
        reward = 0
        for i in range(environnement.height()):
            for j in range(environnement.width(i)):
                content = environnement.getContent(i, j)
                if content == gameConstants.BOX:
                    availableActions = environnement.availableActions((i,j), True)
                    if len(availableActions) < 2:
                        reward -= 10 #TODO
                    elif len(availableActions) == 2:
                        if gameConstants.UP in availableActions :
                            if gameConstants.DOWN in availableActions :
                                reward -= 5 #TODO
                            else:
                                reward -= 10 #TODO
                        elif gameConstants.LEFT in availableActions:
                            if gameConstants.RIGHT in availableActions:
                                reward -= 5 #TODO
                            else:
                                reward -= 10 #TODO
                    else:
                        reward -= 5 #TODO
                elif content == gameConstants.BOX_ON_GOAL:
                    availableActions = environnement.availableActions((i,j), True)
                    if len(availableActions) < 2:
                        reward -= 30 #TODO
                    elif len(availableActions) == 2:
                        if gameConstants.UP in availableActions :
                            if gameConstants.DOWN in availableActions :
                                reward -= 10 #TODO
                            else:
                                reward -= 20 #TODO
                        elif gameConstants.LEFT in availableActions:
                            if gameConstants.RIGHT in availableActions:
                                reward -= 10 #TODO
                            else:
                                reward -= 20 #TODO
                    else:
                        reward -= 8 #TODO
        return reward
