import arcade
import arcade.key
from models import World, Bat

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCALE = 0.5

SRC = {"bat": "images/bat.png",
        "firefly": "images/firefly.png"}


class ModelSprite(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        # super().__init__(*args, SCALE)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class AvoidTheLightGameWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color((46, 53, 124, 0))

        self.world = World(width, height)
        self.bat_sprite = ModelSprite(SRC['bat'], model=self.world.bat)
        self.firefly_sprites = []
        n = 0
        for firefly in self.world.fireflies:
            print(n)
            n += 1
            self.firefly_sprites.append(ModelSprite(SRC['firefly'], model=firefly))
        
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        self.bat_sprite.draw()
        for sprite in self.firefly_sprites:
            sprite.draw()

    def animate(self, delta):
        self.world.animate(delta)
        self.check_collision(self.bat_sprite, self.firefly_sprites)
    
    def check_collision(self, bat_sprite, firefly_sprites):
        # collision_list = arcade.check_for_collision_with_list(bat_sprite, firefly_sprites)
        # print(collision_list)
        # print(len(collision_list))
        for sprite in firefly_sprites:
            is_collided = arcade.check_for_collision(bat_sprite, sprite)
            print(is_collided)
            n = 0
            print(n)
            n += 1
        n = 0

if __name__ == '__main__':
    window = AvoidTheLightGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
