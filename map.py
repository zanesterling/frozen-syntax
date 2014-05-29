class Tile(object):
    """ A tile, which can hold some information about walls existing at its coordinate """
    def __init__(self, type, x=0, y=0):
        pass

class Map(object):
    """ A map, on which units frolic and walk into walls. """
    def __init__(self):
        pass
    
    def get_tile(self, x, y):
        """ Returns the tile at (x, y) in map-space (different from unit-space) """
        pass
