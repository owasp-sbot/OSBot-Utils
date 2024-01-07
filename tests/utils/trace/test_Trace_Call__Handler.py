import sys
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock

from osbot_utils.utils.Call_Stack import call_stack_current_frame
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import method_line_number
from osbot_utils.utils.Misc import random_value, list_set

from osbot_utils.utils.Objects import base_classes

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler, DEFAULT_ROOT_NODE_NODE_TITLE
from osbot_utils.utils.trace.Trace_Call__Stack import Trace_Call__Stack
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node
from osbot_utils.utils.trace.Trace_Call__Stats import Trace_Call__Stats


class test_Trace_Call__Handler(TestCase):

    def setUp(self):
        self.handler = Trace_Call__Handler()

    def test___default_kwargs(self):
        default_kwargs = Trace_Call__Handler.__default_kwargs__()
        assert list_set(default_kwargs) == ['config', 'stack', 'stats']
        assert type(default_kwargs.get('config')) is Trace_Call__Config
        assert type(default_kwargs.get('stack' )) is Trace_Call__Stack
        assert type(default_kwargs.get('stats' )) is Trace_Call__Stats



    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call__Handler)
        assert list_set(self.handler.__locals__()) == list_set(self.handler.__default_kwargs__()) + ['trace_title']
        assert self.handler.trace_title == DEFAULT_ROOT_NODE_NODE_TITLE
        assert self.handler.stack.size() == 1
        assert type(self.handler.stack.top()) is Trace_Call__Stack_Node
        assert self.handler.stack.top()       == Trace_Call__Stack_Node(name=DEFAULT_ROOT_NODE_NODE_TITLE)


    def test_add_trace_ignore(self):
        value = random_value()
        assert self.handler.config.trace_ignore_start_with == []
        assert self.handler.add_trace_ignore(value) is None
        assert self.handler.config.trace_ignore_start_with == [value]


    def test_handle_event__call(self):
        config             = self.handler.config
        handle_event__call = self.handler.handle_event__call
        should_capture     = self.handler.should_capture
        stack              = self.handler.stack

        # case 1: invoke with bad data
        assert handle_event__call(frame=None) is None

        # case 2: invoke with valid frame but capture is false
        sample_frame = call_stack_current_frame()
        #code         = sample_frame.f_code                              # Get code object from frame
        #func_name    = code.co_name                                     # Get function name
        module       = sample_frame.f_globals.get("__name__", "")       # Get module name
        assert should_capture(sample_frame)      is False          # confirm that the function should not be captured
        assert handle_event__call(frame=sample_frame) is None

        # case 2: invoke with valid frame but capture is true
        assert module == 'test_Trace_Call__Handler'
        config.capture_locals           = False
        config.trace_capture_start_with = [module]

        assert should_capture(sample_frame)      is True           # confirm that the function should be captured
        assert len(stack)   == 1
        new_node = handle_event__call(frame=sample_frame)
        assert type(new_node) is Trace_Call__Stack_Node
        assert stack[-1]    == new_node
        assert len(stack)   == 2
        assert new_node == Trace_Call__Stack_Node(call_index=1, frame=sample_frame, func_name='test_handle_event__call', name= 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_handle_event__call', module='test_Trace_Call__Handler')


    def test_handle_event__return(self):
        config               = self.handler.config
        handle_event__call   = self.handler.handle_event__call
        handle_event__return = self.handler.handle_event__return
        stack                = self.handler.stack
        sample_frame         = call_stack_current_frame()

        # case 1: invoke with bad data
        assert handle_event__return(frame=None) is False

        # case 2: invoke with valid frame by no stack
        assert len(stack) == 1
        assert handle_event__return(frame=None) is False

        # case 3: invoke with valid frame and valid stack

        assert len(stack) == 1
        assert stack[0].data() == Trace_Call__Stack_Node(name=DEFAULT_ROOT_NODE_NODE_TITLE).data()
        config.trace_capture_all = True
        config.capture_locals    = False

        assert handle_event__call(frame=sample_frame) is not None                   # add node using handle_event__call
        assert len(stack) == 2

        assert handle_event__return(frame=sample_frame) is True                 # remove node using handle_event__return
        assert len(stack) == 1

        root_node = stack[0]
        node_1    = root_node.children[0]
        assert root_node ==  Trace_Call__Stack_Node(call_index=0, children=[node_1], frame=None        , func_name='',                          name= DEFAULT_ROOT_NODE_NODE_TITLE                                                 , module=''                        )
        assert node_1    ==  Trace_Call__Stack_Node(call_index=1, children=[      ], frame=sample_frame, func_name='test_handle_event__return', name= 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_handle_event__return', module='test_Trace_Call__Handler')


    def test_should_capture(self):
        sample_frame   = call_stack_current_frame()
        should_capture = self.handler.should_capture
        config         = self.handler.config

        # check default config values that impact logic

        assert config.trace_capture_all      is False
        assert config.trace_ignore_internals is True

        # case 1: with invalid values on frame
        assert should_capture(frame=None)    is False

        # case 2: trace_capture_all is True
        config.trace_capture_all = True
        assert should_capture(frame=None        ) is False
        assert should_capture(frame=sample_frame) is True

        # case 3: with trace_capture_start_with set
        config.trace_capture_all        = False
        config.trace_capture_start_with = ['test']
        assert should_capture(frame=sample_frame ) is True


        # case 4: with trace_ignore_internals set for False
        config.trace_ignore_internals = False
        assert should_capture(frame=sample_frame) is True
        assert should_capture(frame=sample_frame) is True

        # case 5: with trace_ignore_start_with set
        config.trace_ignore_internals   = True
        config.trace_ignore_start_with  = ['test']
        config.trace_capture_start_with = ['test']
        assert should_capture(frame=sample_frame) is False

        # case 6: Mixed Cases for trace_capture_start_with logic
        config.trace_ignore_start_with  = []
        config.trace_capture_start_with = ['te']
        assert should_capture(frame=sample_frame) is True

        # case 7 Edge Cases in Configurations
        config.trace_capture_start_with = ['']
        assert should_capture(frame=sample_frame) is False                      # empty queries ('') should not have a match
        config.trace_capture_start_with = ['*']
        assert should_capture(frame=sample_frame) is True                       # empty queries ('*') will have a match


        # case 8: trace_capture_contains is set
        config.trace_ignore_start_with  = []
        config.trace_capture_start_with = []
        config.trace_capture_contains   = ['Call']                              # 'contains' hit in module
        assert should_capture(frame=sample_frame) is True
        config.trace_capture_contains = ['should_capture']                      # 'contains' hit in func_name
        assert should_capture(frame=sample_frame) is True
        config.trace_capture_contains = ['should_not_capture']                  # no 'contains' hit
        assert should_capture(frame=sample_frame) is False


        # case 9: nteraction Between trace_ignore_internals and trace_capture_start_with/trace_ignore_start_with
        config.trace_capture_start_with = ['mod']
        config.trace_ignore_internals   = True
        assert should_capture(frame=sample_frame) is False                      # todo: improve the logic of this (since it has lost a bit of the meaning after the refactoring to should_capture(frame=sample_frame) )

        # case 10: Functionality When All Configs are Empty or Default
        config.trace_capture_all        = False
        config.trace_capture_start_with = []
        config.trace_ignore_start_with  = []
        config.trace_ignore_internals   = True
        assert should_capture(frame=sample_frame) is False     # Assuming default behavior is to not capture

        # Case 11: Overlapping Patterns
        config.trace_capture_start_with = ['common']
        config.trace_ignore_start_with = ['common']
        assert should_capture(frame=sample_frame) is False


    def test_trace_calls(self):
        config      = self.handler.config
        stack       = self.handler.stack
        trace_calls = self.handler.trace_calls
        frame_1 = call_stack_current_frame(return_caller=False)
        frame_2 = frame_1.f_back
        frame_3 = frame_1.f_back


        assert type(frame_1).__name__ == 'frame'
        assert type(frame_2).__name__ == 'frame'
        assert type(frame_3).__name__ == 'frame'

        assert len(stack)         == 1
        assert self.handler.stats == Trace_Call__Stats()

        # case 1: with bad data
        assert trace_calls(frame=frame_1, event=None    , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='aa'    , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='call'  , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='return', arg=None) == trace_calls
        assert trace_calls(frame=None   , event=None    , arg='aa') == trace_calls
        assert len(stack) == 1                                                      # confirm no changes made by call above

        assert self.handler.stats == Trace_Call__Stats(event_call= 1, event_return=1, event_unknown=3)
        self.handler.stats.event_unknown = 0                                        # remove these since they were caused by the bad calls above
        # case 2: with valid frame and event buy with no capture
        assert trace_calls(frame_1, 'call', None) == trace_calls
        assert len(stack) == 1

        # case 3: with valid frame and event buy with no capture
        assert stack[0].data() == Trace_Call__Stack_Node(name=DEFAULT_ROOT_NODE_NODE_TITLE).data()
        root_node = stack[0]
        assert self.handler.stats == Trace_Call__Stats(event_call= 2, event_return=1)

        config.trace_capture_all = True
        assert trace_calls(frame_1, 'call', None) == trace_calls

        node_1    = stack[1]

        assert len(stack)     == 2
        assert stack.bottom() == root_node
        assert stack.top   () == node_1
        assert stack          == [root_node, node_1]

        assert root_node      == Trace_Call__Stack_Node(name=DEFAULT_ROOT_NODE_NODE_TITLE, children=[ node_1])
        assert node_1         == Trace_Call__Stack_Node(call_index = 1                                                       ,
                                                        frame      = frame_1                                                 ,
                                                        func_name  = 'call_stack_current_frame'                              ,
                                                        locals     = { 'return_caller': False }                              ,
                                                        module     = 'osbot_utils.utils.Call_Stack'                          ,
                                                        name       = 'osbot_utils.utils.Call_Stack.call_stack_current_frame' )


        assert trace_calls(frame_1, 'return', None) == trace_calls
        assert len(stack)         == 1
        assert stack              == [root_node]
        assert root_node.children == [node_1]

        assert trace_calls(frame_1, 'call', None) == trace_calls

        node_1_a = stack[1]
        assert len(stack)         == 2
        assert stack.bottom()     == root_node
        assert stack.top   ()     == node_1_a
        assert stack              == [root_node, node_1_a]
        assert root_node.children == [node_1, node_1_a]
        assert node_1_a           == Trace_Call__Stack_Node(call_index = 2                                                       ,
                                                            func_name  = 'call_stack_current_frame'                              ,
                                                            frame      = frame_1                                                 ,
                                                            locals     = { 'return_caller': False }                              ,
                                                            module     = 'osbot_utils.utils.Call_Stack'                          ,
                                                            name       = 'osbot_utils.utils.Call_Stack.call_stack_current_frame' )

        config.capture_locals = False                                           # removing locals from here since they don't work well with tests and code coverage
        assert trace_calls(frame_2, 'call', None) == trace_calls

        node_2 = stack[2]
        assert len(stack)         == 3
        assert stack.bottom()     == root_node
        assert stack.top   ()     == node_2
        assert stack              == [root_node, node_1_a, node_2]
        assert root_node.children == [node_1, node_1_a]
        assert node_1_a.children  == [node_2]
        assert node_2.children    == []
        assert node_2             == Trace_Call__Stack_Node(call_index = 3                                                                  ,
                                                            frame      = frame_2                                                            ,
                                                            func_name  = 'test_trace_calls'                                                 ,
                                                            module     = 'test_Trace_Call__Handler'                                         ,
                                                            name       = 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls' )

        assert trace_calls(frame_3, 'call', None) == trace_calls

        node_3 = stack[3]
        assert len(stack)         == 4
        assert stack.bottom()     == root_node
        assert stack.top   ()     == node_3
        assert stack              == [root_node, node_1_a, node_2, node_3]
        assert root_node.children == [node_1, node_1_a]
        assert node_1_a.children  == [node_2]
        assert node_2.children    == [node_3]
        assert node_3.children    == []                                             # todo: figure out why the func_name and module and the same as none_3
        assert node_3             == Trace_Call__Stack_Node(call_index = 4                                                                   ,
                                                            func_name  = 'test_trace_calls'                                                  ,
                                                            frame      = frame_3                                                            ,
                                                            module     = 'test_Trace_Call__Handler'                                          ,
                                                            name       = 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls' )
        assert self.handler.stats == Trace_Call__Stats(event_call=6, event_return=2)


        assert trace_calls(frame_3, 'return', None) == trace_calls
        assert len(stack) == 3
        assert stack.bottom()     == root_node
        assert stack.top   ()     == node_2                                 # changed to parent
        assert stack              == [root_node, node_1_a, node_2]            # node_4 is no longer here
        assert root_node.children == [node_1, node_1_a]                       # these are all the same
        assert node_1_a.children  == [node_2]
        assert node_2.children    == [node_3]
        assert node_3.children    == []
        assert self.handler.stats == Trace_Call__Stats(event_call=6, event_return=3)

        assert trace_calls(frame_2, 'return', None) == trace_calls
        assert len(stack) == 2
        assert stack.bottom()     == root_node
        assert stack.top   ()     == node_1_a
        assert stack              == [root_node, node_1_a]
        assert root_node.children == [node_1, node_1_a]
        assert node_1_a.children  == [node_2]
        assert node_2.children    == [node_3]
        assert node_3.children    == []

        assert trace_calls(frame_1, 'return', None) == trace_calls
        assert len(stack)         == 1
        assert stack.bottom()     == root_node
        assert stack.top   ()     == root_node
        assert stack              == [root_node]
        assert root_node.children == [node_1, node_1_a]
        assert node_1_a.children  == [node_2]
        assert node_2.children    == [node_3]
        assert node_3.children    == []
        assert self.handler.stats == Trace_Call__Stats(event_call=6, event_return=5)




    def test_trace_calls__direct_invoke(self):
        frame   = sys._getframe()         # get a valid frame object
        event   = 'call'
        arg     = None

        self.handler.config.trace_capture_all = True
        self.handler.trace_calls(frame, event, arg)

        stack_0 = self.handler.stack[0]
        stack_1 = self.handler.stack[1]

        assert type(stack_0) is Trace_Call__Stack_Node
        assert type(stack_1) is Trace_Call__Stack_Node


        assert stack_0.data() == Trace_Call__Stack_Node(children =  [stack_1]                  ,
                                                        name     = DEFAULT_ROOT_NODE_NODE_TITLE).data()


        stack_1_locals = stack_1.locals
        stack_1.locals = {}

        assert stack_1_locals ==   { 'arg': None,
                                     'event': 'call',
                                     'frame': frame,
                                     'self':stack_1_locals.get('self')}

        assert stack_1.data() == Trace_Call__Stack_Node(call_index = 1,
                                                        func_name  = 'test_trace_calls__direct_invoke'  ,
                                                        frame      = frame                              ,
                                                        name       = 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls__direct_invoke',
                                                        module     = 'test_Trace_Call__Handler').data()

        assert len(self.handler.stack) == 2


    def test_trace_calls__direct_invoke__variations(self):
        sample_frame = call_stack_current_frame()
        self.handler.config.trace_capture_start_with = ['test']
        self.handler.config.trace_capture_source_code = True
        self.handler.trace_calls(sample_frame, 'call', None)

        method_in_frame         = test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 4
        source_code_location    = f'{source_code_file}:{source_code_line_number}'

        stack_1 = self.handler.stack[1]

        assert stack_1.name                 == 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations'

        assert stack_1.source_code          == "self.handler.trace_calls(sample_frame, 'call', None)"
        assert stack_1.source_code_caller   == 'method()'
        assert stack_1.source_code_location == source_code_location
        assert len(self.handler.stack) == 2






