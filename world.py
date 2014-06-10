from itertools import combinations, product
from numpy import matrix, vdot
import math
import json
import event
import unit
import wall
import bullet

class World(object):
    def __init__(self, width, height, turn_length = 250):
        self.actors = []
        self.units = []
        self.bullets = []
        self.walls = []
        self.history = event.History()
        self.timestamp = 0
        self.turn_length = turn_length


    def add_unit(self, player, x, y, radius):
        return unit.Unit(self, player, x, y, radius)

    def add_bullet(self, player, x, y, heading, speed):
        return bullet.Bullet(self, player, x, y, heading, speed)

    def add_wall(self, x, y, width, height):
        return wall.Wall(self, x, y, width, height)
        
    def step(self):
        """ Step all the units forward one timestep """
        self.timestamp += 1
        factor = 1 # Number of sub-steps we need for numerical integration
        #TODO: make this use the segment-quadrance function instead
        for unit in self.units:
            unit.update_turret_angle()
        for i in xrange(factor):
            for actor in self.actors:
                if not (actor.__class__.__name__ == 'Unit' and actor.dead):
                    actor.x += actor.vx / factor
                    actor.y += actor.vy / factor
            self.handle_collisions()
        if self.timestamp % self.turn_length == 0:
            self.history.turn_end(self)

    def handle_collisions(self):
        """ Check for collisions between each pair of unit, and if they exist, resolve them.
        Then, check for collisions between units and walls, and if they exist, resolve them. """
        # bullet -> unit collisions
        self.kill_shot_units()
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

    def kill_shot_units(self):
        for (u, b) in product(self.units, self.bullets):
            if u.player != b.player and self.actor_shot(u, b):
                u.kill()

    def callbacks(self):
        return {'move-unit': self.move_unit}
    
    def move_unit(self, unit_id, heading, speed):
        """ Callback to make a unit move from lisp code """
        if unit in self.units:
            unit.heading = heading
            unit.speed = speed
        return


    def actor_shot(self, actor, bullet):
        AB = matrix([[bullet.vx],
                     [bullet.vy]])
        AP = matrix([[actor.x - bullet.x],
                     [actor.y - bullet.y]])
        BP = AP - AB
        J = matrix([[0, -1],
                    [1, 0]])
        if vdot(AB, AP) >= vdot(AB, AB):
            return vdot(BP, BP) <= actor.radius**2
        if vdot(AB, AP) <= 0:
            return vdot(AP, AP) <= actor.radius**2
        return abs(vdot(J*AB, AP)) <= actor.radius**2 * vdot(AB, AB)
