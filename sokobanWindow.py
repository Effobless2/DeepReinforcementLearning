import arcade

SPRITE_SIZE = 64

class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SPRITE_SIZE * 10, 
                        SPRITE_SIZE * 10,
                        "Pousse la caisse !")
    def setup(self):
        pass
    
    def run(self):
        arcade.run()