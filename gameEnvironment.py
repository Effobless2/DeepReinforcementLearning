import gameConstants


class Environment:
    def __init__(self, template):
        self.template = template.strip().split('\n')
        self.reset()

    def height(self):
        return len(self.template)
    
    def width(self, lineIndex):
        return len(self.template[lineIndex])

    def getContent(self, line, col):
        return self.states[(line, col)]

    def reset(self):
        self.states = {}
        self.starting_point = (0,0)
        lines = self.template
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] in [gameConstants.PLAYER, gameConstants.PLAYER_ON_GOAL]:
                    self.starting_point = (row, col)

    def availableActions(self, state, fromBlock = False):
        result = {}
        (up, blockMoved) = self.checkUpOK(state, fromBlock)
        if up :
            result[gameConstants.UP] = blockMoved
        (left, blockMoved) = self.checkLeftOK(state, fromBlock)
        if left :
            result[gameConstants.LEFT] = blockMoved
        (down, blockMoved) = self.checkDownOK(state, fromBlock)
        if down :
            result[gameConstants.DOWN] = blockMoved
        (right, blockMoved) = self.checkRightOK(state, fromBlock)
        if right :
            result[gameConstants.RIGHT] = blockMoved
        return result
            
    def checkUpOK(self, state, fromBlock = False):
        new_state = (state[0] - 1, state[1])
        if new_state[0] < 0 :
            return (False, False)
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return (False, False)
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return (False, False)
            else :
                return self.checkUpOK(new_state, True)
        return (True, fromBlock)

    def checkDownOK(self, state, fromBlock = False):
        new_state = (state[0] + 1, state[1])
        if new_state[0] >= len(self.template) :
            return (False, False)
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return (False, False)
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return (False, False)
            else :
                return self.checkDownOK(new_state, True)
        return (True, fromBlock)

    def checkLeftOK(self, state, fromBlock = False):
        new_state = (state[0], state[1] - 1)
        if new_state[1] < 0 :
            return (False, False)
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return (False, False)
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return (False, False)
            else :
                return self.checkLeftOK(new_state, True)
        return (True, fromBlock)

    def checkRightOK(self, state, fromBlock = False):
        new_state = (state[0], state[1] + 1)
        if new_state[1] >= len(self.template[new_state[0]]) :
            return (False, False)
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return (False, False)
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return (False, False)
            else :
                return self.checkRightOK(new_state, True)
        return (True, fromBlock)

    def apply(self, state, action):
        blockHasMoved = 0
        if action == gameConstants.UP:
            new_state = (state[0] - 1, state[1])

        elif action == gameConstants.DOWN:
            new_state = (state[0] + 1, state[1])

        elif action == gameConstants.LEFT:
            new_state = (state[0], state[1] - 1)

        elif action == gameConstants.RIGHT:
            new_state = (state[0], state[1] + 1)
        state_content = self.states[new_state]
        if self.states[new_state] in [gameConstants.BOX, gameConstants.BOX_ON_GOAL]:
            if self.states[new_state] == gameConstants.BOX:
                blockHasMoved = 1
            else:
                blockHasMoved = 2
            self.moveBlock(action, new_state)
                
        if new_state in self.states:
            state = new_state
        return state, blockHasMoved, state_content

    def stateAfterMove(self, state, action):
        if action == gameConstants.UP:
            return (state[0] - 1, state[1])
        elif action == gameConstants.DOWN:
            return (state[0] + 1, state[1])
        elif action == gameConstants.LEFT:
            return (state[0], state[1] - 1)
        elif action == gameConstants.RIGHT:
            return (state[0], state[1] + 1)

    def lose(self):
        for i in range(self.height()):
            for j in range(self.width(i)):
                content = self.states[(i,j)]
                if content == gameConstants.BOX:
                    availableActions = self.availableActions((i,j), True)
                    if len(availableActions) >= 2:
                        if not ((gameConstants.UP in availableActions and gameConstants.DOWN in availableActions) or (gameConstants.LEFT in availableActions and gameConstants.RIGHT in availableActions)):
                            
                            return True
                    else:
                        return True
        return False

    def win(self):
        for i in range(self.height()):
            for j in range(self.width(i)):
                content = self.states[(i,j)]
                if content == gameConstants.BOX:
                    return False
                elif content == gameConstants.BOX_ON_GOAL:
                    return True
        return True

    def __repr__(self):
        res = ""
        for i in range(self.height()):
            for j in range(self.width(i)):
                res+= self.states[(i, j)]
            res+= '\n'
        return res

    def moveBlock(self, action, blockPos):
        if action == gameConstants.UP:
            self.states[(blockPos[0]-1, blockPos[1])] = gameConstants.BOX if self.states[(blockPos[0]-1, blockPos[1])] == gameConstants.FLOOR or self.states[(blockPos[0]-1, blockPos[1])] == gameConstants.PLAYER else gameConstants.BOX_ON_GOAL
        elif action == gameConstants.DOWN:
            self.states[(blockPos[0]+1, blockPos[1])] = gameConstants.BOX if self.states[(blockPos[0]+1, blockPos[1])] == gameConstants.FLOOR or self.states[(blockPos[0]+1, blockPos[1])] == gameConstants.PLAYER else gameConstants.BOX_ON_GOAL
        elif action == gameConstants.LEFT:
            self.states[(blockPos[0], blockPos[1]-1)] = gameConstants.BOX if self.states[(blockPos[0], blockPos[1]-1)] == gameConstants.FLOOR or self.states[(blockPos[0], blockPos[1]-1)] == gameConstants.PLAYER else gameConstants.BOX_ON_GOAL
        elif action == gameConstants.RIGHT:
            self.states[(blockPos[0], blockPos[1]+1)] = gameConstants.BOX if self.states[(blockPos[0], blockPos[1]+1)] == gameConstants.FLOOR or self.states[(blockPos[0], blockPos[1]+1)] == gameConstants.PLAYER else gameConstants.BOX_ON_GOAL
        if self.states[blockPos] == gameConstants.BOX_ON_GOAL:
            self.states[blockPos] = gameConstants.GOAL
        else:
            self.states[blockPos] = gameConstants.FLOOR
