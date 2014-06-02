import actor





default_bullet_speed = 100

class Bullet(actor.Actor):
    def __init__(self, world, player, x, y, heading, speed):
        super(Bullet, self).__init__(world, player, x, y)
        self.heading = heading
        self.speed = speed
        self.bulletID = len(self.world.bullets)
        self.world.history.actor_spawned(self)
