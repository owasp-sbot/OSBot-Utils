import linecache
import sys
import traceback

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.CPrint              import CPrint
from osbot_utils.helpers.Print_Table         import Print_Table, CHAR_TABLE_HORIZONTAL, CHAR_TABLE_TOP_LEFT, CHAR_TABLE_VERTICAL, CHAR_TABLE_BOTTOM_LEFT
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Objects               import obj_data, class_full_name

MODULES_TO_STOP_CAPTURE   = ['unittest.case']
PRINT_STACK_COLOR_THEMES  = { 'default'    : ('none'          , 'none'  , 'none' ),
                              'minty'      : ('green'         , 'grey'  , 'cyan' ) ,
                              'meadow'     : ('blue'          , 'none'  ,'green' ) ,
                              'aquamarine' : ('bright_cyan'   , 'cyan'  ,'blue'  ),
                              'autumn'     : ('bright_yellow' , 'yellow','red'   )}

class Frame_Data(Kwargs_To_Self):
    depth         : int
    caller_line   : str
    method_line   : str
    method_name   : str
    line_number   : int
    local_self    : str
    module        : str

    def __repr__(self):
        return f"{self.data()})"

    def data(self):
        return self.__locals__()

class Call_Stack(Kwargs_To_Self):
    capture_locals : bool = False
    cprint         : CPrint
    cprint_theme   : str = 'meadow'
    frames         : list
    max_depth      : int  = 10

    __print_order__: list = ['module', 'method_name', 'caller_line', 'method_line',  'local_self', 'line_number', 'depth']

    def __repr__(self):
        return "Call_Stack"

    def calls(self):
        calls = []
        for frame in self.frames:
            method_name = frame.method_name
            module = frame.module
            call = f"{module}.{method_name}"
            calls.append(call)
        return calls

    def capture(self,skip_caller=True):
        current_frame = sys._getframe().f_back
        if skip_caller:
            current_frame = current_frame.f_back
        return self.capture_frame(current_frame)

    def capture_frame(self, frame):
        depth = 0
        while frame:
            if self.stop_capture(frame, depth):
                break
            new_frame = self.new_frame(frame,depth)
            self.frames.append(new_frame)
            depth += 1
            frame = frame.f_back
        return self

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
        method_name        = frame.f_code.co_name
        caller_line_number = frame.f_lineno
        method_line_number = frame.f_code.co_firstlineno

        caller_line    = linecache.getline(file_path, caller_line_number).strip()
        method_line    = linecache.getline(file_path, method_line_number).strip()   # see if we need to add the code to resolve the function from the decorators
        module         = frame.f_globals.get("__name__", "")
        local_self     = class_full_name(frame.f_locals.get('self'))
        frame_data     = Frame_Data( depth          = depth              ,
                                     caller_line    = caller_line        ,
                                     method_line    = method_line        ,
                                     method_name    = method_name        ,
                                     module         = module             ,
                                     local_self     = local_self         ,
                                     line_number    = caller_line_number )
        if self.capture_locals:
            frame_data.locals = frame.f_locals,
        return frame_data

    def print(self):
        print()
        print()
        for line in self.print_lines():
            print(line)

    def print_lines(self):
        self.cprint.lines      = []
        self.cprint.auto_print = False
        calls = self.calls()

        if len(calls) == 0:
            return []

        if len(calls) == 1:
            self.print_with_color('none', f"{CHAR_TABLE_HORIZONTAL} {calls[0]}")
        else:
            color_top, color_middle, color_bottom = self.stack_colors()
            self.print_with_color(color_top, text=f"{CHAR_TABLE_TOP_LEFT} {calls[0]}")
            for call in calls[1:-1]:
                self.print_with_color(color_middle, text=f"{CHAR_TABLE_VERTICAL} {call}")
            self.print_with_color(color_bottom, text=f"{CHAR_TABLE_BOTTOM_LEFT} {calls[-1]}")
        return self.cprint.lines


    def stack_colors(self):
        color_themes = PRINT_STACK_COLOR_THEMES
        stack_colors = color_themes.get(self.cprint_theme)
        if not stack_colors:
            stack_colors = color_themes.get('default')
        return stack_colors

    def print_with_color(self, color_name, text):
        self.cprint.__getattribute__(color_name)(text)

    def print_table(self):
        all_data = []
        for frame in self.frames:
            all_data.append(frame.data())

        with Print_Table() as _:
            _.print(all_data,self.__print_order__)




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

