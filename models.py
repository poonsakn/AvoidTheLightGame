import arcade.key

state = 0
falling_acceleration = -25
flying_acceleration = 30

flying_time = 0
falling_time = 0
bat_flying_velocity = 0
bat_falling_velocity = 0


class Bat:

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def animate(self, delta_time):
        global state
        global falling_acceleration
        global falling_time
        global flying_time
        global falling_time
        global bat_falling_velocity
        global bat_flying_velocity

        if state == 0:
            if bat_flying_velocity <= 0:
                self.y += falling_acceleration * falling_time * falling_time
                flying_time = 0
                falling_time += delta_time
            else:
                self.y += bat_flying_velocity * flying_time + \
                    falling_acceleration * flying_time * flying_time
                flying_time -= delta_time
            print("state 0")

        elif state != 0:
            if bat_falling_velocity >= 0:
                self.y += flying_acceleration * flying_time * flying_time
                falling_time = 0
                flying_time += delta_time
            else:
                self.y -= bat_falling_velocity * falling_time + \
                    flying_acceleration * falling_time * falling_time
                falling_time -= delta_time
            print("state not 0")
        
        print(bat_falling_velocity)
        bat_flying_velocity = flying_acceleration * flying_time
        bat_falling_velocity = falling_acceleration * falling_time

        if self.y < 0:
            self.y = 0
            falling_time = 0
        elif self.y > self.world.height:
            self.y = self.world.height
            flying_time = 0


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
