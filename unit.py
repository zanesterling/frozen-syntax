import math

class Unit:
    def __init__(self, x, y, heading, radius, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.color = 'green'
        self.heading = 0
        self.destination = (self.x, self.y)
        self.target = None
        self.hit_wall = False

    def singleStep(self):
        self.x += self.speed * math.cos(self.heading)
        self.y += self.speed * math.sin(self.heading)

    def unStep():
        self.x -= self.speed * math.cos(self.heading)
        self.y -= self.speed * math.sin(self.heading)

    def getQuadrance(self, unit):
        return (self.x - unit.x)**2 + (self.y - unit.y)**2

    def getDistance(self, unit):
        return math.sqrt(self.getQuadrance(unit))

    def checkCollision(self, unit):
        return self.getQuadrance(unit) > (self.radius + other.radius)**2
