import arcade
import gameConstants
import json

SPRITE_SIZE = 64

class MainWindow(arcade.Window):
    def __init__(self, height, width, agent):
        super().__init__(SPRITE_SIZE * width, 
                        SPRITE_SIZE * height,
                        "Pousse la caisse !")
        self.agent = agent
        self.reset()

    def setup(self):
        self.initSprites()

    def reset(self):
        self.started = False
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
        elif key == arcade.key.S:
            self.exportTable()

        
    def on_update(self, delta_time):
        if not self.started:
            self.started = True
            return
        player_can_play = self.agent.do()
        self.update_player()
        if self.agent.environment.win():
            input()
        if not player_can_play:
            self.reset()

    
    def run(self):
        arcade.run()

    def exportTable(self):
        x = {}
        x["learning_rate"] = self.agent.policy.learning_rate
        x["discount_factor"] = self.agent.policy.discount_factor
        x["table"] = {}
        for (i,j) in self.agent.policy.table.keys():
            x["table"]["("+str(i)+","+str(j)+")"] = self.agent.policy.table[(i,j)]

        json_object = json.dumps(x, indent = 4)
        print(json_object)
        f = open("novobanTable.json", "w")
        f.write(json_object)
        f.close()