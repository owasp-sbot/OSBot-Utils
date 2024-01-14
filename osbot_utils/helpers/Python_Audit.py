import sys
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.Print_Table         import Print_Table
from osbot_utils.utils.Call_Stack import Frame_Data, Call_Stack


class Python_Audit(Kwargs_To_Self):
    audit_events : list
    frame_depth  : int = 10

    def hook_callback(self, event, args):
        if event != 'sys._getframe':                           # since sys._getframe will trigger an event (and cause a recursive loop) we have to ignore it
            frame = sys._getframe().f_back
            self.audit_events.append((event, args,frame))

    def data(self):
        data = []
        for index, item in enumerate(self.audit_events):
            (event, args, frame) = item
            call_stack = Call_Stack(max_depth=self.frame_depth)
            call_stack.capture_frame(frame)
            data.append({'index':index, 'event': event, 'args': args, 'stack': call_stack.stats()})
        return data

    def start(self):
        sys.addaudithook(self.hook_callback)
        return self

    def events(self):
        return self.audit_events

    def events_by_type(self):
        events_by_type = {}
        for event, args, stack in self.audit_events:
            events_by_type[event] = events_by_type.get(event, 0) + 1
        return events_by_type

    def print(self):
        with Print_Table() as _:
            _.add_data(self.data())
            _.set_order('index', 'event', 'args', 'stack')
            _.print()

    def size(self):
        return len(self.events)