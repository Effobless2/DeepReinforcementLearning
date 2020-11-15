import gameConstants


class Environment:
    def __init__(self, template):
        self.states = {}
        self.starting_point = (0,0)
        lines = template.strip().split('\n')
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] in [gameConstants.PLAYER, gameConstants.PLAYER_ON_GOAL]:
                    self.starting_point = (row, col)

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
            #Reward
            state = new_state
        return state, self.states[state]