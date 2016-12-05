import arcade
import arcade.key
from models import World, Bat

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCALE = 0.5

SRC = {"bat" : "images/bat.png"}
 
class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
     
        # super().__init__(*args, **kwargs)
        super().__init__(*args, SCALE)

        

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class AvoidTheLightGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.WHITE)
 
        self.world = World(width, height)
        self.bat_sprite = ModelSprite(SRC['bat'], model=self.world.bat)
        # print(type(self.bat_sprite))
    
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        self.bat_sprite.draw()
 
    def animate(self, delta):
        self.world.animate(delta)

if __name__ == '__main__':
    window = AvoidTheLightGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()