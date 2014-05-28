from itertools import combinations
import math
import json
import random

class Unit(object):
    def __init__(self, x, y, player, radius, team):
        self.player = player
        self.id = -1 # we don't know our id until the world tells us
        self.world = None # When we're added to the world, it'll inform us
        self.x = x
        self.y = y
        self._heading = 0
        self._speed = 0
        self.max_speed = 10
        self.radius = radius
        self.team = team
        self.dead = False

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
        self.dead = True
        self.world.add_event('ActorDied', {'id': self.id})


class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.units = {} # Mapping of id -> unit
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
        factor = 2
        for i in xrange(factor):
            for id in self.units:
                unit = self.units[id]
                if not unit.dead:
                    unit.x += unit.vx / factor
                    unit.y += unit.vy / factor
            self.handle_collisions()
        return

    def handle_collisions(self):
        """ Check for collisions between each pair of unit, and if they exist, resolve them """
        for (first,second) in combinations(self.units, 2):
            unit1 = self.units[first]
            unit2 = self.units[second]
            if unit1.is_colliding_with(unit2):
                self.resolve_collision(unit1, unit2)
                # add random chance for opposing colliders to explode
                if unit1.team != unit2.team:
                    if random.random() < 0.01:
                        unit1.kill()
                    if random.random() < 0.01:
                        unit2.kill()

    def resolve_collision(self, unit1, unit2):
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
