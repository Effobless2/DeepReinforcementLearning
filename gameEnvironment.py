import gameConstants


class Environment:
    def __init__(self, template):
        self.states = {}
        self.template = template.strip().split('\n')
        self.starting_point = (0,0)
        lines = template.strip().split('\n')
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] in [gameConstants.PLAYER, gameConstants.PLAYER_ON_GOAL]:
                    self.starting_point = (row, col)

    def availableActions(self, state):
        result = []
        if self.checkUpOK(state) :
            result.append(gameConstants.UP)
        if self.checkLeftOK(state) :
            result.append(gameConstants.LEFT)
        if self.checkDownOK(state) :
            result.append(gameConstants.DOWN)
        if self.checkRightOK(state) :
            result.append(gameConstants.RIGHT)
        return result
            


    def checkUpOK(self, state, fromBlock = False):
        new_state = (state[0] - 1, state[1])
        if new_state[0] < 0 :
            return False
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return False
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return False
            else :
                return self.checkUpOK(new_state, True)
        return True

    
    def checkDownOK(self, state, fromBlock = False):
        new_state = (state[0] + 1, state[1])
        if new_state[0] >= len(self.template) :
            return False
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return False
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return False
            else :
                return self.checkDownOK(new_state, True)
        return True

    def checkLeftOK(self, state, fromBlock = False):
        new_state = (state[0], state[1] - 1)
        if new_state[1] < 0 :
            return False
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return False
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return False
            else :
                return self.checkLeftOK(new_state, True)
        return True

    def checkRightOK(self, state, fromBlock = False):
        new_state = (state[0], state[1] + 1)
        if new_state[1] >= len(self.template[new_state[0]]) :
            return False
        new_state_content = self.states[new_state]
        if new_state_content == gameConstants.WALL :
            return False
        if new_state_content == gameConstants.BOX or new_state_content == gameConstants.BOX_ON_GOAL :
            if fromBlock :
                return False
            else :
                return self.checkRightOK(new_state, True)
        return True

    def apply(self, state, action):
        if action == gameConstants.UP:
            new_state = (state[0] - 1, state[1])
        elif action == gameConstants.DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == gameConstants.LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == gameConstants.RIGHT:
            new_state = (state[0], state[1] + 1)
        if new_state in self.states:
            state = new_state
        return state, self.states[state]