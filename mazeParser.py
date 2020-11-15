import gameConstants

class MazeParser:
    def __init__(self):
        pass

    def importFile(self, filename):
        file = open(filename, 'r')
        res = ''
        line = file.readline()
        while line:
            if (line == "" or line[0] not in gameConstants.COMPONENTS):
                break
            res += line
            line = file.readline()
        return res