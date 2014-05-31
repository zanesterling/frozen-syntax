class Actor(object):
    def __init__(self, x, y, world):
        self.world = world
        self._x = x
        self._y = y
        self._heading
        self._speed = 0
        self.max_speed = 10
        self.radius = 0
        self.dead = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x != self._x + self.vx:
            self._x = x
            self.world.history.actor_trajectory_update(world.time, self)
        else:
            self._x = x
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y != self._y + self.vy:
            self._y = y
            self.world.history.actor_trajectory_update(world.time, self)
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
            self.world.history.actor_trajectory_update(world.time, self)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        """ Set the speed, clamped to max_speed, and generate an event to inform the client of this change """
        if self._speed != min(speed, self.max_speed):
            self._speed = min(speed, self.max_speed)
            self.world.history.actor_trajectory_update(world.time, self)

    @property
    def vx(self):
        return self.speed * math.cos(self.heading)

    @property
    def vy(self):
        return self.speed * math.sin(self.heading)

    def is_colliding_with(self, other):
        """ True if this unit is colliding with other, False otherwise"""
        quadrance = (self.x-other.x)**2 + (self.y-other.y)**2
        colliding_quadrance = (self.radius + other.radius)**2
        return quadrance <= colliding_quadrance
