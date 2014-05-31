from itertools import combinations
import math
import json
import event
import unit
import wall

class World(object):
    def __init__(self, width, height):
        self.units = []
        self.walls = []
        self.history = event.History()
        self.timestamp = 0

    def add_unit(self, player, x, y, radius):
        """ Add a unit to the list of units, giving it an id as appropriate.
        Inform the unit of this world, it's id, and generate an event to inform the client
        Returns the assigned new unit """
        id = len(self.units)
        self.units.append(unit.Unit(self, player, x, y, radius, id))
        self.history.actor_spawned(self.units[id])
        return self.units[id]

    def add_wall(self, x, y, width, height):
        """ Add a wall to the list of walls, giving it an appropriate id.
        Inform the client of this new wall
        Return assigned id"""
        id = len(self.walls)
        self.walls.append(wall.Wall(self, x, y, width, height, id))
        self.history.wall_added(self.walls[id])
        return self.walls[id]

    def step(self):
        """ Step all the units forward one timestep """
        self.timestamp += 1
        factor = 1 # Number of sub-steps we need for numerical integration
        for i in xrange(factor):
            for unit in self.units:
                if not unit.dead:
                    unit.x += unit.vx / factor
                    unit.y += unit.vy / factor
            self.handle_collisions()
        return

    def handle_collisions(self):
        """ Check for collisions between each pair of unit, and if they exist, resolve them.
        Then, check for collisions between units and walls, and if they exist, resolve them. """
        for (unit1,unit2) in combinations(self.units, 2):
            if unit1.is_colliding_with(unit2):
                self.resolve_unit_collision(unit1, unit2)
        # unit -> wall collisions
        for unit in self.units:
            for wall in self.walls:
                if wall.is_colliding_with(unit):
                    self.resolve_wall_collision(wall, unit)

    def resolve_unit_collision(self, unit1, unit2):
        """ Resolve collisions between unit1 and unit2 """
        # As long as these two units are colliding, move them apart by their angle
        while unit1.is_colliding_with(unit2):
            angle = math.atan2(unit1.y-unit2.y, unit1.x-unit2.x)
            dx = math.cos(angle)
            dy = math.sin(angle)
            unit1.x += dx
            unit1.y += dy
            unit2.x -= dx
            unit2.y -= dy
        # Then remember to add an event for each unit so the client knows what happened

    def resolve_wall_collision(self, wall, unit):
        while wall.is_colliding_with(unit):
            moved = False
            if unit.x <= wall.x + wall.width/4:
                unit.x -= abs(unit.vx)
                moved = True
            if unit.y <= wall.y + wall.height/4:
                unit.y -= abs(unit.vy)
                moved = True
            if unit.x >= wall.x + wall.width * 3/4:
                unit.x += abs(unit.vx)
                moved = True
            if unit.y >= wall.y + wall.height * 3/4:
                unit.y += abs(unit.vy)
                moved = True
            # If we failed to move them, they're in some weird limbo from which none can be saved
            if not moved:
                break

    def callbacks(self):
        return {'move-unit': self.move_unit}
    
    def move_unit(self, unit_id, heading, speed):
        """ Callback to make a unit move from lisp code """
        if unit in self.units:
            unit.heading = heading
            unit.speed = speed
        return
