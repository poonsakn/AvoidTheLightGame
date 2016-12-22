import arcade
import arcade.key
import CONSTANT
import math

from models import World, Bat

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()

class AvoidTheLightGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.gametitle_sprite = arcade.Sprite(CONSTANT.SRC['gametitle'], 1)
        self.gametitle_sprite.set_position(CONSTANT.SCREEN_WIDTH/2, CONSTANT.SCREEN_HEIGHT/2)
        self.background_sprite = arcade.Sprite(CONSTANT.SRC['background'], CONSTANT.SCREEN_HEIGHT/1080)
        self.background_sprite.set_position(CONSTANT.SCREEN_WIDTH/2, CONSTANT.SCREEN_HEIGHT/2)
        self.world = World()
        self.init_bat_sprite()
        self.refresh_firefly_sprite()        
        self.touched_sprite = arcade.Sprite(CONSTANT.SRC['touched'], 2.3)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        self.background_sprite.draw()
        if CONSTANT.FLYING_STATE != 0 and CONSTANT.BAT_ALIVE:
            self.bat_sprite2.draw()
        elif CONSTANT.BAT_ALIVE:
            self.bat_sprite.draw()

        if len(self.firefly_sprites) != 0:
            for sprite in self.firefly_sprites:
                sprite.draw()
        
        if CONSTANT.FRONT_PAGE:
            self.gametitle_sprite.draw()
            arcade.draw_text("press S to start",
                CONSTANT.SCREEN_WIDTH/2 - 60, 0.14*CONSTANT.SCREEN_HEIGHT,
                arcade.color.WHITE, 15)
            arcade.draw_text("Intruction: press Spacebar to fly!",
                15, 15,
                arcade.color.WHITE, 15)
        if not CONSTANT.BAT_ALIVE and not CONSTANT.FRONT_PAGE:
            arcade.draw_text("press R to try again",
                CONSTANT.SCREEN_WIDTH/2 - 95, 0.14*CONSTANT.SCREEN_HEIGHT,
                arcade.color.WHITE, 15)
            arcade.draw_text("Your score is " + str(math.ceil(CONSTANT.SCORE)),
                CONSTANT.SCREEN_WIDTH/2 - 95, 0.7*CONSTANT.SCREEN_HEIGHT,
                arcade.color.WHITE, 20)

        if CONSTANT.COLLIDED:
            self.touched_sprite.set_position(
                self.world.bat.x, self.world.bat.y)
            self.touched_sprite.draw()

        arcade.draw_text("High Score: " + str(math.ceil(CONSTANT.HIGH_SCORE)),
                20, CONSTANT.SCREEN_HEIGHT - 30,
                arcade.color.WHITE, 15)

        if CONSTANT.BAT_ALIVE:
            arcade.draw_text("Score: " + str(math.ceil(CONSTANT.SCORE)),
                            20, CONSTANT.SCREEN_HEIGHT - 50,
                            arcade.color.WHITE, 15)
            arcade.draw_text("HP: " + str(math.ceil(self.world.bat.hit_points/10)),
                            20, CONSTANT.SCREEN_HEIGHT - 70,
                            arcade.color.WHITE, 15)

    def animate(self, delta):        
        self.world.animate(delta)
        if CONSTANT.RESTART:
            self.init_bat_sprite()
        
        if CONSTANT.BAT_ALIVE:
            self.score(delta)
            self.bat_sprite.center_x = self.world.bat.x
            self.bat_sprite.center_y = self.world.bat.y
            self.world.check_collision(
                delta, self.bat_sprite, self.firefly_sprites)

        if CONSTANT.TIME_UNTIL_GET_HIT <= 0:
            self.world.add_firefly()
            self.refresh_firefly_sprite()
    def score(self, delta):
        CONSTANT.SCORE += delta*10

    def refresh_firefly_sprite(self):
        self.firefly_sprites = []
        for firefly in self.world.fireflies:
            self.firefly_sprites.append(ModelSprite(
                CONSTANT.SRC['firefly'], model=firefly))
    
    def init_bat_sprite(self):
        if CONSTANT.BAT_ALIVE:
            self.bat_sprite = ModelSprite(
                CONSTANT.SRC['bat'], model=self.world.bat)
            self.bat_sprite2 = ModelSprite(
                CONSTANT.SRC['bat2'], model=self.world.bat)

if __name__ == '__main__':
    window = AvoidTheLightGameWindow(
        CONSTANT.SCREEN_WIDTH, CONSTANT.SCREEN_HEIGHT)
    arcade.run()