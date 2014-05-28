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
            
