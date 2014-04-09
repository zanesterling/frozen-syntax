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

    def unStep():
        self.x -= self.speed * math.cos(self.theta)
        self.y -= self.speed * math.sin(self.theta)

    def getQuadrance(self.unit):
        return (self.x - unit.x)**2 + (self.y - unit.y)**2

    def getDistance(self, unit):
        return math.sqrt(self.get_quadrance(unit))

    def checkCollision(self, unit):
        return self.get_quadrance(unit) > (self.radius + other.radius)**2
