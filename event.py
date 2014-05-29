import collections
import json

class Event(object):
    def __init__(self):
        self.event_deque = collections.deque()

    def create_event(self, new_event):
        #Extend the deque to be large enough to contain the new event.
        while len(self.event_deque) <= new_event['timestamp']:
            self.event_deque.append([])
        #And then add the new event to that list.
        merge_event_into_list(new_event, self.event_deque[new_event['timestamp']])

    def actor_seen(self, time, unitID, x, y, player, actor_type):
        create_event({'timestamp' : time,
                      'type' : 'ActorSeen',
                      'data' : {'id' : unitID,
                                'x' : x,
                                'y' : y,
                                'team' : player,
                                'type' : actor_type
                            }
                  })

    def actor_hidden(self, time, unitID):
        create_event({'timestamp' : time,
                      'type' : 'ActorHidden',
                      'data' : {'id' : unitID
                            }
                  })

    def actor_velocity_change(self, time, unitID, x, y, vx, vy):
        create_event({'timestamp' : time,
                      'type' : 'ActorVelocityChange',
                      'data' : {'id' : unitID,
                                'x' : x,
                                'y' : y,
                                'vx' : vx,
                                'vy' : vy
                            }
                  })

    def actor_position_update(self, time, unitID, x, y):
        create_event({'timestamp' : time,
                      'type' : 'ActorPositionUpdate',
                      'data' : {'id' : unitID,
                                'x' : x,
                                'y': y
                            }
                  })



    def get_event_json(self):
        return json.dumps([x for x in self.event_deque])

def merge_event_into_list(new_event, event_list):
    for i in xrange(len(event_list)-1, -1, -1): #iterate backward through the indices
        merged_events = merge_events(new_event, event_list[i])
        if merge_events(new_event, event_list[i]):
            event_list[i] = merge_events(new_event, event_list[i])
            return
    event_list.append(new_event)
    
def merge_events(new_event, old_event):
    if new_event['data']['id'] = old_event['data']['id']:
        new_type = new_event['type']
        old_type = old_event['type']
        if new_type == old_type:
            return new_event
        if new_type == 'ActorVelocityChange' and old_type == 'ActorPositionUpdate':
            return new_event
        if new_type == 'ActorPositionUpdate' and old_type == 'ActorVelocityChange':
            old_event['data']['x'] = new_event['data']['x']
            old_event['data']['y'] = new_event['data']['y']
            return old_event
    return False
