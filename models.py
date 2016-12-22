import arcade.key
import random
import CONSTANT
import ORIGINAL_CONSTANT
import math

class Bat():

    def __init__(self, world):
        self.world = world
        CONSTANT.FLYING_STATE = ORIGINAL_CONSTANT.FLYING_STATE
        CONSTANT.FALLING_ACCELERATION = ORIGINAL_CONSTANT.FALLING_ACCELERATION
        CONSTANT.FLYING_ACCELERATION = ORIGINAL_CONSTANT.FLYING_ACCELERATION
        CONSTANT.FALLING_TIME = ORIGINAL_CONSTANT.FALLING_TIME
        CONSTANT.FLYING_TIME = ORIGINAL_CONSTANT.FLYING_TIME
        CONSTANT.BAT_FALLING_VELOCITY = ORIGINAL_CONSTANT.BAT_FALLING_VELOCITY
        CONSTANT.BAT_FLYING_VELOCITY = ORIGINAL_CONSTANT.BAT_FLYING_VELOCITY

        self.x = CONSTANT.SCREEN_WIDTH/2
        self.y = CONSTANT.SCREEN_HEIGHT/2

        self.i = 0
        self.angle = 0
        self.hit_points = 999999
        CONSTANT.BAT_ALIVE = True
    
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


        elif CONSTANT.FLYING_STATE != 0 and CONSTANT.BAT_ALIVE:

            if CONSTANT.BAT_FALLING_VELOCITY >= 0:
                self.y += CONSTANT.FLYING_ACCELERATION * \
                    CONSTANT.FLYING_TIME * CONSTANT.FLYING_TIME
                CONSTANT.FALLING_TIME = 0
                CONSTANT.FLYING_TIME += delta_time
            else:
                self.y -= CONSTANT.BAT_FALLING_VELOCITY * CONSTANT.FALLING_TIME + \
                    CONSTANT.FLYING_ACCELERATION * CONSTANT.FALLING_TIME * CONSTANT.FALLING_TIME
                CONSTANT.FALLING_TIME -= delta_time

        CONSTANT.BAT_FLYING_VELOCITY = CONSTANT.FLYING_ACCELERATION * CONSTANT.FLYING_TIME
        CONSTANT.BAT_FALLING_VELOCITY = CONSTANT.FALLING_ACCELERATION * CONSTANT.FALLING_TIME

        if self.y < 25 and CONSTANT.BAT_ALIVE:
            self.y = 25
            CONSTANT.FALLING_TIME = 0
        elif self.y < -100 and not CONSTANT.BAT_ALIVE:
            self.y = -100
            CONSTANT.FALLING_TIME = 0
        elif self.y > CONSTANT.SCREEN_HEIGHT-25:
            self.y = CONSTANT.SCREEN_HEIGHT-25
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

        if self.x > CONSTANT.SCREEN_WIDTH:
            self.x = 0
        
        elif self.x < 0:
            self.x = CONSTANT.SCREEN_WIDTH
        
        elif self.y > CONSTANT.SCREEN_HEIGHT:
            self.y = 0
        
        elif self.y < 0:
            self.y = CONSTANT.SCREEN_HEIGHT
        
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
    def __init__(self):
        self.create_fireflies()

    def create_fireflies(self):
        self.fireflies = []
        for i in range(CONSTANT.NUM_FIREFLY):
            self.add_firefly()

    def add_firefly(self):
        self.firefly = Firefly(self)
        self.firefly.random_location()
        self.fireflies.append(self.firefly)
        CONSTANT.TIME_UNTIL_GET_HIT = 3



    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and CONSTANT.BAT_ALIVE:
            CONSTANT.FLYING_STATE = 1

        if (key == arcade.key.S or key == arcade.key.R) and not CONSTANT.BAT_ALIVE:
            if CONSTANT.RESTART:
                for j in range(0,len(self.fireflies)):
                    self.fireflies.pop()
            self.bat = Bat(self)
            CONSTANT.RESTART = True
            CONSTANT.FRONT_PAGE = False
            self.bat.hit_points = 200
            if CONSTANT.SCORE > CONSTANT.HIGH_SCORE:
                CONSTANT.HIGH_SCORE = CONSTANT.SCORE
            CONSTANT.SCORE = 0

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            CONSTANT.FLYING_STATE = 0

    def animate(self, delta):
        if CONSTANT.BAT_ALIVE:
            self.bat.animate(delta)
        
        for firefly in self.fireflies:
            firefly.animate(delta)

    def check_collision(self, delta, bat_sprite, firefly_sprites):
        self.final_collided = 0
        for sprite in firefly_sprites:
            is_collided = arcade.check_for_collision(bat_sprite, sprite)
            if is_collided:
                self.final_collided += 1
            
        if self.final_collided > 0:
            self.hp_lost()
            CONSTANT.COLLIDED = True
        else:
            CONSTANT.COLLIDED = False
            CONSTANT.TIME_UNTIL_GET_HIT -= delta
        self.final_collided = 0

        if self.bat.hit_points <= 0:
            CONSTANT.BAT_ALIVE = False
       

    def hp_lost(self):
        if self.bat.hit_points > 0:
            self.bat.hit_points -= 1
