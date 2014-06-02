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
        
