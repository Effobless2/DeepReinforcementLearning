import sokobanWindow
import mazeParser
import gameEnvironment
import gameAgent

def main():
    parser = mazeParser.MazeParser()
    template = parser.importFile('tableaux/novoban01.xsb')
    width = len(max(template.strip().split('\n'), key=lambda x:len(x)))
    height = len(template.strip().split('\n'))
    environment = gameEnvironment.Environment(template)
    agent = gameAgent.Agent(environment)

    window = sokobanWindow.MainWindow(height, width, agent)
    window.setup()
    window.run()


if __name__ == "__main__":
    main()