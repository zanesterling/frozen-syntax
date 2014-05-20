import unit
import Queue
import math
import json
import itertools

class World:
    def __init__(self, playerCount):
        self.units = {player : {} for player in range(playerCount)}
        self.walls = []
        self.map_bounds = (-1000, 1000, -1000, 1000)
        self.time = 0
        self.visibility = {player : {} for player in self.units}
        #self.visibility[player1][player2][unitID] is a boolean that tells me whether
        #player1 can see the unit with ID unitID, which belongs to player2
        self.events = []

    def addWall(self, x0, y0, width, height):
        self.walls.append((x0, x0+width, y0, y0+height)) #xmin, xmax, ymin, ymax

    def addWallCentered(self, x0, y0, width, height):
        self.walls.append((x0 - width/2, x0 + width/2, y0 - height/2, y0 + height/2))

    def pointInWall(self, x, y):
        for wall in self.walls:
            if wall[0] <= x <= wall[1] and wall[2] <= y <= wall[3]:
                return true
        return False

    def pointOnMap(self, x, y):
        return (self.map_bounds[0] < x < self.map_bounds[1]) \
            and (self.map_bounds[2] < y < self.map_bounds[3])

    def addUnit(self, unit, unitID, player):
        if unitID in self.units[player]:
            print "UnitID already taken"
        else:
            self.units[player][unitID] = unit
            self.createEvent(self.actorSpawnedEvent(unitID, \
                                          unit.x, \
                                          unit.y, \
                                          player, \
                                          'unit'))

    def runStep(self):
        #This is the id info for all of the units
        
        unit_data = [(player, unitID) for player in self.units for unitID in self.units[player]]

        
        units_that_moved = {}
        for data in unit_data:
            units_that_moved[data] = self.units[data[0]][data[1]].speed != 0
            self.units[data[0]][data[1]].singleStep()
        #Now all the units have been stepped, and we have a dictionary of booleans,
        #representing which ones have actually moved.
        #Next, check for collisions. First get all of the colliding pairs:
        colliding_unit_pairs = [pair for pair in itertools.combinations(unit_data, 2) if self.units[pair[0][0]][pair[0][1]].checkCollision(self.units[pair[1][0]][pair[1][1]])]
        #Then take all of the units in either element of a pair, or that are in walls.
        first_colliding_units = [pair[0] for pair in colliding_unit_pairs]
        second_colliding_units = [pair[1] for pair in colliding_unit_pairs]
        colliding_units = [data for data in unit_data if data in first_colliding_units or
                                                         data in second_colliding_units or
                                                         self.pointInWall(self.units[data[0]][data[1]].x, self.units[data[0]][data[1]].y)]
        #And unstep them, and write this down in units_that_moved
        for data in colliding_units:
            if units_that_moved[data]:
                self.safeUnStep(data[0], data[1])
                units_that_moved[data] = False
        while colliding_units != []:
            print units_that_moved
            colliding_units = [data for data in unit_data if
                               data in first_colliding_units or
                               data in second_colliding_units or
                               self.pointInWall(self.units[data[0]][data[1]].x, self.units[data[0]][data[1]].y)]
            for data in colliding_units:
                if units_that_moved[data]:
                    self.safeUnStep(data[0], data[1])
                    units_that_moved[data] = False
            colliding_unit_pairs = [pair for pair in itertools.combinations(unit_data, 2) if self.units[pair[0][0]][pair[0][1]].checkCollision(self.units[pair[1][0]][pair[1][1]])]
            first_colliding_units = [pair[0] for pair in colliding_unit_pairs]
            second_colliding_units = [pair[1] for pair in colliding_unit_pairs]
            colliding_units = [data for data in unit_data if data in first_colliding_units or
                                                         data in second_colliding_units or
                                                         self.pointInWall(self.units[data[0]][data[1]].x, self.units[data[0]][data[1]].y)]
        #TODO This algorithm relies on the assumption that after the previous step, there were no collisions.
        #need to ensure that no units can be created such that there are collisions.
        for player in self.units:
            for unitID in self.units[player]:
                print (self.units[player][unitID].x, self.units[player][unitID].y, unitID)

    def safeUnStep(self, player, unitID): #If a unit is unstepped, this needs to be used in order to make the client reflect it.
        self.units[player][unitID].unStep()
        self.createEvent(self.updateActorPositionEvent(unitID, self.units[player][unitID].x, self.units[player][unitID].y))


        

    def move(self, player, unitID, dx, dy):
        self.go(player, unitID, x + dx, y + dy)

    def go(self, player, unitID, x, y):
        unit = self.units[player][unitID]
        unit.speed = unit.max_speed
        unit.destination = (x, y)
        displacement = (x - unit.x, y - unit.y)
        distance = math.sqrt(displacement[0]**2 + displacement[1]**2)
        vx = unit.speed * displacement[0] / distance
        vy = unit.speed * displacement[1] / distance
        self.createEvent(self.actorStartedMovingEvent(unitID, unit.x, unit.y, vx, vy))

    def stop(self, player, unitID):
        unit = self.units[player][unitID]
        self.go(player, unitID, unit.x, unit.y)

    def say(self, unit, message):
        pass

    def createEvent(self, event): #this needs to send the event to the client
        self.events.append(event)

    def getEventsJson(self):
        return json.dumps(self.events)

    def updateVisibility(self, player1, player2): #player1 is looking for player2's units
        units_seen = {}
        for u2 in self.units[player2]:
            units_seen[u2] = False
            for u1 in self.units[player1]:
                if self.canSee(u1, u2):
                    units_seen[u2] = True
                    break
        vis_event_units = {unitID : units_seen[unitID] for unitID in units_seen
                           if units_seen[unitID] != self.visibility[player1][player2][unitID]}
        for unitID in vis_event_units:
            if vis_event_units[unitID]:
                self.createEvent(actorSeenEvent(unitID,
                                           self.units[player2].x,
                                           self.units[player2].y,
                                           player2,
                                           'unit'))
            else:
                createEvent(actorHiddenEvent(unitID))
        self.visibility[player1][player2] = units_seen

    def canSee(self, unit1, unit2): #Returns whether unit1 can see unit2
        return True

    def actorSpawnedEvent(self, unitID, x, y, player, actor_type):
        return {'timestamp' : self.time,
                'type' : 'ActorSpawned',
                'data' : {'id' : str(unitID),
                          'x' : x,
                          'y' : y,
                          'team' : player,
                          'type' : actor_type,
                          }
                }

    def actorSeenEvent(self, unitID, x, y, player, actor_type):
        return {'timestamp' : self.time,
                'type' : 'ActorSeen',
                'data' : {'id' : str(unitID),
                          'x' : x,
                          'y' : y,
                          'team' : player,
                          'type' : actor_type
                          }
                }

    def actorHiddenEvent(self, unitID):
        return {'timestamp' : self.time,
                'type' : 'ActorHidden',
                'data' : {'id' : str(unitID)}
                }

    def actorStartedMovingEvent(self, unitID, x, y, vx, vy):
        return {'timestamp' : self.time,
                'type' : 'ActorStartedMoving',
                'data' : {'id' : str(unitID),
                          'x' : x,
                          'y' : y,
                          'vx' : vx,
                          'vy' : vy
                          }
                }

    def updateActorPositionEvent(self, unitID, x, y):
        return {'timestamp' : self.time,
                'type' : 'UpdateActorPosition',
                'data' : {'id' : str(unitID),
                          'x' : x,
                          'y' : y
                          }
                }
