import actor
from math import pi, floor, copysign


turret_speed = 15

class Unit(actor.Actor):
    def __init__(self, world, player, x, y, radius):
        super(Unit, self).__init__(world, player, x, y)
        self.radius = radius
        self.dead = False
        self.unitID = len(world.units)
        world.units.append(self)
        world.history.actor_spawned(self)
        self._turret_angle = 0
        self.target_angle = 0

    def kill(self):
        """ Cause this unit to die, and generate an event to inform the client """
        if not self.dead:
            self.speed = 0
            self.dead = True
            self.world.history.actor_died(self)

    def shoot(self, delta_heading=0):
        #delta_heading kwarg is deprecated, leave it empty
        self.world.add_bullet(self.player, self.x, self.y, self.heading+delta_heading, 20)

    def update_turret_angle(self):
        """ Move the turret toward its intended orientation """
        def least_coterminal_angle(theta):
            return theta - 2*pi*floor(theta / (2*pi))
        delta_theta = least_coterminal_angle(self.target_angle - self._turret_angle)
        if abs(delta_theta) <= turret_speed:
            self._turret_angle = target_angle
        else:
            self._turret_angle = least_coterminal_angle(self._turret_angle + delta_theta)

    @property
    def typeID(self):
        return self.unitID

    @property
    def turret_angle(self):
        return self.turret_angle
