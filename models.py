import arcade.key
 
s = 0
a = -10
t = 0

class Bat:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.originalSpeed = 3;
        self.speed = self.originalSpeed
    # def fly(self):
    #     self.y += 5
    
    def animate(self, delta):
        global s
        global a
        global t

        if s == 0:
            self.y += a*t*t

        elif s != 0:
            self.y += 50
            self.speed = self.originalSpeed
            t = 0
        s = 0
        t += 0.03
        if self.y < 0:
                self.y = self.world.height
                self.speed = self.originalSpeed
            
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bat = Bat(self, int(self.width/2), int(self.height/2))

    def on_key_press(self, key, key_modifiers):
        global s
        if key == arcade.key.SPACE:
            s = 1
       
    def animate(self, delta):
        self.bat.animate(delta)
