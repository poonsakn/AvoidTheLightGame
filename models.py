import arcade.key

s = 0
falling_acceleration = -10
flying_acceleration = 20
t = 0
flying_time = 0


class Bat:
    
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.original_falling_speed = 3
        self.falling_speed = self.original_falling_speed
        self.original_flying_speed = 6
        self.flying_speed = self.original_flying_speed

    def animate(self, delta):
        global s
        global falling_acceleration
        global t
        global flying_time

        if s == 0:
            self.y += falling_acceleration * t * t

        elif s != 0:
            self.y += flying_acceleration * t * t
            self.falling_speed = self.original_falling_speed
            t = 0
        s = 0
        t += 0.03
        if self.y < 0:
            self.y = 0
            self.falling_speed = 0
            t = 0
        elif self.y > self.world.height:
            self.y = self.world.height
            self.falling_speed = 0
        print(t)


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width / 2), int(self.height / 2))

    def on_key_press(self, key, key_modifiers):
        global s
        if key == arcade.key.SPACE:
            s += 1

    def animate(self, delta):
        self.bat.animate(delta)