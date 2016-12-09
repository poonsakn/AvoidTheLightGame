import arcade.key
import random

FLYING_STATE = 0
FALLING_ACCELERATION = -15
FLYING_ACCELERATION = 20
FLYING_TIME = 0
FALLING_TIME = 0
BAT_FLYING_VELOCITY = 0
BAT_FALLING_VELOCITY = 0
NUM_FIREFLY = 20

class Bat():
    def __init__(self, world, x, y):
        global NUM_FIREFLY
        self.world = world
        self.x = x
        self.y = y
        self.hit_points = 10000+NUM_FIREFLY

    def animate(self, delta_time):
        global FLYING_STATE
        global FALLING_ACCELERATION
        global FALLING_TIME
        global FLYING_TIME
        global FALLING_TIME
        global BAT_FALLING_VELOCITY
        global BAT_FLYING_VELOCITY

        if FLYING_STATE == 0:
            if BAT_FLYING_VELOCITY <= 0:
                self.y += FALLING_ACCELERATION * FALLING_TIME * FALLING_TIME
                FLYING_TIME = 0
                FALLING_TIME += delta_time
            else:
                self.y += BAT_FLYING_VELOCITY * FLYING_TIME + \
                    FALLING_ACCELERATION * FLYING_TIME * FLYING_TIME
                FLYING_TIME -= delta_time
            # print("FLYING_STATE 0")

        elif FLYING_STATE != 0:
            if BAT_FALLING_VELOCITY >= 0:
                self.y += FLYING_ACCELERATION * FLYING_TIME * FLYING_TIME
                FALLING_TIME = 0
                FLYING_TIME += delta_time
            else:
                self.y -= BAT_FALLING_VELOCITY * FALLING_TIME + \
                    FLYING_ACCELERATION * FALLING_TIME * FALLING_TIME
                FALLING_TIME -= delta_time
            # print("FLYING_STATE not 0")

        # print(BAT_FALLING_VELOCITY)
        BAT_FLYING_VELOCITY = FLYING_ACCELERATION * FLYING_TIME
        BAT_FALLING_VELOCITY = FALLING_ACCELERATION * FALLING_TIME

        if self.y < 0:
            self.y = 0
            FALLING_TIME = 0
        elif self.y > self.world.height:
            self.y = self.world.height
            FLYING_TIME = 0

class Firefly():
    def __init__(self, world):
        self.world = world
        self.x = 800
        self.y = 800
    
    def random_location(self):
        self.x = random.randrange(450)
        self.y = random.randrange(600)

class World():
    global NUM_FIREFLY
    global FLYING_STATE
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width / 2), int(self.height / 2))
        self.fireflies = []
        for i in range(NUM_FIREFLY):
            self.firefly = Firefly(self)
            self.firefly.random_location()
            # print('{0} x: {1} y: {2}'.format(i, self.firefly.x, self.firefly.y))       
            self.fireflies.append(self.firefly)

    def on_key_press(self, key, key_modifiers):
        global FLYING_STATE
        if key == arcade.key.SPACE:
            FLYING_STATE += 1
            # print("press")
            # print(s)

    def on_key_release(self, key, key_modifiers):
        global FLYING_STATE
        if key == arcade.key.SPACE:
            FLYING_STATE = 0
        # print("release")
        # print(s)

    def animate(self, delta):
        self.bat.animate(delta)
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
        print(self.bat.hit_points)
        
    def hp_lost(self):
        self.bat.hit_points -= 1         
