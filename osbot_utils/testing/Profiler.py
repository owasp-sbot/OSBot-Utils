import sys

# see https://explog.in/notes/settrace.html for ideas on how to expand this class

class Profiler:

    def __init__(self):
        self.events = []
        self.profile_options   = self.default_profile_options()
        self.previous_profiler = self.current_profiler()
        self.on_event = None

    def __enter__(self):
        sys.setprofile(self.profiling_function)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        sys.setprofile(self.previous_profiler)

    def add_values(self, profile_options, source):
        item = {}
        for arg_name in set(profile_options):
            option =  profile_options.get(arg_name)
            value  = getattr(source, arg_name)
            if type(option) is dict:
                item[arg_name] = self.add_values(option, value)
            else:
                if profile_options.get(arg_name):
                    if arg_name == 'f_locals' and sys.version_info < (3, 13):    # todo: figure out why in 3.13 the value.copy doesn't work
                        item[arg_name] = value.copy()                            # create a copy of the var
                    else:
                        item[arg_name] = value
        return item

    def current_profiler(self):
        return sys.getprofile()

    def default_profile_options(self):
        return {
            'f_back'         : False,
            'f_builtins'     : False,
            'f_code'         : {
                'co_argcount'       : True ,
                'co_cellvars'       : True ,
                'co_code'           : True ,
                'co_consts'         : True ,
                'co_filename'       : True ,
                'co_firstlineno'    : True ,
                'co_flags'          : True ,
                'co_freevars'       : True ,
                'co_kwonlyargcount' : True ,
                'co_lnotab'         : True ,
                'co_name'           : True ,
                'co_names'          : True ,
                'co_nlocals'        : True ,
                'co_posonlyargcount': True ,
                'co_stacksize'      : True ,
                'co_varnames'       : True ,
            } ,
            'f_globals'      : False,
            'f_lasti'        : True ,
            'f_lineno'       : True ,
            'f_locals'       : True ,
            'f_trace'        : True ,
            'f_trace_lines'  : True ,
            'f_trace_opcodes': True
        }

    def get_last_event(self):
        return self.events.pop()

    def get_f_locals(self):
        return self.get_last_event().get('f_locals')

    def get_f_locals_variable(self, var_name):
        return self.get_f_locals().get(var_name)

    def profiling_function(self, frame, event, arg):
        if type(frame.f_locals.get('self')) != Profiler:                    # dont' capture traces of the current (Trace) class
            item = self.add_values(self.profile_options, frame)
            item['arg'  ] = arg
            item['event'] = event
            self.events.append(item)
            if self.on_event:
                self.on_event(self,frame, event, arg)                         # allow the caler to see and modify the data (after its data been captured)

    def set_on_event(self, on_event):
        self.on_event = on_event
        return self
