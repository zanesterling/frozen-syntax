from itertools import combinations
import math
import json
import random

class Unit(object):
    def __init__(self, x, y, player, radius, team):
        self.player = player
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.team = team
        self.dead = False

    def is_colliding_with(self, other):
        quadrance = (self.x-other.x)**2 + (self.y-other.y)**2
        colliding_quadrance = (self.radius + other.radius) ** 2
        return quadrance <= colliding_quadrance

class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.units = {} # Mapping of id -> unit
        self.events = []
        self.timestamp = 0

    def add_unit(self, unit):
        """ Add a unit to the list of units, giving it an id as appropriate. Returns the assigned id """
        # Find an untaken id, assign it to the unit
        for i in xrange(len(self.units)+1):
            if not i in self.units:
                self.units[i] = unit
                self.add_event("ActorSpawned", { 'id': i,
                    'x': unit.x,
                    'y': unit.y,
                    'team': unit.player,
                    })
                return i

    def step(self):
        self.timestamp += 1
        for id in self.units:
            unit = self.units[id]
            if not unit.dead:
                unit.x += unit.vx
                unit.y += unit.vy
        self.handle_collisions()
        return

    def handle_collisions(self):
        """ Check for collisions between each pair of unit, and if they exist, resolve them """
        for (first,second) in combinations(self.units, 2):
            unit1 = self.units[first]
            unit2 = self.units[second]
            if unit1.is_colliding_with(unit2):
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
                self.add_event("ActorPositionUpdate", {'id': first,
                    'x': unit1.x,
                    'y': unit1.y})
                self.add_event("ActorPositionUpdate", {'id': second,
                    'x': unit2.x,
                    'y': unit2.y})
                # add random chance for opposing colliders to explode
                if unit1.team != unit2.team:
                    if random.random() < 0.01:
                        unit1.dead = True;
                        self.add_event("ActorDied", {'id': first})
                    if random.random() < 0.01:
                        unit2.dead = True;
                        self.add_event("ActorDied", {'id': second})
    
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
    
    def move_unit(self, unit_id, vx, vy):
        """ Callback to make a unit move from lisp code """
        if unit_id in self.units:
            self.units[unit_id].vx = vx
            self.units[unit_id].vy = vy
            self.add_event('ActorVelocityChange', {'id': unit_id,
                'x': self.units[unit_id].x,
                'y': self.units[unit_id].y,
                'vx': self.units[unit_id].vx,
                'vy': self.units[unit_id].vy})
        return
