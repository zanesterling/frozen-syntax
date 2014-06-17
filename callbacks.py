class Callbacks(object):
    def __init__(self, players=2, units=[]):
        self.units = [{} for p in xrange(players)]# list with a dict for each player
        for unit in units:
            self.add_unit(unit)

    def add_unit(self, unit):
        """ Insert a unit into the appropriate place, return assigned canonical id """
        player = unit.player
        # Insert a unit into it's playerlist 
        for unit_id in xrange(len(self.units[player])+1):
            if not unit_id in self.units[player]:
                self.units[player][unit_id] = unit
                return unit_id

    def get_units(self, player):
        """ Get all units belonging to a player.
        Returns dict of canonical id -> unit """
        return self.units[player]

    def callbacks(self):
        """ Returns dict of lisp function-name -> function.
        These functions takes a canonical id as the first argument,
        then specific arguments to the function """

        def move(player, unit_id, heading, speed):
            """ Callback to move the specified unit in the specified way """
            if unit_id in self.units[player]:
                self.units[player][unit_id].heading = heading
                self.units[player][unit_id].heading = speed
            else:
                raise ValueError("Unit with unit_id",unit_id,"does not exist")
        
        def aim(player, unit_id, angle):
            """ Callback to aim a unit's turret at the specified angle """
            pass

        def shoot(player, unit_id):
            """ Callback to make a unit shoot """
            pass

        def units_seen(player, unit_id):
            """ Callback to return a lisp list of all the units we can see """
            pass

        return {'move': move,
                'aim': aim,
                'shoot': shoot,
                'units-seen': units_seen}
