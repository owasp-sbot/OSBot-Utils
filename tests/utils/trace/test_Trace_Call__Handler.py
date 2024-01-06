import sys
from unittest import TestCase
from unittest.mock import patch, call

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


    def test_add_trace_ignore(self):
        value = random_value()
        assert self.handler.config.trace_ignore_start_with == []
        assert self.handler.add_trace_ignore(value) is None
        assert self.handler.config.trace_ignore_start_with == [value]

    # def test_map_full_name(self):
    #     map_source_code = self.handler.map_full_name
    #     config = self.handler.config

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


