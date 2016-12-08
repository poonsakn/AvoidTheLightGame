import arcade.key
import random

FLYING_STATE = 0
FALLING_ACCELERATION = -15
FLYING_ACCELERATION = 20
FLYING_TIME = 0
FALLING_TIME = 0
BAT_FLYING_VELOCITY = 0
BAT_FALLING_VELOCITY = 0


class Bat():

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

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
        self.x = 0
        self.y = 0
    
    def random_location(self):
        self.x = random.randrange(450)
        self.y = random.randrange(600)

class World():
    NUM_FIREFLY = 10
    global FLYING_STATE
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width / 2), int(self.height / 2))
        self.fireflies = []
        for i in range(World.NUM_FIREFLY):
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
