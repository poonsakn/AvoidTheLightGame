import arcade.key

state = 0
falling_acceleration = -15
flying_acceleration = 20
t = 0
flying_time = 0
bat_velocity = 0


class Bat:
    
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def animate(self, delta_time):
        global state
        global falling_acceleration
        global t
        global flying_time
        global bat_velocity

        if state == 0:
            if bat_velocity <= 0:
                self.y += falling_acceleration * t * t
                flying_time = 0
                t += delta_time
            else:
                self.y += bat_velocity * flying_time + falling_acceleration * flying_time * flying_time
                flying_time -= delta_time
            print("state 0")

        elif state != 0:
            self.y += flying_acceleration * flying_time * flying_time
            print("state not 0")
            t = 0
            flying_time += delta_time        

        bat_velocity = flying_acceleration*flying_time
        print(bat_velocity)

        if self.y < 0:
            self.y = 0

            t = 0
        elif self.y > self.world.height:
            self.y = self.world.height

class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width / 2), int(self.height / 2))

    def on_key_press(self, key, key_modifiers):
        global state
        if key == arcade.key.SPACE:
            state += 1
            print("press")
            # print(s)

    def on_key_release(self, key, key_modifiers):
        global state
        if key == arcade.key.SPACE:
            state = 0
        print("release")
        # print(s)

    def animate(self, delta):
        self.bat.animate(delta)