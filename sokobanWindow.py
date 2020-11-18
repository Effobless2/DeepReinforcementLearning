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
        self.initSprites()

    def reset(self):
        self.agent.environment.reset()
        self.agent.reset()
        self.update_player()  

    def initSprites(self):
        self.walls = arcade.SpriteList()
        self.goals = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        for state in self.agent.environment.states:
            if self.agent.environment.states[state] == gameConstants.WALL:
                self.walls.append(self.generateSprite(state, ":resources:images/tiles/grassCenter.png"))
            elif self.agent.environment.states[state] == gameConstants.BOX:
                self.boxes.append(self.generateSprite(state, ':resources:images/tiles/boxCrate_single.png'))
            elif self.agent.environment.states[state] == gameConstants.BOX_ON_GOAL:
                self.boxes.append(self.generateSprite(state, ':resources:images/items/coinBronze.png'))
            elif self.agent.environment.states[state] == gameConstants.GOAL:
                self.goals.append(self.generateSprite(state, ':resources:images/items/coinGold_lr.png'))
                
        self.update_player()

    def generateSprite(self, position, spriteUrl):
        sprite = arcade.Sprite(spriteUrl, 0.5)
        sprite.center_x = position[1] * sprite.width + sprite.width * 0.5
        sprite.center_y = self.height - (position[0] * sprite.width + sprite.width * 0.5)
        return sprite

    def update_player(self):
        self.player = self.generateSprite(self.agent.state, ":resources:images/enemies/frog.png")

    def on_draw(self):
        self.initSprites()
        arcade.start_render()
        self.walls.draw()
        self.goals.draw()
        self.boxes.draw()
        self.player.draw()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.C:
            self.reset()
        
    def on_update(self, delta_time):
        action = self.agent.best_action()
        if action != None :
            self.agent.do(action)
            self.update_player()

    
    def run(self):
        arcade.run()