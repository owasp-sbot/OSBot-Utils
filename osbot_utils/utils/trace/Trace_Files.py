from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call import Trace_Call


class Trace_Files(Trace_Call):

    files: list = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files = self.files or []

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            self.files.append(frame.f_code.co_filename)
        return super().trace_calls(frame, event, arg)


