import math

class Unit:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = 0

    def singleStep(self):
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)

    def unstep():
        self.x -= self.speed * math.cos(self.theta)
        self.y -= self.speed * math.sin(self.theta)
