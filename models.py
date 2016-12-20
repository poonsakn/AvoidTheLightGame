import arcade.key
import random
import CONSTANT
import math

class Bat():

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
        self.hit_points = 10000 + CONSTANT.NUM_FIREFLY

    def animate(self, delta_time):
        if CONSTANT.FLYING_STATE == 0:
            if CONSTANT.BAT_FLYING_VELOCITY <= 0:
                self.y += CONSTANT.FALLING_ACCELERATION * \
                    CONSTANT.FALLING_TIME * CONSTANT.FALLING_TIME
                CONSTANT.FLYING_TIME = 0
                CONSTANT.FALLING_TIME += delta_time
            else:
                self.y += CONSTANT.BAT_FLYING_VELOCITY * CONSTANT.FLYING_TIME + \
                    CONSTANT.FALLING_ACCELERATION * CONSTANT.FLYING_TIME * CONSTANT.FLYING_TIME
                CONSTANT.FLYING_TIME -= delta_time
            # print("FLYING_STATE 0")

        elif CONSTANT.FLYING_STATE != 0:
            if CONSTANT.BAT_FALLING_VELOCITY >= 0:
                self.y += CONSTANT.FLYING_ACCELERATION * \
                    CONSTANT.FLYING_TIME * CONSTANT.FLYING_TIME
                CONSTANT.FALLING_TIME = 0
                CONSTANT.FLYING_TIME += delta_time
            else:
                self.y -= CONSTANT.BAT_FALLING_VELOCITY * CONSTANT.FALLING_TIME + \
                    CONSTANT.FLYING_ACCELERATION * CONSTANT.FALLING_TIME * CONSTANT.FALLING_TIME
                CONSTANT.FALLING_TIME -= delta_time
            # print("FLYING_STATE not 0")

        # print(CONSTANT.BAT_FALLING_VELOCITY)
        CONSTANT.BAT_FLYING_VELOCITY = CONSTANT.FLYING_ACCELERATION * CONSTANT.FLYING_TIME
        CONSTANT.BAT_FALLING_VELOCITY = CONSTANT.FALLING_ACCELERATION * CONSTANT.FALLING_TIME

        if self.y < 0:
            self.y = 0
            CONSTANT.FALLING_TIME = 0
        elif self.y > self.world.height:
            self.y = self.world.height
            CONSTANT.FLYING_TIME = 0


class Firefly():

    def __init__(self, world):
        self.world = world
        self.x = 800
        self.y = 800
        self.angle = random.randrange(360)
    
    def animate(self, delta_time):
        self.random_direction()
        self.move_forward()

    def move_forward(self):
        self.x += math.sin(-math.radians(self.angle))
        self.y += math.cos(-math.radians(self.angle))

    def random_direction(self):
        direction = bool(random.getrandbits(1))
        if direction:
            self.angle += 5
        else:
            self.angle -= 5

    def random_location(self):
        self.x = random.randrange(450)
        self.y = random.randrange(600)


class World():

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width / 2), int(self.height / 2))
        self.fireflies = []
        for i in range(CONSTANT.NUM_FIREFLY):
            self.firefly = Firefly(self)
            self.firefly.random_location()
            # self.firefly.random_direction()
            # print('{0} x: {1} y: {2}'.format(i, self.firefly.x, self.firefly.y))
            self.fireflies.append(self.firefly)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            CONSTANT.FLYING_STATE += 1
            # print("press")
            # print(s)

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            CONSTANT.FLYING_STATE = 0
        # print("release")
        # print(s)

    def animate(self, delta):
        self.bat.animate(delta)
        
        for firefly in self.fireflies:
            firefly.animate(delta)

        # self.firefly.animate(delta)

    def check_collision(self, bat_sprite, firefly_sprites):
        # collision_list = arcade.check_for_collision_with_list(bat_sprite, firefly_sprites)
        # print(collision_list)
        # print(len(collision_list))
        for sprite in firefly_sprites:
            is_collided = arcade.check_for_collision(bat_sprite, sprite)
            if is_collided:
                # print(self.bat.hit_points)
                self.hp_lost()
        # print(self.bat.hit_points)

    def hp_lost(self):
        self.bat.hit_points -= 1
