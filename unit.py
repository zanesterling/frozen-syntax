import math

degree = 180 / math.pi

class Unit:
    def __init__(self, x, y, heading, radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.color = 'green'
        self.heading = 0
        self.destination = (self.x, self.y)
        self.target = None

    def single_step(self):
        self.x += self.speed * math.cos(self.heading)
        self.y += self.speed * math.sin(self.heading)

    def un_step():
        self.x -= self.speed * math.cos(self.heading)
        self.y -= self.speed * math.sin(self.heading)

    def get_quadrance(self.unit):
        return (self.x - unit.x)**2 + (self.y - unit.y)**2

    def get_distance(self, unit):
        return math.sqrt(self.get_quadrance(unit))

    def check_collision(self, unit):
        return self.get_quadrance(unit) > (self.radius + other.radius)**2
