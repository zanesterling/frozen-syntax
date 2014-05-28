import collections

class event:
    def __init__(self):
        self.event_deque = collections.deque()

    def create_event(self, new_event):
        #Extend the deque to be large enough to contain the new event.
        while len(self.event_deque) <= new_event['timestamp']:
            self.event_deque.append([])
        #And then add the new event to that list.
        self.event_deque[new_event['timestamp']].append(new_event)

    def actor_seen(self, time, unitID, x, y, player, actor_type):
        return {'timestamp' : time,
                'type' : 'ActorSeen',
                'data' : {'id' : unitID,
                          'x' : x,
                          'y' : y,
                          'team' : player,
                          'type' : actor_type
                          }
                }

    def actor_hidden(self, time, unitID):
        return {'timestamp' : time,
                'type' : 'ActorHidden',
                'data' : {'id' : unitID
                          }
                }

    def actor_velocity_change(self, time, unitID, x, y, vx, vy):
        return {'timestamp' : time,
                'type' : 'ActorVelocityChange',
                'data' : {'id' : unitID,
                          'x' : x,
                          'y' : y,
                          'vx' : vx,
                          'vy' : vy
                          }
                }

    def actor_position_update(self, time, unitID, x, y):
        return {'timestamp' : time,
                'type' : 'ActorPositionUpdate',
                'data' : {'id' : unitID,
                          'x' : x,
                          'y': y
                          }
                }
