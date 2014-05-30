import collections
import json

class Event(object):
    def __init__(self):
        self.history = collections.deque()
        self.json_current = False
        self.json = None

    def throw_event(self, new_event):
        #Extend the deque to be large enough to contain the new event.
        while len(self.history) <= new_event['timestamp']:
            self.history.append([])
        #And then add the new event to that list.
        merge_event_into_list(new_event, self.history[new_event['timestamp']])
        self.json_current = False

    def actor_seen(self, time, unitID, x, y, player, actor_type):
        self.throw_event({'timestamp' : time,
                          'type' : 'ActorSeen',
                          'data' : {'id' : unitID,
                                    'x' : x,
                                    'y' : y,
                                    'team' : player,
                                    'type' : actor_type
                                }
                      })

    def actor_hidden(self, time, unitID):
        self.throw_event({'timestamp' : time,
                          'type' : 'ActorHidden',
                          'data' : {'id' : unitID
                                }
                      })

    def actor_trajectory_update(self, time, unitID, x, y, vx, vy):
        self.throw_event({'timestamp' : time,
                          'type' : 'ActorTrajectoryUpdate',
                          'data' : {'id' : unitID,
                                    'x' : x,
                                    'y' : y,
                                    'vx' : vx,
                                    'vy' : vy
                                }
                  })




    def get_event_json(self):
        if self.json_current:
            return self.json
        else:
            self.json = json.dumps([x for x in self.history])
            self.json_current = True
            return self.json

def merge_event_into_list(new_event, event_list):
    for i in xrange(len(event_list)-1, -1, -1): #iterate backward through the indices
        merged_events = merge_events(new_event, event_list[i])
        if merge_events(new_event, event_list[i]):
            event_list[i] = merge_events(new_event, event_list[i])
            return
    event_list.append(new_event)
    
def merge_events(new_event, old_event):
    if new_event['data']['id'] == old_event['data']['id']:
        new_type = new_event['type']
        old_type = old_event['type']
        if new_type == old_type:
            return new_event
    return False
