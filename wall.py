class Wall(object):
    """ A wall. Blocks units, takes up space. """
    def __init__(self, world, x, y, width, height, wallID):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.world = world
        self.wallID = wallID

    def is_colliding_with(self, unit):
        """ Returns whether this wall and the unit are colliding """
        r = unit.radius
        tl = (self.x - r, self.y - r)
        br = (self.x + self.width + r, self.y + self.height + r)
        return tl[0] <= unit.x <= br[0] and tl[1] <= unit.y <= br[1]
