import actor



class Unit(actor.Actor):
    def __init__(self, world, player, x, y, radius, actorID):
        super(Unit, self).__init__(world, player, x, y, actorID)
        self.radius = radius
        self.dead = False
        self.actor_type = 'Unit'

    def kill(self):
        """ Cause this unit to die, and generate an event to inform the client """
        if not self.dead:
            self.speed = 0
            self.dead = True
            self.world.history.actor_died(self)
