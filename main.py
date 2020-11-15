import sokobanWindow
import mazeParser

def main():
    parser = mazeParser.MazeParser()
    template = parser.importFile('tableaux/novoban01.xsb')
    window = sokobanWindow.MainWindow()
    window.setup()
    window.run()


if __name__ == "__main__":
    main()