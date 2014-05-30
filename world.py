from itertools import combinations
import math
import json
import map

class Unit(object):
    def __init__(self, x, y, player, radius, team):
        self.player = player
        self.id = -1 # we don't know our id until the world tells us
        self.world = None # When we're added to the world, it'll inform us
        self._x = x
        self._y = y
        self._heading = 0
        self._speed = 0
        self.max_speed = 10
        self.radius = radius
        self.team = team
        self.dead = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x != self._x + self.vx:
            self._x = x
            self.world.add_event('ActorPositionUpdate', {'id':self.id,
                'x': self.x, 'y': self.y})
        else:
            self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y != self._y + self.vy:
            self._y = y
            self.world.add_event('ActorPositionUpdate', {'id':self.id,
                'x': self.x, 'y': self.y})
        else:
            self._y = y

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, heading):
        """ Set the heading, and generate an event to inform the client of this change """
        if self._heading != heading:
            self._heading = heading
            self.world.add_event('ActorVelocityChange', {'id':self.id,
                'x': self.x, 'y': self.y, 'vx': self.vx, 'vy': self.vy})

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        """ Set the speed, clamped to max_speed, and generate an event to inform the client of this change """
        if self._speed != speed:
            self._speed = min(speed, self.max_speed)
            self.world.add_event('ActorVelocityChange', {'id':self.id,
                'x': self.x, 'y': self.y, 'vx': self.vx, 'vy': self.vy})

    @property
    def vx(self):
        return self.speed * math.cos(self.heading)

    @property
    def vy(self):
        return self.speed * math.sin(self.heading)

    def is_colliding_with(self, other):
        """ True if this unit is colliding with other, False otherwise"""
        quadrance = (self.x-other.x)**2 + (self.y-other.y)**2
        colliding_quadrance = (self.radius + other.radius) ** 2
        return quadrance <= colliding_quadrance

    def kill(self):
        """ Cause this unit to die, and generate an event to inform the client """
        if not self.dead:
            self.dead = True
            self.world.add_event('ActorDied', {'id': self.id})


class Wall(object):
    """ A wall. Blocks units, takes up space. """
    def __init__(self, x=0, y=0, width=10, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_colliding_with(self, unit):
        """ Returns whether this wall and the unit are colliding """
        r = unit.radius
        tl = (self.x - r, self.y - r)
        br = (self.x + self.width + r, self.y + self.height + r)
        return tl[0] <= unit.x <= br[0] and tl[1] <= unit.y <= br[1]


class World(object):
    def __init__(self, width, height):
        self.units = {} # Mapping of id -> unit
        self.walls = []
        self.events = []
        self.timestamp = 0

    def add_unit(self, unit):
        """ Add a unit to the list of units, giving it an id as appropriate.
        Inform the unit of this world, it's id, and generate an event to inform the client
        Returns the assigned id """
        # Find an untaken id, assign it to the unit
        for i in xrange(len(self.units)+1):
            if not i in self.units:
                self.units[i] = unit
                unit.id = i
                unit.world = self
                self.add_event("ActorSpawned", { 'id': i,
                    'x': unit.x,
                    'y': unit.y,
                    'team': unit.player,
                    })
                return i

    def step(self):
        """ Step all the units forward one timestep """
        self.timestamp += 1
        factor = 1 # Number of sub-steps we need for numerical integration
        for i in xrange(factor):
            for id in self.units:
                unit = self.units[id]
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
            for wall in self.walls:
                if wall.is_colliding_with(unit):
                    print "collision at: ",unit.x, unit.y
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
        self.add_event("ActorPositionUpdate", {'id': unit1.id,
            'x': unit1.x,
            'y': unit1.y})
        self.add_event("ActorPositionUpdate", {'id': unit2.id,
            'x': unit2.x,
            'y': unit2.y})

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

    def add_event(self, type, data):
        event = {
                "timestamp": self.timestamp,
                "type": type,
                "data": data
            }
        self.events.append(event)

    def serialized_events(self):
        return json.dumps(self.events)

    def callbacks(self):
        return {'move-unit': self.move_unit}
    
    def move_unit(self, unit_id, heading, speed):
        """ Callback to make a unit move from lisp code """
        if unit_id in self.units:
            self.units[unit_id].heading = heading
            self.units[unit_id].speed = speed
        return
