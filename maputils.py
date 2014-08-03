import os
from world import World
from wall import Wall
from unit import Unit

def load_map(map_dict):
    """ Load a map of the dictionary representation map_dict, return the world with that map set up """
    world = World(map_dict['width'], map_dict['height'])
    for wall_dict in map_dict['walls']:
        world.add_wall(wall_dict['x'], wall_dict['y'], wall_dict['width'], wall_dict['height'])
    for unit_dict in map_dict['starting_positions']:
        unit = world.add_unit(unit_dict['player'], unit_dict['x'], unit_dict['y'], unit_dict['radius'])
        if 'vx' in unit_dict:
            unit.vx = unit_dict['vx']
        if 'vy' in unit_dict:
            unit.vy = unit_dict['vy']
    return world

def list_maps():
    """
    Returns a list of map filenames located in the maps/ directory.
    Maps have a filename ending with json.
    The returned filenames have .json stripped out.
    """
    return [x[:-5] for x in [x for x in os.walk('maps')][0][2] if x.endswith('.json')]
