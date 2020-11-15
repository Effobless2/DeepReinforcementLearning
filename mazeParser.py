WALL, PLAYER, PLAYER_ON_GOAL, BOX, BOX_ON_GOAL, GOAL, FLOOR = '#', '@', '+', '$', '*', '.', ' '

class MazeParser:
    def __init__(self):
        pass

    def importFile(self, filename):
        file = open(filename, 'r')
        res = ''
        line = file.readline()
        while line:
            if (line == "" or line[0] not in [WALL, PLAYER, PLAYER_ON_GOAL, BOX, BOX_ON_GOAL, GOAL, FLOOR]):
                break
            res += line
            line = file.readline()
        return res