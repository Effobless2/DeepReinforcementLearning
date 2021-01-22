import sys
import sokobanWindow
import mazeParser
import gameEnvironment
import gameAgent
import json

def main():
    if len(sys.argv) == 1:
        importedPolicy = None
    else:
        f = open(sys.argv[1], 'r')
        myJson = f.read()
        importedPolicy = json.loads(myJson)
        print(importedPolicy)
        toGive = {}
        toGive["learning_rate"] = importedPolicy["learning_rate"]
        toGive["discount_factor"] = importedPolicy["discount_factor"]
        toGive["table"] = {}
        for key in importedPolicy["table"].keys():
            keyTuple = key[1:-1]
            keyTuple = keyTuple.split(',')
            keyTuple = (int(keyTuple[0]), int(keyTuple[1]))
            toGive["table"][keyTuple] = {}
            for action in importedPolicy["table"][key].keys():
                toGive["table"][keyTuple][action] = {}
                toGive["table"][keyTuple][action][True] = float(importedPolicy["table"][key][action]['true'])
                toGive["table"][keyTuple][action][False] = float(importedPolicy["table"][key][action]['false'])
        importedPolicy = toGive
    parser = mazeParser.MazeParser()
    template = parser.importFile('tableaux/novoban01.xsb')
    width = len(max(template.strip().split('\n'), key=lambda x:len(x)))
    height = len(template.strip().split('\n'))
    environment = gameEnvironment.Environment(template)
    agent = gameAgent.Agent(environment, importedPolicy)

    window = sokobanWindow.MainWindow(height, width, agent)
    window.setup()
    window.run()


if __name__ == "__main__":
    main()