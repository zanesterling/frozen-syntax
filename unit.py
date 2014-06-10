import actor



class Unit(actor.Actor):
    def __init__(self, world, player, x, y, radius):
        super(Unit, self).__init__(world, player, x, y)
        self.radius = radius
        self.dead = False
        self.unitID = len(world.units)
        world.units.append(self)
        world.history.actor_spawned(self)

    def kill(self):
        """ Cause this unit to die, and generate an event to inform the client """
        if not self.dead:
            self.speed = 0
            self.dead = True
            self.world.history.actor_died(self)

    def shoot(self, delta_heading):
        self.world.add_bullet(self.player, self.x, self.y, self.heading+delta_heading, 20)

    @property
    def typeID(self):
        return self.unitID

    def can_see(self, x, y):
        theta = math.atan2(x - self.x, y - self.y)

        # check fov
        max_angle = self._heading + self._fov
        min_angle = self._heading - self._fov
        if max_angle > math.pi:
            max_angle -= math.pi * 2
            min_angle -= math.pi * 2
        if max_angle < theta or theta > min_angle:
            return False

        # check walls
        for wall in self.world.walls:
            point_angles = [atan2(x, y) for x,y in wall.corners()]

            # cluster the angles if they are across the polar axis
            if max(point_angles) - min(point_angles) > math.pi:
                point_angles = [t if t > 0 else t + math.pi * 2
                                  for t in point_angles]

            maxa = max(point_angles)
            mina = min(point_angles)
            # TODO add distance logic
            if (maxa > theta and theta > mina):
                return False
            theta += math.pi * 2
            if (maxa > theta and theta > mina):
                return False

        return True
