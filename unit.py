import math

class Unit:
    def __init__(self, x, y, theta, radius):
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = 0
        self.radius = radius

    def singleStep(self):
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)

    def unstep():
        self.x -= self.speed * math.cos(self.theta)
        self.y -= self.speed * math.sin(self.theta)

    def get_quadrance(self.unit):
        return (self.x - unit.x)**2 - (self.y - unit.y)**2

    def get_distance(self, unit):
        return math.sqrt(self.get_quadrance(unit))

    def check_collision(self, unit):
        return self.get_quadrance(unit) > (self.radius + other.radius)**2
