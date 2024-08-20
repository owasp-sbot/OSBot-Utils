import inspect
import linecache
from osbot_utils.utils.Objects                          import class_full_name
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.helpers.trace.Trace_Call__Config       import Trace_Call__Config
from osbot_utils.helpers.trace.Trace_Call__Stack        import Trace_Call__Stack
from osbot_utils.helpers.trace.Trace_Call__Stack_Node   import Trace_Call__Stack_Node, EXTRA_DATA__RETURN_VALUE
from osbot_utils.helpers.trace.Trace_Call__Stats        import Trace_Call__Stats

DEFAULT_ROOT_NODE_NODE_TITLE = 'Trace Session'
GLOBAL_FUNCTIONS_TO_IGNORE   = ['value_type_matches_obj_annotation_for_attr'       ,            # these are type safety functions which introduce quite a lot of noise in the traces (and unless one is debugging type safety, they will not be needed)
                                'value_type_matches_obj_annotation_for_union_attr' ,            # todo: map out and document why exactly these methods are ignore (and what is the side effect)
                                'are_types_compatible_for_assigment'               ,
                                'obj_attribute_annotation'                         ,
                                'get_origin'                                       ,
                                'getmro'                                           ,
                                'default_value'                                    ,
                                'raise_exception_on_obj_type_annotation_mismatch'  ,
                                '__cls_kwargs__'        ,
                                '__default__value__'    ,
                                '__setattr__'           ,
                                '<module>']
GLOBAL_MODULES_TO_IGNORE     = ['osbot_utils.helpers.trace.Trace_Call'               ,            # todo: map out and document why exactly these modules are ignore (and what is the side effect)
                                'osbot_utils.helpers.trace.Trace_Call__Config'       ,
                                'osbot_utils.helpers.trace.Trace_Call__View_Model'   ,
                                'osbot_utils.helpers.trace.Trace_Call__Print_Traces' ,
                                'osbot_utils.helpers.trace.Trace_Call__Stack'        ,
                                'osbot_utils.base_classes.Type_Safe'                 ,
                                'osbot_utils.helpers.CPrint'                         ,            #       also see if this should be done here or at the print/view stage
                                'osbot_utils.helpers.Print_Table'                    ,
                                'osbot_utils.decorators.methods.cache_on_self'       ,
                                'codecs'                                             ]

#GLOBAL_MODULES_TO_IGNORE = []
#GLOBAL_FUNCTIONS_TO_IGNORE = []

class Trace_Call__Handler(Kwargs_To_Self):
    config : Trace_Call__Config
    stack  : Trace_Call__Stack
    stats  : Trace_Call__Stats


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config.title  = self.config.title or DEFAULT_ROOT_NODE_NODE_TITLE                           # Title for the trace root node
        self.stack.config  = self.config

    def add_default_root_node(self):
        return self.stack.add_node(title=self.config.title)

    def add_line(self, frame):
        if self.config.trace_capture_lines:
            if frame:
                target_node = self.stack.top()  # lines captured are added to the current top of the stack
                #obj_info(target_node)
                if self.stack.top():
                    target_node__func_name = target_node.func_name
                    target_node__module    = target_node.module
                    frame_func_name        = frame.f_code.co_name
                    frame_module           = frame.f_globals.get("__name__", "")
                    if frame_func_name == target_node__func_name:
                        if frame_module == target_node__module:
                            return self.add_line_to_node(frame, target_node, 'line')
        return False

    def add_line_to_node(self, frame, target_node, event):
        def source_code_for_frame(function_name):
            try:
                return inspect.getsource(frame.f_code)
            except Exception as error:
                return ''
                #print(self.stack.line_index, f'def {function_name}() : error]  {error}' )
                #return f'def {function_name}() : [error]  {error}'

        if frame and target_node:
            func_name  = frame.f_code.co_name
            module     = frame.f_globals.get("__name__", "")
            self_local = class_full_name(frame.f_locals.get('self'))
            stack_size = len(self.stack)
            line =''
            line_number=0
            if event == 'call':                                                     # if this is a call we need to do the code below to get the actual method signature (and decorators)
                function_name       = frame.f_code.co_name
                filename            = frame.f_code.co_filename                             # Get the filename where the function is defined
                start_line_number   = frame.f_code.co_firstlineno                 # Get the starting line number
                source_lines        = source_code_for_frame(function_name).split('\n')
                if source_lines:
                    def_line_number     = start_line_number                         # Try to find the actual 'def' line
                    for line in source_lines:
                        if line.strip().startswith('def ' + function_name):
                            break
                        def_line_number += 1
                    else:
                        def_line_number = start_line_number                      # If the 'def' line wasn't found, default to the starting line
                    line_number = def_line_number
                    line = linecache.getline(filename, line_number).rstrip()            # todo: refactor this to not capture this info here, and to use the Ast_* utils to get a better source code mapping
            else:
                filename    = frame.f_code.co_filename  # get the filename
                line_number = frame.f_lineno                          # get the current line number
                line        = linecache.getline(filename, line_number)         # get the line

            if line:
                self.stack.line_index += 1
                line_data = dict(event=event, index = self.stack.line_index, func_name=func_name,
                                 line = line.rstrip(), line_number=line_number,
                                 module=module,  self_local=self_local,
                                 stack_size=stack_size)
                target_node.lines.append(line_data)
                return True
            # else:
            #     print(f'no line for : {self.stack.line_index}, {module}.{func_name}')
        return False

    def add_frame(self, frame):
        return self.handle_event__call(frame)

    def add_trace_ignore(self, value):
        self.config.trace_ignore_start_with.append(value)
        return

    def handle_event__call(self, frame):
        if frame:
            if self.config.capture_frame_stats:
                self.stats.log_frame(frame)
            if self.should_capture(frame):
                new_node = self.stack.add_frame(frame)
                if self.config.trace_capture_lines:
                    self.add_line_to_node(frame, new_node,'call')
                return  new_node
            else:
                self.stats.calls_skipped += 1

    def handle_event__line(self, frame):
        return self.add_line(frame)


    def handle_event__return(self, frame, return_value=None):
        if return_value and self.config.capture_extra_data:
            extra_data = { EXTRA_DATA__RETURN_VALUE : return_value}
        else:
            extra_data = {}
        return self.stack.pop(target=frame, extra_data = extra_data)

    def should_capture(self, frame):                                                    # todo: see if we can optimise these 3 lines (starting with frame.f_code) which are repeated in a number of places here
        if self.config.trace_up_to_depth:
            if len(self.stack) > self.config.trace_up_to_depth:
                return False

        capture = False
        if frame:
            code        = frame.f_code                                                      # Get code object from frame
            func_name   = code.co_name                                                      # Get function name
            module      = frame.f_globals.get("__name__", "")                               # Get module name

            if module in GLOBAL_MODULES_TO_IGNORE:                                         # check if we should skip this module
                return False

            if func_name in GLOBAL_FUNCTIONS_TO_IGNORE:                                     # check if we should skip this function
                return False

            if module and func_name:
                if self.config.trace_capture_all:
                    capture = True
                else:
                    for item in self.config.trace_capture_start_with:                                  # capture if the module starts with
                        if item:                                                                       # prevent empty queries  (which will always be true)
                            if module.startswith(item) or item =='*':
                                capture = True
                                break
                    for item in self.config.trace_capture_contains:                                    # capture if module of func_name contains
                        if item:                                                                       # prevent empty queries  (which will always be true)
                            if item in module or item in func_name:
                                capture = True
                                break
                if self.config.trace_show_internals is False and func_name.startswith('_'):                   # Skip private functions
                    capture = False

                for item in self.config.trace_ignore_start_with:                                       # Check if the module should be ignored
                    if module.startswith(item) or func_name.startswith(item):
                        capture = False
                        break

                for item in self.config.trace_ignore_contains:                                       # Check if the module should be ignored
                    if item in module or item in func_name:
                        capture = False
                        break
        return capture

    def stack_json__parse_node(self, stack_node: Trace_Call__Stack_Node):
        node         = stack_node.data()
        new_children = []
        for child in node.get('children'):
            new_children.append(self.stack_json__parse_node(child))
        node['children'] = new_children
        return node

    def stack_top(self):
        if self.stack:
            return self.stack[-1]

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            self.stats.calls +=1
            self.handle_event__call(frame)                  # todo: handle bug with locals which need to be serialised, since it's value will change
        elif event == 'return':
            self.stats.returns += 1
            self.handle_event__return(frame, arg)
        elif event == 'exception':
            self.stats.exceptions +=1                  # for now don't handle exception events
        elif event == 'line':
            self.handle_event__line(frame)
            self.stats.lines +=1
        else:
            self.stats.unknowns += 1

        return self.trace_calls



    def traces(self):
        def map_traces(node, all_traces):
            if node:
                all_traces.append(node)
                for child in node.children:
                    map_traces(child, all_traces)
        result = []
        map_traces(self.stack.root_node, result)
        return result
