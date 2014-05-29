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



    def get_event_json(self):
        return json.dumps([x for x in self.event_deque])

def merge_event_into_list(new_event, event_list):
    empty_flag = True
    for i in xrange(len(event_list)-1, -1, -1): #iterate backward through the indices
        if event_list[i]['type'] == new_event['type'] and\
           event_list[i]['data']['id'] == new_event['data']['id']:
            last_index = i
            empty_flag = False
    if empty_flag:
        event_list.append(new_event)
    else:
        event_list[last_index] = merge_2_events(new_event, event_list[last_index])
    
def merge_2_events(new_event, old_event):
    if new_event['type'] == old_event['type']:
        return new_event
