import collections
import json

class History(object):
    def __init__(self):
        self.histories = {i : PlayerHistory() for i in xrange(2)}
        self.global_history = PlayerHistory()
    
    def clear_events(self):
        self.histories = {i : PlayerHistory() for i in xrange(2)}
        self.global_history = PlayerHistory()

    def get_events(self, player_id):
        return self.histories[player_id].get_event_json();

    def wall_added(self, wall):
        self.throw_event({'timestamp' : wall.world.timestamp,
                          'type' : 'WallAdded',
                          'data' : {'id' : wall.wallID,
                                    'x' : wall.x,
                                    'y' : wall.y,
                                    'width' : wall.width,
                                    'height' : wall.height,
                                    }
                          }, actor.visibilities)

    def actor_spawned(self, actor): #This should only be used on actors that are associated with a team
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorSpawned',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'team' : actor.player,
                                    'type' : actor.__class__.__name__,
                                    'typeID' : actor.typeID
                                }
                          }, actor.visibilities)

    def actor_died(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorDied',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'type': actor.__class__.__name__,
                                    'typeID': actor.typeID
                                    }
                          }, actor.visibilities)

    def actor_seen(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorSeen',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'type' : actor.___class___.___name__,
                                    'typeID': actor.typeID
                                }
                      }, actor.visibilities)

    def actor_hidden(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorHidden',
                          'data' : {'id' : actor.actorID,
                                    'type' : actor.___class___.___name__,
                                    'typeID': actor.typeID
                                }
                      }, actor.visibilities)

    def actor_trajectory_update(self, actor):
        self.throw_event({'timestamp' : actor.world.timestamp,
                          'type' : 'ActorTrajectoryUpdate',
                          'data' : {'id' : actor.actorID,
                                    'x' : actor.x,
                                    'y' : actor.y,
                                    'vx' : actor.vx,
                                    'vy' : actor.vy,
                                    'type': actor.__class__.__name__,
                                    'typeID' : actor.typeID
                                }
                  }, actor.visibilities)

    def turn_end(self, world):
        self.throw_event({'timestamp' : world.timestamp,
                          'type' : 'TurnEnd'
                          })

    def throw_event(self, event, visibilities=None):
        for i in range(len(self.histories)):
            if (not visibilities) or visibilities[i]:
                self.histories[i].throw_event(event)
        self.global_history.throw_event(event)

class PlayerHistory(object):
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

    def get_event_json(self):
        if not self.json_current:
            events = {str(i): self.history[i] for i in range(len(self.history))
                                              if len(self.history[i]) > 0}
            self.json = json.dumps(events)
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
