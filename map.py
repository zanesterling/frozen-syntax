class Tile(object):
    """ A tile, which can hold some information about walls existing at its coordinate """
    def __init__(self, type, x=0, y=0):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.type) + ','
            + str(self.x) + ','
            + str(self.y) + ')'


class Map(object):
    """ A map, on which units frolic and walk into walls. """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize self.tiles to a 2D list of the right size
        self.tiles = [[Tile(0, x, y) for y in xrange(height)] for x in xrange(width)]
    
    def get_tile(self, x, y):
        """ Returns the tile at (x, y) in map-space (different from unit-space) """
        return self.tiles[x][y]
