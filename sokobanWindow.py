import arcade
import gameConstants

SPRITE_SIZE = 64

class MainWindow(arcade.Window):
    def __init__(self, height, width, agent):
        super().__init__(SPRITE_SIZE * width, 
                        SPRITE_SIZE * height,
                        "Pousse la caisse !")
        self.agent = agent

    def setup(self):
        self.walls = arcade.SpriteList()
        self.goals = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        for state in self.agent.environment.states:
            if self.agent.environment.states[state] == gameConstants.WALL:
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = state[1] * sprite.width + sprite.width * 0.5
                sprite.center_y = self.height - (state[0] * sprite.width + sprite.width * 0.5)
                self.walls.append(sprite)
            elif self.agent.environment.states[state] == gameConstants.BOX:
                sprite = arcade.Sprite(':resources:images/tiles/boxCrate_single.png', 0.5)
                sprite.center_x = state[1] * sprite.width + sprite.width * 0.5
                sprite.center_y = self.height - (state[0] * sprite.width + sprite.width * 0.5)
                self.boxes.append(sprite)
            elif self.agent.environment.states[state] == gameConstants.GOAL:
                sprite = arcade.Sprite(':resources:images/items/coinGold_lr.png', 0.5)
                sprite.center_x = state[1] * sprite.width + sprite.width * 0.5
                sprite.center_y = self.height - (state[0] * sprite.width + sprite.width * 0.5)
                self.goals.append(sprite)
            
            self.player = arcade.Sprite(":resources:images/enemies/frog.png", 0.5)
        self.player.center_x = self.agent.state[1] * self.player.width + self.player.width * 0.5
        self.player.center_y = self.height - (self.agent.state[0] * self.player.width + self.player.height * 0.5)


    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.goals.draw()
        self.boxes.draw()
        self.player.draw()

    
    def run(self):
        arcade.run()