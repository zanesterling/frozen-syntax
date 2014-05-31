from itertools import combinations
import math
import json
import event
import unit
import wall





class World(object):
    def __init__(self, width, height):
        self.units = {} # Mapping of id -> unit
        self.walls = {} # Mapping of id -> wall
        self.history = event.History()
        self.timestamp = 0

    def add_unit(self, player, x, y, radius):
        """ Add a unit to the list of units, giving it an id as appropriate.
        Inform the unit of this world, it's id, and generate an event to inform the client
        Returns the assigned id """
        # Find an untaken id, assign it to the unit
        for i in xrange(len(self.units)+1):
            if not i in self.units:
                self.units[i] = unit.Unit(self, player, x, y, radius, i)
                self.history.actor_spawned(self.units[i])
                return self.units[i]

    def add_wall(self, x, y, width, height):
        """ Add a wall to the list of walls, giving it an appropriate id.
        Inform the client of this new wall
        Return assigned id"""
        for i in xrange(len(self.walls)+1):
            if not i in self.walls:
                self.walls[i] = wall.Wall(self, x, y, width, height, i)
                self.history.wall_added(wall)
                return wall

    def step(self):
        """ Step all the units forward one timestep """
        self.timestamp += 1
        factor = 1 # Number of sub-steps we need for numerical integration
        for i in xrange(factor):
            for unitID in self.units:
                unit = self.units[unitID]
                if not unit.dead:
                    unit.x += unit.vx / factor
                    unit.y += unit.vy / factor
            self.handle_collisions()
        return

    def handle_collisions(self):
        """ Check for collisions between each pair of unit, and if they exist, resolve them.
        Then, check for collisions between units and walls, and if they exist, resolve them. """
        for (first,second) in combinations(self.units, 2):
            unit1 = self.units[first]
            unit2 = self.units[second]
            if unit1.is_colliding_with(unit2):
                self.resolve_unit_collision(unit1, unit2)
        # unit -> wall collisions
        for unitid in self.units:
            unit = self.units[unitid]
            for wallid in self.walls:
                wall = self.walls[wallid]
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
        if unit_id in self.units:
            self.units[unit_id].heading = heading
            self.units[unit_id].speed = speed
        return
