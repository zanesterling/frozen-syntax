from world import World
from wall import Wall
from unit import Unit

def load_map(map_dict):
    """ Load a map of the dictionary representation map_dict, return the world with that map set up """
    world = World(map_dict['width'], map_dict['height'])
    for wall_dict in map_dict['walls']:
        world.add_wall(wall_dict['x'], wall_dict['y'], wall_dict['width'], wall_dict['height'])
    for unit_dict in map_dict['starting_positions']:
        world.add_unit(unit_dict['player'], unit_dict['x'], unit_dict['y'], unit_dict['radius'])
    return world
