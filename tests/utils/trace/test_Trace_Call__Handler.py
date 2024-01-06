import sys
from unittest import TestCase
from unittest.mock import patch, call, MagicMock, PropertyMock

from osbot_utils.utils.Call_Stack import call_stack_current_frame
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import method_line_number
from osbot_utils.utils.Misc import random_value, list_set

from osbot_utils.utils.Objects import base_classes

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler, DEFAULT_ROOT_NODE_NODE_TITLE


class test_Trace_Call__Handler(TestCase):

    def setUp(self):
        self.handler = Trace_Call__Handler()

    def test___default_kwargs(self):
        default_kwargs = Trace_Call__Handler.__default_kwargs__()
        assert list_set(default_kwargs) == ['call_index', 'config', 'stack']
        assert type(default_kwargs.get('config')) is Trace_Call__Config
        assert default_kwargs.get('call_index') == 0
        assert default_kwargs.get('stack'     ) == []


    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call__Handler)
        assert list_set(self.handler.__locals__()) == list_set(self.handler.__default_kwargs__()) + ['trace_title']
        assert self.handler.trace_title == DEFAULT_ROOT_NODE_NODE_TITLE
        assert self.handler.stack       == [{'call_index': 0, 'children': [], 'name': DEFAULT_ROOT_NODE_NODE_TITLE}]

    def test_add_node(self):
        sample_frame  = call_stack_current_frame().f_back  # f_back so that test_map_full_name is the frame we are looking at
        stack         = self.handler.stack
        root_node     = self.handler.stack[0]

        assert len(stack) ==1
        assert stack     == [root_node]
        assert root_node == {'call_index': 0, 'children': [], 'name': 'Trace Session'}

        # case 1: with bad data
        assert self.handler.add_node(frame=None        , new_node=None) is False
        assert self.handler.add_node(frame=sample_frame, new_node=None) is False
        assert self.handler.add_node(frame=None        , new_node={}  ) is False
        assert stack == [root_node]        # confirm no changes made to the default stack

        # case 2: adding a valid frame and node with missing fields (it needs ['call_index', 'children', 'name'])
        node_bad = {'node_1' : 'data goes here' }
        assert self.handler.add_node(frame=sample_frame, new_node=node_bad) is False

        # case 3: adding valid frame and node
        node_1 = dict(call_index=1, children=[], name='node_1')
        assert stack                                        == [root_node]
        assert stack[-1]                                    == root_node
        assert stack[-1]['children']                        == []
        assert len(stack)                                   == 1
        assert sample_frame.f_locals.get('__trace_depth')   is None                     # confirm that the frame doesn't have the __trace_depth attribute

        assert self.handler.add_node(frame=sample_frame, new_node=node_1) is True

        assert sample_frame.f_locals.get('__trace_depth')  == len(stack)  # confirm that the frame now has the __trace_depth attribute
        assert len(stack)                                  == 2
        assert stack[-1]                                   == node_1
        assert stack                                       == [root_node, node_1]
        assert stack[-2]                                   == root_node
        assert root_node.get('children')                   == [node_1]
        assert root_node                                   == {'call_index': 0,  'children': [ node_1 ],  'name': DEFAULT_ROOT_NODE_NODE_TITLE}

        # case 3: adding another valid node
        node_2 = dict(call_index=2, children=[], name='node_2')
        assert self.handler.add_node(frame=sample_frame, new_node=node_2) is True
        assert sample_frame.f_locals.get('__trace_depth')  == len(stack)  # confirm that the frame now has the __trace_depth attribute
        assert len(stack)                                  == 3
        assert stack[-1]                                   == node_2
        assert stack[-2]                                   == node_1
        assert stack[-3]                                   == root_node
        assert stack                                       == [root_node, node_1, node_2]
        assert node_1.get('children')                      == [node_2]
        assert root_node.get('children')                   == [node_1]
        assert root_node                                   == {'call_index': 0,  'children': [ node_1 ],  'name': DEFAULT_ROOT_NODE_NODE_TITLE}
        assert node_1                                      == {'call_index': 1,  'children': [ node_2 ],  'name': 'node_1'                    }
        assert node_2                                      == {'call_index': 2,  'children': [        ],  'name': 'node_2'                    }





    def test_add_trace_ignore(self):
        value = random_value()
        assert self.handler.config.trace_ignore_start_with == []
        assert self.handler.add_trace_ignore(value) is None
        assert self.handler.config.trace_ignore_start_with == [value]

    def test_create_stack_node(self):
        create_stack_node = self.handler.create_stack_node
        config            = self.handler.config

        # case 1: with bad data
        assert create_stack_node(frame=None, full_name=None, source_code=None, call_index=None) ==  {'call_index': None, 'children': [], 'name': None}

        # case 2: with empty data
        source_code = {'source_code': '', 'source_code_caller': '', 'source_code_location': ''}
        assert create_stack_node(frame=None, full_name='', source_code=source_code, call_index=0) == {'call_index'          : 0  ,
                                                                                                      'children'            : [] ,
                                                                                                      'name'                : '' ,
                                                                                                      'source_code'         : '' ,
                                                                                                      'source_code_caller'  : '' ,
                                                                                                      'source_code_location': '' }
        # case 2: with valid stack
        assert config.capture_locals is True
        sample_frame = call_stack_current_frame().f_back
        assert create_stack_node(frame=sample_frame, full_name='', source_code=source_code, call_index=0) == { 'call_index'          : 0                     ,
                                                                                                               'children'            : []                    ,
                                                                                                               'locals'              : sample_frame.f_locals ,
                                                                                                               'name'                : ''                    ,
                                                                                                               'source_code'         : ''                    ,
                                                                                                               'source_code_caller'  : ''                    ,
                                                                                                               'source_code_location': ''                    }
        # case 3: with valid stack and config.capture_locals set to False
        config.capture_locals = False
        assert create_stack_node(frame=sample_frame, full_name='', source_code=source_code, call_index=0) == { 'call_index'          : 0  ,
                                                                                                               'children'            : [] ,
                                                                                                               'name'                : '' ,
                                                                                                               'source_code'         : '' ,
                                                                                                               'source_code_caller'  : '' ,
                                                                                                               'source_code_location': '' }

    def test_handle_event__call(self):
        config             = self.handler.config
        handle_event__call = self.handler.handle_event__call
        should_capture     = self.handler.should_capture
        stack              = self.handler.stack

        # case 1: invoke with bad data
        assert handle_event__call(frame=None) is False

        # case 2: invoke with valid frame but capture is false
        sample_frame = call_stack_current_frame().f_back               # f_back so that test_map_full_name is the frame we are looking at
        code         = sample_frame.f_code                              # Get code object from frame
        func_name    = code.co_name                                     # Get function name
        module       = sample_frame.f_globals.get("__name__", "")       # Get module name
        assert should_capture(module, func_name)      is False          # confirm that the function should not be captured
        assert handle_event__call(frame=sample_frame) is False

        # case 2: invoke with valid frame but capture is true
        assert module == 'test_Trace_Call__Handler'
        config.capture_locals           = False
        config.trace_capture_start_with = [module]
        assert should_capture(module, func_name)      is True           # confirm that the function should be captured
        assert len(stack) == 1
        assert handle_event__call(frame=sample_frame) is True
        assert len(stack) == 2
        new_node = stack[-1]
        assert new_node == {  'call_index'          : 1     ,
                              'children'            : []    ,
                              'name'                : 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_handle_event__call',
                              'source_code'         : ''    ,
                              'source_code_caller'  : ''    ,
                              'source_code_location': ''    }

    def test_handle_event__return(self):
        config               = self.handler.config
        handle_event__call   = self.handler.handle_event__call
        handle_event__return = self.handler.handle_event__return
        stack                = self.handler.stack
        sample_frame         = call_stack_current_frame().f_back

        # case 1: invoke with bad data
        assert handle_event__return(frame=None) is False

        # case 2: invoke with valid frame by no stack
        assert len(stack) == 1
        assert handle_event__return(frame=None) is False

        # case 3: invoke with valid frame and valid stack

        assert stack == [{'call_index': 0, 'children': [], 'name': 'Trace Session'}]
        assert len(stack) == 1
        config.trace_capture_all = True
        config.capture_locals    = False
        assert sample_frame.f_locals.get('__trace_depth')  is None

        assert handle_event__call(frame=sample_frame) is True                   # add node using handle_event__call
        assert sample_frame.f_locals.get('__trace_depth') == 2
        assert len(stack) == 2

        assert handle_event__return(frame=sample_frame) is True                 # remove node using handle_event__return
        assert sample_frame.f_locals.get('__trace_depth') == 2
        assert len(stack) == 1

        assert stack == [{'call_index': 0,
                          'children': [{'call_index': 1,
                                        'children': [],
                                        'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_handle_event__return',
                                        'source_code': '',
                                        'source_code_caller': '',
                                        'source_code_location': ''}],
                          'name': 'Trace Session'}]

    def test_map_full_name(self):
        sample_frame  = call_stack_current_frame().f_back                       # f_back so that test_map_full_name is the frame we are looking at
        map_full_name = self.handler.map_full_name

        # case 1: with bad data
        assert map_full_name(frame=None, module=None, func_name=None) is None
        assert map_full_name(frame=None, module='aa', func_name=None) is None
        assert map_full_name(frame=None, module=None, func_name='bb') is None
        assert map_full_name(frame=None, module='',   func_name='')   is None
        assert map_full_name(frame=None, module='aa', func_name='')   is None
        assert map_full_name(frame=None, module='',   func_name='bb') is None

        # case 2: with good frame and empty module and func_name
        assert map_full_name(frame=sample_frame, module= None, func_name=None) is None
        assert map_full_name(frame=sample_frame, module='aaa', func_name=None) is None
        assert map_full_name(frame=sample_frame, module='aaa', func_name=''  ) is None

        # case 3: with good frame and valid module and func_name
        assert map_full_name(frame=sample_frame, module='aaa', func_name='bbb') == 'aaa.test_Trace_Call__Handler.bbb'

        # case 4: with variations of self value

        mock_frame          = MagicMock()
        mock_instance       = MagicMock()
        expected_class_name = 'YourClassName'
        mock_instance.__class__.__name__ = expected_class_name
        mock_frame.f_locals = {'self': mock_instance }

        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.YourClassName.bbb'
        mock_instance.__class__.__name__  = ''
        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.bbb'

        type(mock_instance).class_name = PropertyMock(side_effect=Exception)    # When __class__.__name__ is accessed, raise an exception
        mock_frame.f_locals = {'self': None}                           # Set the 'self' in f_locals to the mock instance
        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.bbb'




    def test_map_source_code(self):
        sample_frame    = call_stack_current_frame().f_back
        map_source_code = self.handler.map_source_code
        config          = self.handler.config

        # case 1: with trace_capture_source_code set to False
        assert config.trace_capture_source_code is False
        assert map_source_code(sample_frame) == {'source_code': '', 'source_code_caller': '', 'source_code_location': ''}

        # case 2: with trace_capture_source_code set to True
        config.trace_capture_source_code = True
        method_in_frame         = test_Trace_Call__Handler.test_map_source_code
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 15
        source_code_location    = f'{source_code_file}:{source_code_line_number}'
        source_code             = map_source_code(sample_frame)
        assert  source_code == { 'source_code': 'source_code             = map_source_code(sample_frame)'  ,
                                 'source_code_caller': 'method()'                                       ,
                                 'source_code_location': source_code_location                           }



    def test_new_stack_node(self):
        title      = random_value()
        call_index = random_value()
        assert self.handler.new_stack_node(title, call_index) == {'call_index': call_index, 'children': [], 'name': title}


    def test_should_capture(self):
        should_capture = self.handler.should_capture
        config         = self.handler.config

        # check default config values that impact logic

        assert config.trace_capture_all      is False
        assert config.trace_ignore_internals is True

        # case 1: with invalid values on module and/or func_name
        assert should_capture(module=None , func_name=None) is False
        assert should_capture(module='aa' , func_name=None) is False
        assert should_capture(module=None , func_name='bb') is False
        assert should_capture(module=''   , func_name=''  ) is False
        assert should_capture(module='aa' , func_name=''  ) is False
        assert should_capture(module=''   , func_name='bb') is False

        # case 2: trace_capture_all is True
        config.trace_capture_all = True
        assert should_capture(module='aa' ,func_name='bb') is True
        assert should_capture(module=None, func_name='bb') is False
        assert should_capture(module='aa', func_name=None) is False

        # case 3: with trace_capture_start_with set
        config.trace_capture_all = False
        config.trace_capture_start_with = ['module_a']
        assert should_capture(module='module_a' ,func_name='func_a'   ) is True
        assert should_capture(module='module_a' ,func_name='func_b'   ) is True
        assert should_capture(module='module_a', func_name='_internal') is False
        assert should_capture(module='module_b', func_name='func_a'   ) is False
        assert should_capture(module='module_b', func_name='______'   ) is False

        # case 4: with trace_ignore_internals set for False
        config.trace_ignore_internals = False
        assert should_capture(module='module_a', func_name='func_a'   ) is True
        assert should_capture(module='module_a', func_name='_internal') is True

        # case 5: with trace_ignore_start_with set
        config.trace_ignore_internals   = True
        config.trace_ignore_start_with  = ['module_a']
        config.trace_capture_start_with = ['module_b']
        assert should_capture(module='module_a' ,func_name='func_a'   ) is False
        assert should_capture(module='module_a' ,func_name='func_b'   ) is False
        assert should_capture(module='module_a', func_name='_internal') is False
        assert should_capture(module='module_b', func_name='func_a'   ) is True
        assert should_capture(module='module_b', func_name='______'   ) is False

        # case 6: Mixed Cases for trace_capture_start_with logic
        config.trace_capture_start_with = ['mod']
        assert should_capture(module='modXYZ', func_name='func_a') is True

        # case 7 Edge Cases in Configurations
        config.trace_capture_start_with = ['']
        assert should_capture(module='anything', func_name='func_a') is True                    # Assuming empty string matches any module

        config.trace_capture_start_with = ['mod']
        config.trace_ignore_start_with  = ['mod']
        assert should_capture(module='modXYZ', func_name='func_a') is False                     # Overlapping configurations

        # case 8: Boundary Values for startswith Logic
        config.trace_ignore_start_with   = []
        config.trace_capture_start_with = ['mod']
        assert should_capture(module='mod', func_name='func_a') is True

        # case 9: nteraction Between trace_ignore_internals and trace_capture_start_with/trace_ignore_start_with
        config.trace_capture_start_with = ['mod']
        config.trace_ignore_internals   = True
        assert should_capture(module='mod', func_name='_internalFunc') is False

        # case 10: Functionality When All Configs are Empty or Default
        config.trace_capture_all        = False
        config.trace_capture_start_with = []
        config.trace_ignore_start_with  = []
        config.trace_ignore_internals   = True
        assert should_capture(module='anyModule', func_name='anyFunc') is False     # Assuming default behavior is to not capture

        # Case 11: Overlapping Patterns
        config.trace_capture_start_with = ['common']
        config.trace_ignore_start_with = ['common']
        assert should_capture(module='commonModule', func_name='func') is False

        # Case 12: Whitespace and Special Characters in Names
        assert should_capture(module='  ', func_name='func') is False
        assert should_capture(module='module', func_name='@#$') is False

        # Case 13: Long String Names
        long_string = 'a' * 1000
        assert should_capture(module=long_string, func_name=long_string) is False

        # Case 14: Special Characters in Start With Lists
        config.trace_capture_start_with = ['^', '$', '*']
        config.trace_ignore_start_with  = ['?', '+', '|']
        assert should_capture(module='^module', func_name='func') is True
        assert should_capture(module='$module', func_name='func') is True
        assert should_capture(module='*module', func_name='func') is True
        assert should_capture(module='?module', func_name='func') is False
        assert should_capture(module='+module', func_name='func') is False
        assert should_capture(module='|module', func_name='func') is False

    def test_trace_calls(self):
        config      = self.handler.config
        stack       = self.handler.stack
        trace_calls = self.handler.trace_calls
        frame_1 = call_stack_current_frame()
        frame_2 = frame_1.f_back
        frame_3 = frame_1.f_back

        assert type(frame_1).__name__ == 'frame'
        assert type(frame_2).__name__ == 'frame'
        assert type(frame_3).__name__ == 'frame'

        assert len(stack) == 1

        # case 1: with bad data
        assert trace_calls(frame=frame_1, event=None    , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='aa'    , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='call'  , arg=None) == trace_calls
        assert trace_calls(frame=frame_1, event='return', arg=None) == trace_calls
        assert trace_calls(frame=None   , event=None    , arg='aa') == trace_calls
        assert len(stack) == 1                                                      # confirm no changes made by call above

        # case 2: with valid frame and event buy with no capture
        assert trace_calls(frame_1, 'call', None) == trace_calls
        assert len(stack) == 1

        # case 3: with valid frame and event buy with no capture
        assert stack == [{'call_index': 0, 'children': [], 'name': 'Trace Session'}]
        config.trace_capture_all = True
        assert trace_calls(frame_1, 'call', None) == trace_calls
        assert len(stack) == 2
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'},
                          { 'call_index': 1,
                            'children': [],
                            'locals': {'__trace_depth': 2},
                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''}]

        assert trace_calls(frame_1, 'return', None) == trace_calls
        assert len(stack) == 1
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'}]

        assert trace_calls(frame_1, 'call', None) == trace_calls
        assert len(stack) == 2
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''},
                                          { 'call_index': 2,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'},
                          { 'call_index': 2,
                            'children': [],
                            'locals': {'__trace_depth': 2},
                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''}]

        config.capture_locals = False                                           # removing locals from here since they don't work well with tests and code coverage
        assert trace_calls(frame_2, 'call', None) == trace_calls
        assert len(stack) == 3
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''},
                                          { 'call_index': 2,
                                            'children': [ { 'call_index': 3,
                                                            'children': [],
                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                            'source_code': '',
                                                            'source_code_caller': '',
                                                            'source_code_location': ''}],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'},
                          { 'call_index': 2,
                            'children': [ { 'call_index': 3,
                                            'children': [],
                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'locals': {'__trace_depth': 2},
                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''},
                          { 'call_index': 3,
                            'children': [],
                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''}]

        assert trace_calls(frame_3, 'call', None) == trace_calls
        assert len(stack) == 4
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''},
                                          { 'call_index': 2,
                                            'children': [ { 'call_index': 3,
                                                            'children': [ { 'call_index': 4,
                                                                            'children': [],
                                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                                            'source_code': '',
                                                                            'source_code_caller': '',
                                                                            'source_code_location': ''}],
                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                            'source_code': '',
                                                            'source_code_caller': '',
                                                            'source_code_location': ''}],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'},
                          { 'call_index': 2,
                            'children': [ { 'call_index': 3,
                                            'children': [ { 'call_index': 4,
                                                            'children': [],
                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                            'source_code': '',
                                                            'source_code_caller': '',
                                                            'source_code_location': ''}],
                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'locals': {'__trace_depth': 2},
                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''},
                          { 'call_index': 3,
                            'children': [ { 'call_index': 4,
                                            'children': [],
                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''},
                          { 'call_index': 4,
                            'children': [],
                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''}]

        assert trace_calls(frame_3, 'return', None) == trace_calls
        assert len(stack) == 3
        assert stack == [ { 'call_index': 0,
                            'children': [ { 'call_index': 1,
                                            'children': [],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''},
                                          { 'call_index': 2,
                                            'children': [ { 'call_index': 3,
                                                            'children': [ { 'call_index': 4,
                                                                            'children': [],
                                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                                            'source_code': '',
                                                                            'source_code_caller': '',
                                                                            'source_code_location': ''}],
                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                            'source_code': '',
                                                            'source_code_caller': '',
                                                            'source_code_location': ''}],
                                            'locals': {'__trace_depth': 2},
                                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'Trace Session'},
                          { 'call_index': 2,
                            'children': [ { 'call_index': 3,
                                            'children': [ { 'call_index': 4,
                                                            'children': [],
                                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                                            'source_code': '',
                                                            'source_code_caller': '',
                                                            'source_code_location': ''}],
                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'locals': {'__trace_depth': 2},
                            'name': 'osbot_utils.utils.Call_Stack.call_stack_current_frame',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''},
                          { 'call_index': 3,
                            'children': [ { 'call_index': 4,
                                            'children': [],
                                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                                            'source_code': '',
                                            'source_code_caller': '',
                                            'source_code_location': ''}],
                            'name': 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls',
                            'source_code': '',
                            'source_code_caller': '',
                            'source_code_location': ''}]

        # todo: continue this test when refactored the code to use the new stack_node method
        #       there is a bug here where the __trace_depth of frame_2 and frame_3 are the same
        #       but I think this might be a side effect for how those frames were collected (and not a bug in the actual code)
        #assert trace_calls(frame_2, 'return', None) == trace_calls
        #assert len(stack) == 3
        #pprint(stack)


    def test_trace_calls__direct_invoke(self):
        frame   = sys._getframe()         # get a valid frame object
        event   = 'call'
        arg     = None

        self.handler.config.trace_capture_all = True
        self.handler.trace_calls(frame, event, arg)

        stack_0 = self.handler.stack[0]
        stack_1 = self.handler.stack[1]


        assert stack_0 == dict(call_index = 0                           ,
                               children   =  [stack_1]                  ,
                               name       = DEFAULT_ROOT_NODE_NODE_TITLE)


        stack_1_locals = dict(stack_1.get('locals'))
        del stack_1['locals']

        assert stack_1_locals ==   { '__trace_depth': 2,
                                    'arg': None,
                                    'event': 'call',
                                    'frame': frame,
                                    'self':stack_1_locals.get('self')}
        assert stack_1 == dict(call_index=1,
                               children=[],
                               name = 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls__direct_invoke',
                               source_code          =  '',
                               source_code_caller   = '' ,
                               source_code_location = '')

        assert len(self.handler.stack) == 2


    def test_trace_calls__direct_invoke__variations(self):
        sample_frame = call_stack_current_frame().f_back
        self.handler.config.trace_capture_start_with = ['test']
        self.handler.config.trace_capture_source_code = True
        self.handler.trace_calls(sample_frame, 'call', None)

        method_in_frame         = test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 4
        source_code_location    = f'{source_code_file}:{source_code_line_number}'

        stack_1 = self.handler.stack[1]
        assert stack_1.get('name'                ) == 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations'
        assert stack_1.get('source_code'         ) == "self.handler.trace_calls(sample_frame, 'call', None)"
        assert stack_1.get('source_code_caller'  ) == 'method()'
        assert stack_1.get('source_code_location') == source_code_location
        assert len(self.handler.stack) == 2


