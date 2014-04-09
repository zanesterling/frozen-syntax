import unit

class World:
    def __init__(self, playerCount):
        self.players = range(playerCount) #This will be replaced by an enum.
        self.units = {player : {} for player in players}

    def addUnit(self, unit, unitID, player):
        if unitID in self.units[player]:
            print "UnitID already taken"
        else:
            self.units[player] = unit

    def runStep():
        for player in self.players:
            for unitID in self.units[player]:
                self.units[player][unitID].singleStep()
