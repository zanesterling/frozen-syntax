import math
class Unit:
    def __init__(self, x, y, heading, radius, max_speed):
        self.x = x
        self.y = y
        self.max_speed = max_speed
        self.speed = 0.0
        self.radius = radius
        self.color = 'green'
        self.heading = heading #in radians
        self.destination = (self.x, self.y)
        self.target = None
        self.hit_wall = False

    def singleStep(self):
        #If they are far from their destination, go toward it
        if (self.x - self.destination[0])**2 + (self.y - self.destination[1])**2 > self.max_speed**2:
            self.x += self.speed * math.cos(self.heading)
            self.y += self.speed * math.sin(self.heading)
        else: #Otherwise, just put them there
            self.speed = math.sqrt((self.x - self.destination[0])**2 + (self.y - self.destination[1])**2)
            (self.x, self.y) = self.destination

    def unStep(self):
        self.x -= self.speed * math.cos(self.heading)
        self.y -= self.speed * math.sin(self.heading)

    def getQuadrance(self, unit):
        return (self.x - unit.x)**2 + (self.y - unit.y)**2

    def getDistance(self, unit):
        return math.sqrt(self.getQuadrance(unit))

    def checkCollision(self, unit):
        return self.getQuadrance(unit) < (self.radius + unit.radius)**2
