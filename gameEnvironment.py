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