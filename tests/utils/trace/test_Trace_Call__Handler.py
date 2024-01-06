import sys
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import method_line_number
from osbot_utils.utils.Misc import random_value, list_set

from osbot_utils.utils.Objects import base_classes

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler


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



    def test_trace_calls__direct_invoke(self):
        frame   = sys._getframe()         # get a valid frame object
        event   = 'call'
        arg     = None

        self.handler.config.trace_capture_all = True
        self.handler.trace_calls(frame, event, arg)

        stack_0 = self.handler.stack[0]
        stack_1 = self.handler.stack[1]


        assert stack_0 == dict(call_index = 0               ,
                               children   =  [stack_1]      ,
                               name       = 'Trace Session' )


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
        self.handler.config.trace_capture_start_with = ['test']
        self.handler.config.trace_capture_source_code = True
        self.handler.trace_calls( sys._getframe(),  'call', None)

        method_in_frame         = test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 3
        source_code_location    = f'{source_code_file}:{source_code_line_number}'

        stack_1 = self.handler.stack[1]
        assert stack_1.get('name'                ) == 'test_Trace_Call__Handler.test_Trace_Call__Handler.test_trace_calls__direct_invoke__variations'
        assert stack_1.get('source_code'         ) == "self.handler.trace_calls( sys._getframe(),  'call', None)"
        assert stack_1.get('source_code_caller'  ) == 'method()'
        assert stack_1.get('source_code_location') == source_code_location
        assert len(self.handler.stack) == 2


    def test_add_trace_ignore(self):
        value = random_value()
        assert self.handler.config.trace_ignore_start_with == []
        assert self.handler.add_trace_ignore(value) is None
        assert self.handler.config.trace_ignore_start_with == [value]