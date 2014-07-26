import actor
from math import pi, floor, copysign, atan2

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

    def can_see(self, x, y):
        target_angle = atan2(y - self.y, x - self.x)

        # check fov
        max_angle = self._heading + self._fov
        min_angle = self._heading - self._fov
        if max_angle > pi:
            max_angle -= pi * 2
            min_angle -= pi * 2
        if max_angle < target_angle or target_angle < min_angle:
            return False

        # check walls
        for wall in self.world.walls:
            points = wall.corners()
            point_angles = [atan2(py - self.y, px - self.x) for px,py in points]

            # cluster the angles if they are across the polar axis
            if max(point_angles) - min(point_angles) > pi:
                point_angles = [t if t > 0 else t + pi * 2
                                  for t in point_angles]

            # get min and max points, vals
            maxdex = 0
            mindex = 0
            for i in range(len(points)):
                if point_angles[i] > point_angles[maxdex]:
                    maxdex = i
                if point_angles[i] < point_angles[mindex]:
                    mindex = i
            maxa = point_angles[maxdex]
            mina = point_angles[mindex]

            # ensure target_angle is properly normalized (-pi,pi or 0,2pi)
            val = True
            if (maxa > target_angle and target_angle > mina):
                val = False
            if val:
                target_angle += pi * 2 # renormalize target_angle
                if (maxa > target_angle and target_angle > mina):
                    val = False

            # if point is radially occluded, check if it's closer than the wall
            if not val:
                t_maxpt = interp_points(points[maxdex], points[mindex],
                                        (target_angle - mina) / (maxa - mina))
                t_max_quad = (t_maxpt[0] - self.x) ** 2 + (t_maxpt[1] - self.y) ** 2
                t_quad = (x - self.x) ** 2 + (y - self.y) ** 2
                val = t_max_quad > t_quad
            if not val:
                return False
        return True

def interp_points(p1, p2, t):
    '''Return the linear interpolation of the two points at ratio t'''
    return [x2 + (x1 - x2) * t for x1,x2 in zip(p1, p2)]
