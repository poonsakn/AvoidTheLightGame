import arcade
import arcade.key
import CONSTANT

from models import World, Bat


class ModelSprite(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        # super().__init__(*args, SCALE)

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

        # arcade.set_background_color((60, 60, 60, 0))

        self.background_sprite = arcade.Sprite(CONSTANT.SRC['background'], CONSTANT.SCREEN_HEIGHT/1080)
        self.background_sprite.set_position(CONSTANT.SCREEN_WIDTH/2, CONSTANT.SCREEN_HEIGHT/2)
        self.world = World(width, height)
        self.init_sprite()
        self.firefly_sprites = []
        for firefly in self.world.fireflies:
            self.firefly_sprites.append(ModelSprite(
                CONSTANT.SRC['firefly'], model=firefly))
        
        self.touched_sprite = arcade.Sprite(CONSTANT.SRC['touched'], 4)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        # print(CONSTANT.FLYING_STATE)
        self.background_sprite.draw()
        if CONSTANT.FLYING_STATE != 0 and CONSTANT.BAT_ALIVE:
            self.bat_sprite2.draw()
        elif CONSTANT.BAT_ALIVE:
            self.bat_sprite.draw()

        for sprite in self.firefly_sprites:
            sprite.draw()

        if CONSTANT.COLLIDED:
            # self.touched_sprite.set_position(CONSTANT.SCREEN_WIDTH/2, CONSTANT.SCREEN_HEIGHT/2)
            self.touched_sprite.set_position(
                self.world.bat.x, self.world.bat.y)
            self.touched_sprite.draw()
            # print(CONSTANT.COLLIDED)
        
        # for firefly in self.world.fireflies:
        #     arcade.draw_text("x " + str(int(firefly.x)) + "y" + str(int(firefly.y)),
        #         firefly.x, firefly.y, arcade.color.WHITE, 10)
        
        # if CONSTANT.BAT_ALIVE:
        #     arcade.draw_text("x " + str(int(self.world.bat.x)) + "y" + str(int(self.world.bat.y)),
        #             self.world.bat.x, self.world.bat.y, arcade.color.WHITE, 10)
       
        # if CONSTANT.BAT_ALIVE:
        #     arcade.draw_text("x " + str(int(self.bat_sprite.center_x)) + "y" + str(int(self.bat_sprite.center_x)),
        #             self.bat_sprite.center_x, self.bat_sprite.center_y, arcade.color.WHITE, 10)
        if CONSTANT.BAT_ALIVE:
            arcade.draw_text("HP: " + str(self.world.bat.hit_points),
                            20, CONSTANT.SCREEN_HEIGHT - 40,
                            arcade.color.WHITE, 15)

    def animate(self, delta):        
        self.world.animate(delta)
        if CONSTANT.RESTART:
            self.init_sprite()

        if CONSTANT.BAT_ALIVE:
            # print("checking collision")
            self.bat_sprite.center_x = self.world.bat.x
            self.bat_sprite.center_y = self.world.bat.y
            self.world.check_collision(
                delta, self.bat_sprite, self.firefly_sprites)

        

    def init_sprite(self):
        if CONSTANT.BAT_ALIVE:
            
            self.bat_sprite = ModelSprite(
                CONSTANT.SRC['bat'], model=self.world.bat)

            # print("self world bat x")
            # print(self.world.bat.x)
            # print("self bat sprite x")
            # print(self.bat_sprite.center_x)
            
            self.bat_sprite2 = ModelSprite(
                CONSTANT.SRC['bat2'], model=self.world.bat)

if __name__ == '__main__':
    window = AvoidTheLightGameWindow(
        CONSTANT.SCREEN_WIDTH, CONSTANT.SCREEN_HEIGHT)

    arcade.run()
