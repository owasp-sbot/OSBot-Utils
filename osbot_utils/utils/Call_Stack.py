import inspect
import linecache
import sys
import traceback

from osbot_utils.helpers.Print_Table         import Print_Table
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Objects               import obj_data, class_full_name

MODULES_TO_STOP_CAPTURE = ['unittest.case']

class Frame_Data(Kwargs_To_Self):
    depth         : int
    function_name : str
    caller_line   : str
    method_line   : str
    line_number   : int
    local_self    : str
    module        : str

    def __repr__(self):
        return f"{self.data()})"

    def data(self):
        return self.__locals__()

class Call_Stack(Kwargs_To_Self):
    max_depth      : int  = 10
    frames         : list
    capture_locals : bool = False
    __print_order__: list = ['depth', 'module', 'function_name', 'caller_line', 'method_line',  'local_self', 'line_number']

    def capture(self):
        return sys._getframe().f_back

    def capture_frame(self, frame):
        depth = 0
        while frame:
            if self.stop_capture(frame, depth):
                break
            new_frame = self.new_frame(frame,depth)
            self.frames.append(new_frame)
            depth += 1
            frame = frame.f_back
        return self.frames

    def stats(self):
        return { 'depth' : len(self.frames)  }

    def stop_capture(self, frame, depth):
        if frame  is None:
            return True
        if depth > self.max_depth:
            return True
        module = frame.f_globals.get("__name__", "")

        if module in MODULES_TO_STOP_CAPTURE:
            return True
        return False

    def new_frame(self, frame, depth):
        file_path          = frame.f_code.co_filename
        function_name      = frame.f_code.co_name
        caller_line_number = frame.f_lineno
        method_line_number = frame.f_code.co_firstlineno

        caller_line    = linecache.getline(file_path, caller_line_number).strip()
        method_line    = linecache.getline(file_path, method_line_number).strip()   # see if we need to add the code to resolve the function from the decorators
        module         = frame.f_globals.get("__name__", "")
        local_self     = class_full_name(frame.f_locals.get('self'))
        frame_data     = Frame_Data( depth          = depth              ,
                                     function_name  = function_name      ,
                                     caller_line    = caller_line        ,
                                     method_line    = method_line        ,
                                     module         = module             ,
                                     local_self     = local_self         ,
                                     line_number    = caller_line_number )
        if self.capture_locals:
            frame_data.locals = frame.f_locals,
        return frame_data

    def print(self):
        all_data = []
        for frame in self.frames:
            all_data.append(frame.data())

        with Print_Table() as _:
            _.print(all_data, order=self.__print_order__)



    # print()
    # for index, frame_data in enumerate(call_stack_frames_data(20)):
    #     print(index, frame_data.get('line'))


def call_stack_current_frame(return_caller=True):
    if return_caller:
        return sys._getframe().f_back
    return sys._getframe()

def call_stack_format_stack(depth=None):
    return traceback.format_stack(limit=depth)

def call_stack_frames(depth=None):
    return traceback.extract_stack(limit=depth)

def call_stack_frames_data(depth=None):
    frames_data = []
    for frame in call_stack_frames(depth=depth):
        frames_data.append(obj_data(frame))
    return frames_data

def frames_in_threads():
    return sys._current_frames()

